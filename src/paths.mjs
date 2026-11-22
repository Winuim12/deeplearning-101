/** A single mapping for both root deployments and GitHub project subpaths. */
export function withBase(value, base='./') {
 if(!value || /^(?:https?:|data:|blob:|#)/i.test(value))return value;
 const prefix=base.endsWith('/')?base:base+'/';
 if(prefix.startsWith('/')&&value.startsWith(prefix))return value;
 return prefix+value.replace(/^(?:\.\/|\/)+/,'');
}
