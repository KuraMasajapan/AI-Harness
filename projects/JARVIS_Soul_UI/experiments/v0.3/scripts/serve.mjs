// Local-only, no-cache static server for repeatable shader iteration.
import {createServer} from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve,sep,extname} from 'node:path';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json','.jpg':'image/jpeg','.webp':'image/webp','.mp4':'video/mp4','.md':'text/plain; charset=utf-8'};
const port=Number(process.env.SOUL_PORT||8034);
createServer(async(req,res)=>{
  res.setHeader('Cache-Control','no-store');
  try{
    const pathname=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
    let path=resolve(root,'.'+pathname);
    if(path!==resolve(root)&&!path.startsWith(resolve(root)+sep)){res.writeHead(403).end();return;}
    if((await stat(path)).isDirectory())path=resolve(path,'index.html');
    const bytes=await readFile(path);
    res.writeHead(200,{'Content-Type':types[extname(path)]||'application/octet-stream','Content-Length':bytes.length});
    res.end(req.method==='HEAD'?undefined:bytes);
  }catch{res.writeHead(404).end('Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`Soul research: http://127.0.0.1:${port}/experiments/v0.3/`));
