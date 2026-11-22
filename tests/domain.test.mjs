import test from 'node:test';
import assert from 'node:assert/strict';
import { validateBank, selectExamQuestions, gradeAttempt, publicQuestion, applyAnswer, submitAttempt, migrateOptionIds } from '../server/domain.mjs';

const makeQ = (i, modules = ['m1']) => ({id:`q${i}`, concept:`c${i}`, modules, status:'ready', prompt:`Câu ${i}`, options:['a','b','c','d'].map(id=>({id,text:id,explanation:`Lý do ${id}`})), correct:'b', explanation:'Giải thích', sources:[{module:'m1',page:1,region:'Công thức'}]});
const questions=Array.from({length:60},(_,i)=>makeQ(i));
const modules=[{id:'m1',pages:3}];
test('validator rejects ambiguous answers, missing sources and page overflow',()=>{
 assert.deepEqual(validateBank(questions,modules),[]);
 const bad=structuredClone(questions[0]); bad.correct='z'; bad.sources[0].page=4;
 assert.ok(validateBank([bad],modules).length>=2);
 assert.ok(validateBank([{...questions[0],sources:[]}],modules).length);
 assert.ok(validateBank([questions[0],questions[0]],modules).length);
});
test('50 unique ready questions; shared modules do not duplicate a question',()=>{
 const shared=questions.map(q=>({...q,modules:['m1','m2']}));
 const selected=selectExamQuestions(shared,{modules:['m1','m2']},50,'repeatable');
 assert.equal(selected.length,50);assert.equal(new Set(selected.map(q=>q.id)).size,50);
 assert.deepEqual(selected,selectExamQuestions(shared,{modules:['m1','m2']},50,'repeatable'));
 assert.notDeepEqual(selected,selectExamQuestions(shared,{},50,'another'));
 assert.throws(()=>selectExamQuestions(questions.slice(0,49),{},50,'x'),/49/);
 assert.throws(()=>selectExamQuestions(questions.map(q=>({...q,status:'draft'})),{},50,'x'),/0/);
});
test('grade includes blank answers and stable option IDs',()=>{
 const result=gradeAttempt(questions.slice(0,4),{q0:'b',q1:'a',q2:'b'});
 assert.deepEqual(result,{correct:2,wrong:1,blank:1,total:4,percent:50,score:5});
 assert.equal(gradeAttempt([questions[0]],{q0:'b'}).score,10);
 assert.equal(gradeAttempt([questions[0]],{}).blank,1);
});
test('public exam questions contain no key, sources or option rationale',()=>{
 const q=publicQuestion(questions[0]); assert.equal(q.correct,undefined);assert.equal(q.sources,undefined);assert.equal(q.explanation,undefined);assert.equal(q.options[0].explanation,undefined);
});
test('expired attempts reject answer changes and submit exactly once',()=>{
 const attempt={id:'t',questionIds:['q0'],answers:{},flags:[],deadline:1000,status:'active'};
 assert.throws(()=>applyAnswer(attempt,questions,'q0','b',1000),/hết giờ/);
 assert.throws(()=>applyAnswer(attempt,questions,'q0','z',100),/lựa chọn/);
 applyAnswer(attempt,questions,'q0','b',900); submitAttempt(attempt,questions,1001);
 assert.equal(attempt.result.correct,1); const first=JSON.stringify(attempt);
 submitAttempt(attempt,questions,2000);assert.equal(JSON.stringify(attempt),first);
 assert.throws(()=>applyAnswer(attempt,questions,'q0','a',2000),/nộp/);
});
test('old answer IDs migrate without changing correctness or resetting progress',()=>{
 const q={...makeQ(0),correct:'c',legacyOptionMap:{o0:'c',o1:'a',o2:'d',o3:'b'}};
 const state={version:1,practice:{m1:{q0:{answer:'o0',correct:true}}},attempts:{t:{status:'submitted',questionIds:['q0'],answers:{q0:'o0'}}}};
 migrateOptionIds(state,[q]);assert.equal(state.practice.m1.q0.answer,'c');assert.equal(state.practice.m1.q0.correct,true);assert.equal(state.attempts.t.result.correct,1);
 const once=JSON.stringify(state);migrateOptionIds(state,[q]);assert.equal(JSON.stringify(state),once);
});
