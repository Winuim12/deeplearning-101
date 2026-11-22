import {mkdirSync,readFileSync,writeFileSync,copyFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export function exportStatic(){
 const read=name=>JSON.parse(readFileSync(path.join(root,'content',name+'.json'),'utf8'));
 const modules=read('modules'),bank=read('bank').filter(q=>q.status==='ready').map(({legacyOptionMap,...q})=>q);
 const filenames=new Set();
 mkdirSync(path.join(root,'public/data'),{recursive:true});mkdirSync(path.join(root,'public/slides'),{recursive:true});
 for(const m of modules){
  if(path.basename(m.file)!==m.file||filenames.has(m.file))throw new Error(`Tên PDF trùng/không hợp lệ: ${m.file}`);filenames.add(m.file);
  const source=path.join(root,m.path),digest=createHash('sha256').update(readFileSync(source)).digest('hex');
  if(digest!==m.sha256)throw new Error(`PDF gốc đã thay đổi, cần rà lại nguồn trước khi deploy: ${m.file}`);
  copyFileSync(source,path.join(root,'public/slides',m.file));
 }
 const sources=read('sources').map(s=>({...s,image:`assets/sources/${s.module}/${s.page}.webp`}));
 for(const s of sources)if(!existsSync(path.join(root,'public',s.image)))throw new Error(`Thiếu ảnh nguồn ${s.image}`);
 const data={version:1,modules,bank,sources,issues:read('issues')};
 writeFileSync(path.join(root,'public/data/study.json'),JSON.stringify(data));
 writeFileSync(path.join(root,'public/.nojekyll'),'');
 const result={modules:modules.length,questions:bank.length,pages:sources.length};return result;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))console.log('Static export:',JSON.stringify(exportStatic()));
