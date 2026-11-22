import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';import {createHash} from 'node:crypto';
import {exportStatic} from '../scripts/export-static.mjs';
test('static export contains public bank, source images and unchanged PDFs, without user history',()=>{
 const result=exportStatic();assert.equal(result.modules,36);assert.equal(result.questions,356);
 const data=JSON.parse(readFileSync('public/data/study.json','utf8'));
 assert.equal(data.practice,undefined);assert.equal(data.attempts,undefined);assert.equal(data.bank[0].legacyOptionMap,undefined);
 for(const m of data.modules){
  assert.ok(existsSync('public/slides/'+m.file));
  assert.equal(createHash('sha256').update(readFileSync('public/slides/'+m.file)).digest('hex'),m.sha256);
 }
 for(const s of data.sources){assert.ok(!s.image.startsWith('/api/'));assert.ok(existsSync('public/'+s.image));}
});
