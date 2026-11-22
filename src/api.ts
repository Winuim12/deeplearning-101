import {assetUrl} from './assets';
import {createBrowserStore} from './browser-store';
import {createLocalService} from './local-service.mjs';

const sitePath=new URL(import.meta.env.BASE_URL,document.baseURI).pathname;
const localService=createLocalService({store:createBrowserStore(sitePath),loadData:async()=>{
 try{const response=await fetch(assetUrl('data/study.json'));if(!response.ok)throw new Error('Missing data');return await response.json();}
 catch{throw new Error('Không tải được ngân hàng câu hỏi. Kiểm tra kết nối rồi thử lại.');}
}});

// Kept as an interface so screens share the same behavior in practice and exams.
export function api<T>(path:string,method='GET',data?:unknown):Promise<T>{return localService.request<T>(path,method,data);}
