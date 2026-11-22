import {chromium} from '@playwright/test';
import {mkdirSync} from 'node:fs';
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1500,height:1000}});mkdirSync('reports/screenshots',{recursive:true});
const base=process.env.CAPTURE_URL||'http://127.0.0.1:5173';
const errors=[];page.on('pageerror',e=>errors.push(e.message));
for(const [name,url] of [['library','/'],['study','/#/module/m3-2'],['exam-setup','/#/exam']]){
 await page.goto(base+url);await page.waitForLoadState('networkidle');await page.screenshot({path:`reports/screenshots/${name}.png`,fullPage:name!=='library'});
}
await page.setViewportSize({width:390,height:844});await page.goto(base+'/');await page.waitForLoadState('networkidle');await page.screenshot({path:'reports/screenshots/mobile.png'});
console.log(JSON.stringify({screenshots:4,consoleErrors:errors}));await browser.close();
