import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
const bank=JSON.parse(readFileSync('content/bank.json','utf8'));
test('public choice ID does not universally identify the answer',()=>{
 assert.ok(new Set(bank.map(q=>q.correct)).size>=4,'All answers share a public marker ID');
 assert.ok(bank.every(q=>q.options.every(o=>['a','b','c','d'].includes(o.id))));
});
test('shared-note citations point at the actual definitions',()=>{
 const self=bank.find(q=>q.concept==='self-cross-sources');assert.equal(self.sources.find(s=>s.module==='m5-7').page,9);
 const ema=bank.find(q=>q.concept==='ema-teacher');assert.equal(ema.sources.find(s=>s.module==='m6-2').page,7);
});
test('DINO family question does not show a diagram naming its answer',()=>{
 assert.equal(bank.find(q=>q.concept==='dino-distill').image,undefined);
});
