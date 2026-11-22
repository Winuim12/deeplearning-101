import {withBase} from './paths.mjs';
export const assetUrl=(path:string)=>withBase(path,import.meta.env.BASE_URL);
