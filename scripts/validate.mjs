import {readFileSync,existsSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {validateBank} from '../server/domain.mjs';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const bank=read('content/bank.json'),modules=read('content/modules.json'),sources=read('content/sources.json');
const errors=validateBank(bank,modules);let sourceImages=0;
for(const m of modules){
 const hash=createHash('sha256').update(readFileSync(m.path)).digest('hex');if(hash!==m.sha256)errors.push(`File gốc đã thay đổi: ${m.file}`);
 if(!bank.some(q=>q.modules.includes(m.id)))errors.push(`Module chưa có câu hỏi: ${m.id}`);
 if(m.questionCount!==bank.filter(q=>q.modules.includes(m.id)).length)errors.push(`Sai module count: ${m.id}`);
 for(let p=1;p<=m.pages;p++){if(!existsSync(`public/assets/sources/${m.id}/${p}.webp`))errors.push(`Thiếu ảnh nguồn ${m.id}/${p}`);else sourceImages++;}
 const raw=read(`content/pages/${m.id}.json`);if(raw.length!==m.pages)errors.push(`Sai số trang ${m.id}`);
}
for(const q of bank){
 for(const s of q.sources)if(!sources.some(x=>x.module===s.module&&x.page===s.page))errors.push(`Nguồn không tồn tại ${q.id}`);
 if(q.image&&!existsSync('public'+q.image))errors.push(`Thiếu hình ${q.image}`);
 for(const id of q.modules)if(!q.sources.some(s=>s.module===id))errors.push(`Thiếu trang riêng cho module liên kết ${q.id}/${id}`);
}
const report={checkedAt:new Date().toISOString(),modules:modules.length,uniqueQuestions:bank.length,moduleLinks:modules.reduce((a,m)=>a+m.questionCount,0),sourceImages,illustratedQuestions:bank.filter(q=>q.image).length,questionSourcePages:new Set(bank.flatMap(q=>q.sources.map(s=>s.module+':'+s.page))).size,types:Object.fromEntries(['concept','calculation','visual'].map(t=>[t,bank.filter(q=>q.type===t).length])),originalHashesUnchanged:!errors.some(e=>e.includes('File gốc')),errors};
mkdirSync('reports',{recursive:true});writeFileSync('reports/validation.json',JSON.stringify(report,null,2));
writeFileSync('reports/module-counts.md','# Số câu hiện có theo module\n\n| File | Trang | Câu liên kết |\n|---|---:|---:|\n'+modules.map(m=>`| ${m.file} | ${m.pages} | ${m.questionCount} |`).join('\n')+'\n\nCâu dùng chung có cùng ID: tổng liên kết module có thể lớn hơn số câu unique. Xem `content/coverage.json` để phân biệt trang có câu hỏi và trang còn cần rà sâu.\n');
console.log(JSON.stringify(report,null,2));if(errors.length)process.exitCode=1;
