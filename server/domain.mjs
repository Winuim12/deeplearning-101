export function validateBank(questions, modules) {
 const errors=[], ids=new Set(), map=new Map(modules.map(m=>[m.id,m]));
 for (const q of questions) {
  const fail=message=>errors.push(`${q.id}: ${message}`);
  if(!q.id||ids.has(q.id)) fail('ID thiếu hoặc trùng'); ids.add(q.id);
  if(!q.prompt||!q.explanation) fail('Thiếu đề hoặc lời giải');
  if(q.options?.length!==4 || new Set(q.options?.map(o=>o.id)).size!==4 || new Set(q.options?.map(o=>o.text)).size!==4) fail('Cần 4 lựa chọn phân biệt');
  if(!q.options?.some(o=>o.id===q.correct)) fail('Đáp án không thuộc lựa chọn');
  if(q.options?.some(o=>!o.explanation)) fail('Thiếu lý do cho lựa chọn');
  if(!q.modules?.length||q.modules.some(id=>!map.has(id))) fail('Module không tồn tại');
  if(!q.sources?.length) fail('Thiếu nguồn');
  for(const s of q.sources||[]) if(!map.has(s.module)||!Number.isInteger(s.page)||s.page<1||s.page>map.get(s.module).pages||!s.region) fail('Nguồn/trang/vùng xem lại không hợp lệ');
 }
 return errors;
}
export function selectExamQuestions(questions,filters={},count=50,seed=String(Date.now())) {
 if(!Number.isInteger(count)||count<1||count>200) throw new Error('Số câu phải từ 1 đến 200');
 let state=2166136261;for(const c of String(seed)){state^=c.charCodeAt(0);state=Math.imul(state,16777619);}
 const random=()=>{state+=0x6D2B79F5;let t=Math.imul(state^state>>>15,1|state);t^=t+Math.imul(t^t>>>7,61|t);return((t^t>>>14)>>>0)/4294967296;};
 const eligible=[...new Map(questions.filter(q=>q.status==='ready'&&(!filters.modules?.length||q.modules.some(id=>filters.modules.includes(id)))&&(!filters.ids||filters.ids.includes(q.id))).map(q=>[q.id,q])).values()];
 if(eligible.length<count) throw new Error(`Chỉ có ${eligible.length} câu hợp lệ trong phạm vi đã chọn; cần ${count} câu.`);
 // Shuffle each concept, then round-robin concepts and modules to reduce near-duplicate concentration.
 const shuffled=eligible.map(q=>({q,r:random()})).sort((a,b)=>a.r-b.r).map(x=>x.q);
 const groups=new Map();for(const q of shuffled){const key=q.concept||q.id;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(q);}
 const result=[];while(result.length<count){for(const group of groups.values()){if(group.length)result.push(group.shift());if(result.length===count)break;}}
 return result;
}
export function gradeAttempt(questions,answers) {
 let correct=0,wrong=0,blank=0;
 for(const q of questions){if(!answers[q.id])blank++;else if(answers[q.id]===q.correct)correct++;else wrong++;}
 const total=questions.length;return {correct,wrong,blank,total,percent:total?Math.round(correct/total*10000)/100:0,score:total?Math.round(correct/total*1000)/100:0};
}
export function publicQuestion(q) {
 return {id:q.id,prompt:q.prompt,options:q.options.map(({id,text})=>({id,text})),image:q.image,imageAlt:q.imageAlt,type:q.type};
}
export function applyAnswer(attempt,questions,id,choice,now=Date.now()) {
 if(attempt.status!=='active')throw new Error('Bài đã nộp');
 if(now>=attempt.deadline)throw new Error('Bài đã hết giờ');
 const q=questions.find(q=>q.id===id&&attempt.questionIds.includes(id));
 if(!q||!q.options.some(o=>o.id===choice))throw new Error('Câu hỏi hoặc lựa chọn không hợp lệ');
 attempt.answers[id]=choice;return attempt;
}
export function submitAttempt(attempt,questions,now=Date.now()) {
 if(attempt.status!=='active')return attempt;
 attempt.status='submitted';attempt.submittedAt=now;
 attempt.result=gradeAttempt(attempt.questionIds.map(id=>questions.find(q=>q.id===id)),attempt.answers);return attempt;
}
export function migrateOptionIds(state,questions) {
 if(state.optionIdsVersion===2)return state;
 const map=new Map(questions.map(q=>[q.id,q]));
 for(const records of Object.values(state.practice||{}))for(const [id,r] of Object.entries(records)){const q=map.get(id);if(q){r.answer=q.legacyOptionMap?.[r.answer]||r.answer;r.correct=r.answer===q.correct;}}
 for(const a of Object.values(state.attempts||{})){
  for(const [id,choice] of Object.entries(a.answers)){const q=map.get(id);if(q)a.answers[id]=q.legacyOptionMap?.[choice]||choice;}
  if(a.status==='submitted'&&a.questionIds.every(id=>map.has(id)))a.result=gradeAttempt(a.questionIds.map(id=>map.get(id)),a.answers);
 }
 state.optionIdsVersion=2;return state;
}
