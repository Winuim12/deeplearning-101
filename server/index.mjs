import http from 'node:http';
import {readFileSync,writeFileSync,renameSync,mkdirSync,existsSync,statSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomUUID} from 'node:crypto';
import {selectExamQuestions,gradeAttempt,publicQuestion,applyAnswer,submitAttempt,validateBank,migrateOptionIds} from './domain.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=name=>JSON.parse(readFileSync(path.join(root,'content',name),'utf8'));
const modules=read('modules.json'), sources=read('sources.json');
const questions=read('bank.json');
const errors=validateBank(questions,modules);if(errors.length)throw new Error(errors.join('\n'));
const qmap=new Map(questions.map(q=>[q.id,q]));
const dataDir=process.env.DL_DATA_DIR||path.join(root,'.local');mkdirSync(dataDir,{recursive:true});
const statePath=path.join(dataDir,'state.json');
let state={version:1,optionIdsVersion:2,practice:{},attempts:{}};
if(existsSync(statePath)) {state=JSON.parse(readFileSync(statePath,'utf8'));if(state.version!==1)throw new Error('Phiên bản dữ liệu tiến độ không được hỗ trợ; giữ nguyên file để khôi phục.');}
const save=()=>{const temp=statePath+'.tmp';writeFileSync(temp,JSON.stringify(state));renameSync(temp,statePath);};
if(state.optionIdsVersion!==2){migrateOptionIds(state,questions);save();}
const send=(res,status,data)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
const summary=()=>({modules:modules.map(m=>{const qs=questions.filter(q=>q.status==='ready'&&q.modules.includes(m.id));const records=state.practice[m.id]||{};return {...m,questionCount:qs.length,done:qs.filter(q=>records[q.id]).length,correct:qs.filter(q=>records[q.id]?.correct).length};}),totalQuestions:questions.filter(q=>q.status==='ready').length,history:Object.values(state.attempts).map(a=>({id:a.id,status:a.status,createdAt:a.createdAt,deadline:a.deadline,result:a.result,count:a.questionIds.length})).sort((a,b)=>b.createdAt-a.createdAt),issues:read('issues.json')});
const enrich=q=>({...q,sources:q.sources.map(s=>({...sources.find(x=>x.module===s.module&&x.page===s.page),...s,file:modules.find(m=>m.id===s.module).file,pdf:'/slides/'+encodeURIComponent(modules.find(m=>m.id===s.module).file)+'#page='+s.page}))});
function attemptView(a) {
 if(a.status==='active'&&Date.now()>=a.deadline){submitAttempt(a,questions);save();}
 return {...a,serverNow:Date.now(),questions:a.questionIds.map(id=>a.status==='submitted'?enrich(qmap.get(id)):publicQuestion(qmap.get(id)))};
}
async function body(req){let data='';for await(const c of req){data+=c;if(data.length>200000)throw new Error('Yêu cầu quá lớn');}return data?JSON.parse(data):{};}
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.pdf':'application/pdf','.woff2':'font/woff2','.woff':'font/woff'};
function file(res,p){if(!existsSync(p)||!statSync(p).isFile())return send(res,404,{error:'Không tìm thấy tài liệu/hình. Chạy npm run prepare:slides để chuẩn bị nguồn.'});res.writeHead(200,{'Content-Type':mime[path.extname(p)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Cache-Control':'public, max-age=3600'});res.end(readFileSync(p));}
const server=http.createServer(async(req,res)=>{
 try {
  const url=new URL(req.url,'http://127.0.0.1');const route=url.pathname;
  if(req.method!=='GET'&&req.headers.origin&&!['http://localhost:5173','http://127.0.0.1:5173',`http://localhost:${port}`,`http://127.0.0.1:${port}`].includes(req.headers.origin))return send(res,403,{error:'Nguồn yêu cầu không hợp lệ'});
  if(route==='/api/summary'&&req.method==='GET')return send(res,200,summary());
  const mod=route.match(/^\/api\/modules\/([^/]+)$/);
  if(mod&&req.method==='GET'){
   const m=modules.find(m=>m.id===mod[1]);if(!m)return send(res,404,{error:'Module không tồn tại'});
   return send(res,200,{...m,questions:questions.filter(q=>q.status==='ready'&&q.modules.includes(m.id)).sort((a,b)=>a.sources.find(s=>s.module===m.id).page-b.sources.find(s=>s.module===m.id).page).map(q=>({...publicQuestion(q),sources:enrich(q).sources})),pages:sources.filter(s=>s.module===m.id),progress:state.practice[m.id]||{}});
  }
  if(route==='/api/practice'&&req.method==='POST'){
   const b=await body(req);const q=qmap.get(b.questionId);
   if(!q||q.status!=='ready'||!q.modules.includes(b.module)||!q.options.some(o=>o.id===b.answer))return send(res,400,{error:'Câu hỏi hoặc đáp án không hợp lệ'});
   state.practice[b.module]??={};const record={answer:b.answer,correct:b.answer===q.correct,updatedAt:Date.now()};state.practice[b.module][q.id]=record;save();return send(res,200,{question:enrich(q),record});
  }
  if(route==='/api/attempts'&&req.method==='POST'){
   const b=await body(req);if(!Number.isFinite(b.minutes)||b.minutes<1||b.minutes>300)return send(res,400,{error:'Thời gian phải từ 1 đến 300 phút'});
   if(b.modules&&!Array.isArray(b.modules))return send(res,400,{error:'Danh sách module không hợp lệ'});
   if(b.modules?.some(id=>!modules.some(m=>m.id===id)))return send(res,400,{error:'Module không tồn tại'});
   let filters={modules:b.modules||[]};
   if(b.retry){const old=state.attempts[b.retry];if(!old||old.status!=='submitted')return send(res,400,{error:'Chỉ làm lại được bài đã nộp'});filters.ids=old.questionIds.filter(id=>old.answers[id]!==qmap.get(id).correct&&(b.includeBlank||old.answers[id]));if(!filters.ids.length)return send(res,400,{error:'Không có câu sai trong phạm vi đã chọn'});b.count=filters.ids.length;}
   const selected=selectExamQuestions(questions,filters,b.count,randomUUID());const now=Date.now();
   const a={id:randomUUID(),status:'active',questionIds:selected.map(q=>q.id),answers:{},flags:[],createdAt:now,deadline:now+b.minutes*60000,modules:filters.modules};state.attempts[a.id]=a;save();return send(res,201,attemptView(a));
  }
  const match=route.match(/^\/api\/attempts\/([^/]+)(\/submit)?$/);
  if(match){const a=state.attempts[match[1]];if(!a)return send(res,404,{error:'Không tìm thấy lượt thi'});
   if(req.method==='GET'&&!match[2])return send(res,200,attemptView(a));
   if(req.method==='POST'&&match[2]){submitAttempt(a,questions);save();return send(res,200,attemptView(a));}
   if(req.method==='PATCH'&&!match[2]){
    const b=await body(req);if(Date.now()>=a.deadline){submitAttempt(a,questions);save();return send(res,409,{error:'Bài đã hết giờ và được tự nộp',attempt:attemptView(a)});}
    if(a.status!=='active')return send(res,409,{error:'Bài đã nộp',attempt:attemptView(a)});
    if(b.questionId)applyAnswer(a,questions,b.questionId,b.answer);
    if(b.flags){if(!Array.isArray(b.flags)||b.flags.some(id=>!a.questionIds.includes(id)))return send(res,400,{error:'Cờ đánh dấu không hợp lệ'});a.flags=[...new Set(b.flags)];}
    save();return send(res,200,attemptView(a));
   }
  }
  const img=route.match(/^\/api\/pages\/(m\d+-\d+)\/(\d+)\.webp$/);
  if(img&&req.method==='GET'){const m=modules.find(m=>m.id===img[1]);if(!m||+img[2]<1||+img[2]>m.pages)return send(res,404,{error:'Trang không tồn tại'});return file(res,path.join(root,'public','assets','sources',img[1],img[2]+'.webp'));}
  if(route.startsWith('/slides/')&&req.method==='GET'){const name=decodeURIComponent(route.slice(8));const m=modules.find(m=>m.file===name);if(!m)return send(res,404,{error:'Tài liệu không tồn tại'});return file(res,path.join(root,m.path));}
  if(route.startsWith('/assets/')&&req.method==='GET'){const p=path.resolve(root,'public','.'+decodeURIComponent(route));if(!p.startsWith(path.join(root,'public')+path.sep))return send(res,403,{error:'Đường dẫn không hợp lệ'});return file(res,existsSync(p)?p:path.resolve(root,'dist','.'+decodeURIComponent(route)));}
  if(route.startsWith('/api/'))return send(res,404,{error:'API không tồn tại'});
  const p=path.resolve(root,'dist','.'+decodeURIComponent(route));const dist=path.join(root,'dist');if(!p.startsWith(dist+path.sep)&&p!==dist)return send(res,403,{error:'Đường dẫn không hợp lệ'});
  return file(res,existsSync(p)&&statSync(p).isFile()?p:path.join(dist,'index.html'));
 }catch(e){send(res,400,{error:e.message||'Không xử lý được yêu cầu'});}
});
const port=Number(process.env.PORT||4173);server.listen(port,'127.0.0.1',()=>console.log(`Deep Learning API/local: http://127.0.0.1:${port}`));
