import {selectExamQuestions,publicQuestion,applyAnswer,submitAttempt} from '../server/domain.mjs';

const initialState=()=>({version:1,optionIdsVersion:2,practice:{},attempts:{}});

/** All state changes run inside the storage adapter's atomic read/write transaction. */
export function createLocalService({loadData,store,now=()=>Date.now(),uuid=()=>crypto.randomUUID()}) {
 let dataPromise;
 const getData=()=>dataPromise??=(loadData().catch(error=>{dataPromise=undefined;throw error;}));
 return {async request(path,method='GET',body={}) {
  const data=await getData();
  if(data.version!==1)throw new Error('Dữ liệu website không tương thích. Hãy tải lại trang.');
  const {modules,sources}=data,questions=data.bank.filter(q=>q.status==='ready'),qmap=new Map(questions.map(q=>[q.id,q]));
  const sourceMap=new Map(sources.map(s=>[s.module+':'+s.page,s]));
  const moduleMap=new Map(modules.map(m=>[m.id,m]));
  const enrich=q=>({...q,sources:q.sources.map(s=>{
   const metadata=sourceMap.get(s.module+':'+s.page),file=moduleMap.get(s.module)?.file||s.file;
   return {...metadata,...s,file,image:`assets/sources/${s.module}/${s.page}.webp`,pdf:`slides/${encodeURIComponent(file)}#page=${s.page}`};
  })});
  const outcome=await store.update(saved=>{
   const timestamp=now();
   const state=saved||initialState();
   if(state.version!==1)return {state,value:{error:'Phiên bản tiến độ không được hỗ trợ; dữ liệu của bạn được giữ nguyên.'}};
   const snapshot=a=>a.snapshots||a.questionIds.map(id=>qmap.get(id));
   const settle=a=>{if(a.status==='active'&&timestamp>=a.deadline)submitAttempt(a,snapshot(a),timestamp);};
   const view=a=>{settle(a);const {snapshots,...publicAttempt}=a;return {...publicAttempt,serverNow:timestamp,questions:snapshot(a).map(q=>a.status==='submitted'?enrich(q):publicQuestion(q))};};
   // Closing a tab never extends an exam; settle on the next visit, including history.
   Object.values(state.attempts).forEach(settle);
   let value;
   try {
    const moduleRoute=path.match(/^\/modules\/([^/]+)$/),attemptRoute=path.match(/^\/attempts\/([^/]+)(\/submit)?$/);
    if(path==='/summary'&&method==='GET') {
     value={modules:modules.map(m=>{const qs=questions.filter(q=>q.modules.includes(m.id)),progress=state.practice[m.id]||{};return {...m,questionCount:qs.length,done:qs.filter(q=>progress[q.id]).length,correct:qs.filter(q=>progress[q.id]?.correct).length};}),totalQuestions:questions.length,issues:data.issues||[],history:Object.values(state.attempts).map(a=>({id:a.id,status:a.status,createdAt:a.createdAt,deadline:a.deadline,result:a.result,count:a.questionIds.length})).sort((a,b)=>b.createdAt-a.createdAt)};
    }else if(moduleRoute&&method==='GET') {
     const m=moduleMap.get(moduleRoute[1]);if(!m)throw new Error('Module không tồn tại');
     value={...m,questions:questions.filter(q=>q.modules.includes(m.id)).sort((a,b)=>a.sources.find(s=>s.module===m.id).page-b.sources.find(s=>s.module===m.id).page).map(q=>({...publicQuestion(q),sources:enrich(q).sources})),pages:sources.filter(s=>s.module===m.id),progress:state.practice[m.id]||{}};
    }else if(path==='/practice'&&method==='POST') {
     const q=qmap.get(body.questionId);
     if(!q||!q.modules.includes(body.module)||!q.options.some(o=>o.id===body.answer))throw new Error('Câu hỏi hoặc lựa chọn không hợp lệ');
     const record={answer:body.answer,correct:body.answer===q.correct,updatedAt:timestamp};state.practice[body.module]??={};state.practice[body.module][q.id]=record;
     value={question:enrich(q),record};
    }else if(path==='/attempts'&&method==='POST') {
     if(!Number.isFinite(body.minutes)||body.minutes<1||body.minutes>300)throw new Error('Thời gian phải từ 1 đến 300 phút');
     if(body.modules&&(!Array.isArray(body.modules)||body.modules.some(id=>!moduleMap.has(id))))throw new Error('Module không tồn tại');
     let selected,count=body.count;
     if(body.retry){
      const old=state.attempts[body.retry];if(!old||old.status!=='submitted')throw new Error('Chỉ làm lại được bài đã nộp');
      const wrong=snapshot(old).filter(q=>old.answers[q.id]!==q.correct&&(body.includeBlank||old.answers[q.id]));
      if(!wrong.length)throw new Error('Không có câu sai trong phạm vi đã chọn');
      count=wrong.length;selected=selectExamQuestions(wrong,{},count,uuid());
     }else selected=selectExamQuestions(questions,{modules:body.modules||[]},count,uuid());
     const a={id:uuid(),status:'active',questionIds:selected.map(q=>q.id),snapshots:structuredClone(selected.map(enrich)),answers:{},flags:[],createdAt:timestamp,deadline:timestamp+body.minutes*60000,modules:body.modules||[]};
     state.attempts[a.id]=a;value=view(a);
    }else if(attemptRoute) {
     const a=state.attempts[attemptRoute[1]];if(!a)throw new Error('Không tìm thấy lượt thi trên trình duyệt này');
     if(method==='GET'&&!attemptRoute[2])value=view(a);
     else if(method==='POST'&&attemptRoute[2]){submitAttempt(a,snapshot(a),timestamp);value=view(a);}
     else if(method==='PATCH'&&!attemptRoute[2]) {
      if(a.status!=='active')throw new Error(timestamp>=a.deadline?'Bài đã hết giờ và được tự nộp':'Bài đã nộp');
      if(body.flags&&(!Array.isArray(body.flags)||body.flags.some(id=>!a.questionIds.includes(id))))throw new Error('Cờ đánh dấu không hợp lệ');
      if(body.questionId)applyAnswer(a,snapshot(a),body.questionId,body.answer,timestamp);
      if(body.flags)a.flags=[...new Set(body.flags)];value=view(a);
     }else throw new Error('Thao tác không được hỗ trợ');
    }else throw new Error('Không tìm thấy chức năng này');
    return {state,value:{data:value}};
   }catch(error){return {state,value:{error:error.message||'Không xử lý được yêu cầu'}};}
  });
  if(outcome.error)throw new Error(outcome.error);
  return outcome.data;
 }};
}
