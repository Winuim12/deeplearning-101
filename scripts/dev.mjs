import {spawn} from 'node:child_process';
const children=[spawn(process.execPath,['server/index.mjs'],{stdio:'inherit'}),spawn(process.execPath,['node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5173','--strictPort'],{stdio:'inherit'})];
let closing=false;const close=()=>{if(closing)return;closing=true;children.forEach(c=>c.kill());};
for(const c of children){c.on('error',e=>{console.error(e);close();process.exitCode=1;});c.on('exit',code=>{if(!closing){process.exitCode=code||0;close();}});}
process.on('SIGINT',close);process.on('SIGTERM',close);
