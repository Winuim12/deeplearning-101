/** Test/preview only: serves dist under a repo subpath, with no API or SPA fallback. */
import http from 'node:http';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {readFileSync,statSync,existsSync} from 'node:fs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../dist');
const prefix='/'+(process.env.STATIC_PREFIX||'pages-proof').replace(/^\/+|\/+$/g,'')+'/';
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.pdf':'application/pdf','.woff2':'font/woff2','.woff':'font/woff'};
http.createServer((req,res)=>{
 try{
  const url=new URL(req.url,'http://localhost');if(url.pathname===prefix.slice(0,-1)){res.writeHead(301,{Location:prefix});return res.end();}
  if(!url.pathname.startsWith(prefix)){res.writeHead(404);return res.end('Not found');}
  const relative=decodeURIComponent(url.pathname.slice(prefix.length))||'index.html';
  const file=path.resolve(root,relative);if(!file.startsWith(root+path.sep)||!existsSync(file)||!statSync(file).isFile()){res.writeHead(404);return res.end('Not found');}
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(readFileSync(file));
 }catch{res.writeHead(400);res.end('Bad request');}
}).listen(Number(process.env.PORT||4188),'127.0.0.1',()=>console.log(`Static preview: http://127.0.0.1:${process.env.PORT||4188}${prefix}`));
