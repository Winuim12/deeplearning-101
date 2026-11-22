type Change<T>=(state:unknown)=>{state:unknown;value:T};

/** Native IDB transactions serialize updates across tabs without storing private data in Git. */
export function createBrowserStore(sitePath:string){
 let connection:Promise<IDBDatabase>|undefined;
 const open=()=>connection??=new Promise<IDBDatabase>((resolve,reject)=>{
  if(!globalThis.indexedDB){reject(new Error('Trình duyệt đang chặn lưu tiến độ. Hãy cho phép lưu dữ liệu website rồi thử lại.'));return;}
  const request=indexedDB.open('deep-learning-study-room:'+sitePath,1);
  request.onupgradeneeded=()=>request.result.createObjectStore('progress');
  request.onsuccess=()=>{const db=request.result;db.onversionchange=()=>{db.close();connection=undefined;};resolve(db);};
  request.onerror=()=>{connection=undefined;reject(new Error('Không mở được dữ liệu tiến độ. Hãy cho phép lưu dữ liệu website rồi thử lại.'));};
  request.onblocked=()=>{connection=undefined;reject(new Error('Hãy đóng các tab phòng học khác rồi tải lại trang.'));};
 });
 return {async update<T>(change:Change<T>):Promise<T>{
  const db=await open();return new Promise<T>((resolve,reject)=>{
   const tx=db.transaction('progress','readwrite'),table=tx.objectStore('progress');let value:T;let mutationError:unknown;
   tx.oncomplete=()=>resolve(value);
   tx.onerror=tx.onabort=()=>reject(mutationError||new Error('Không lưu được tiến độ. Kiểm tra dung lượng/quyền lưu của trình duyệt rồi thử lại.'));
   const request=table.get('main');request.onsuccess=()=>{
    try{const next=change(request.result);value=next.value;table.put(next.state,'main');}
    catch(error){mutationError=error;tx.abort();}
   };
  });
 }};
}
