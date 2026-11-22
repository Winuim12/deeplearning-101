import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createLocalService} from '../src/local-service.mjs';
import {withBase} from '../src/paths.mjs';

const read=name=>JSON.parse(readFileSync('content/'+name+'.json','utf8'));
const data={version:1,bank:read('bank'),modules:read('modules'),sources:read('sources'),issues:read('issues')};
class MemoryStore {
 state; queue=Promise.resolve();fail=false;
 update(fn){const op=this.queue.then(()=>{if(this.fail)throw new Error('Không lưu được tiến độ');const draft=structuredClone(this.state);const r=fn(draft);this.state=structuredClone(r.state);return structuredClone(r.value);});this.queue=op.catch(()=>{});return op;}
}
function fixture(){const store=new MemoryStore();let time=100000,sequence=0;const options={loadData:async()=>structuredClone(data),store,now:()=>time,uuid:()=>`attempt-${++sequence}`};return {store,options,service:createLocalService(options),time:value=>{time=value;}};}

test('deadline uses transaction execution time after a queued write',async()=>{
 const f=fixture(),a=await f.service.request('/attempts','POST',{count:2,minutes:1});
 f.time(a.deadline-1);const update=f.store.update.bind(f.store);
 f.store.update=change=>{f.time(a.deadline+1000);return update(change);};
 await assert.rejects(f.service.request('/attempts/'+a.id,'PATCH',{questionId:a.questions[0].id,answer:'a'}),/hết giờ|nộp/);
 assert.equal(f.store.state.attempts[a.id].status,'submitted');assert.equal(f.store.state.attempts[a.id].result.blank,2);
});
test('asset paths preserve repo subpaths and PDF fragments',()=>{
 assert.equal(withBase('/assets/questions/masks.svg','/DeepLearning-101/'),'/DeepLearning-101/assets/questions/masks.svg');
 assert.equal(withBase('slides/a.pdf#page=53','./'),'./slides/a.pdf#page=53');
 assert.equal(withBase('/repo/assets/a.webp','/repo/'),'/repo/assets/a.webp');
 assert.equal(withBase('https://example.com/a.pdf','/repo/'),'https://example.com/a.pdf');
});
test('practice progress survives a new service instance; sources are static assets',async()=>{
 const f=fixture();const m=await f.service.request('/modules/m3-2');const q=m.questions[0];
 assert.equal(q.correct,undefined);assert.equal(q.options[0].explanation,undefined);
 await f.service.request('/practice','POST',{module:'m3-2',questionId:q.id,answer:q.options[0].id});
 const restored=await createLocalService(f.options).request('/modules/m3-2');assert.equal(restored.progress[q.id].answer,q.options[0].id);
 assert.match(restored.questions[0].sources[0].image,/assets\/sources\//);assert.match(restored.questions[0].sources[0].pdf,/slides\/.*#page=/);
});
test('50 unique questions, hidden solutions, persisted deadline and flags',async()=>{
 const f=fixture(),a=await f.service.request('/attempts','POST',{count:50,minutes:60});
 assert.equal(new Set(a.questionIds).size,50);assert.equal(a.questions[0].correct,undefined);assert.equal(a.questions[0].sources,undefined);
 const q=a.questions[0];await f.service.request('/attempts/'+a.id,'PATCH',{questionId:q.id,answer:q.options[0].id});
 await f.service.request('/attempts/'+a.id,'PATCH',{flags:[q.id]});
 const again=await createLocalService(f.options).request('/attempts/'+a.id);assert.equal(again.deadline,a.deadline);assert.equal(again.answers[q.id],q.options[0].id);assert.deepEqual(again.flags,[q.id]);
});
test('expiration on reopen auto-submits and rejects late changes',async()=>{
 const f=fixture(),a=await f.service.request('/attempts','POST',{count:2,minutes:1});f.time(a.deadline+1);
 await assert.rejects(f.service.request('/attempts/'+a.id,'PATCH',{questionId:a.questions[0].id,answer:'a'}),/hết giờ|nộp/);
 const done=await f.service.request('/attempts/'+a.id);assert.equal(done.status,'submitted');assert.equal(done.result.blank,2);
 assert.deepEqual(await f.service.request('/attempts/'+a.id+'/submit','POST'),done);
});
test('grading uses snapshots and retry contains exactly wrong/blank IDs',async()=>{
 const f=fixture(),a=await f.service.request('/attempts','POST',{count:3,minutes:1});const q=data.bank.find(q=>q.id===a.questionIds[0]);
 await f.service.request('/attempts/'+a.id,'PATCH',{questionId:q.id,answer:q.correct});
 const done=await f.service.request('/attempts/'+a.id+'/submit','POST');assert.equal(done.result.correct,1);assert.equal(done.result.blank,2);
 const retry=await f.service.request('/attempts','POST',{retry:a.id,includeBlank:true,minutes:1});assert.equal(retry.questionIds.length,2);assert.ok(!retry.questionIds.includes(q.id));
 await assert.rejects(f.service.request('/attempts','POST',{retry:a.id,includeBlank:false,minutes:1}),/Không có câu sai/);
 // Stored snapshots remain authoritative even after the question disappears from a new bank.
 const changed=createLocalService({...f.options,loadData:async()=>({...structuredClone(data),bank:[]})});
 assert.equal((await changed.request('/attempts/'+a.id)).result.correct,1);
});
test('insufficient pools, invalid selections and failed persistence report errors',async()=>{
 const f=fixture();await assert.rejects(f.service.request('/attempts','POST',{count:50,minutes:1,modules:['m2-3']}),/Chỉ có/);
 await assert.rejects(f.service.request('/attempts','POST',{count:5,minutes:1,modules:['missing']}),/Module/);
 const a=await f.service.request('/attempts','POST',{count:1,minutes:1});f.store.fail=true;
 await assert.rejects(f.service.request('/attempts/'+a.id,'PATCH',{questionId:a.questionIds[0],answer:'a'}),/Không lưu/);
 f.store.fail=false;assert.deepEqual((await f.service.request('/attempts/'+a.id)).answers,{});
});
test('concurrent requests preserve both answers; invalid flags cannot half-save an answer',async()=>{
 const f=fixture(),a=await f.service.request('/attempts','POST',{count:2,minutes:1});
 await Promise.all(a.questions.map(q=>f.service.request('/attempts/'+a.id,'PATCH',{questionId:q.id,answer:q.options[0].id})));
 assert.equal(Object.keys((await f.service.request('/attempts/'+a.id)).answers).length,2);
 const b=await f.service.request('/attempts','POST',{count:1,minutes:1});
 await assert.rejects(f.service.request('/attempts/'+b.id,'PATCH',{questionId:b.questionIds[0],answer:'a',flags:['not-in-exam']}),/đánh dấu/);
 assert.deepEqual((await f.service.request('/attempts/'+b.id)).answers,{});
});
