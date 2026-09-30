import { parseCompletion, onRequestPost } from '../main-app/functions/api/magnet-chat.js';
import assert from 'node:assert';
// --- parse tests
const P=parseCompletion;
assert.equal(P(true,200,{choices:[{message:{content:'hi '}}]}).text,'hi');
assert.equal(P(true,200,{choices:[{message:{content:[{type:'text',text:'a'},{type:'text',text:'b'}]}}]}).text,'ab');
assert.match(P(true,200,{choices:[{message:{content:''},finish_reason:'length'}]}).error,/empty content.*length/);
assert.match(P(true,200,{choices:[{message:{content:null,reasoning:'thinking...'}}]}).error,/empty/);
assert.match(P(true,200,{choices:[]}).error,/no choices/);
assert.match(P(true,200,{error:{message:'boom'}}).error,/boom/);
assert.match(P(false,402,{error:{message:'Insufficient credits'}}).error,/credits/);
assert.match(P(false,502,null).error,/502/);
console.log('parse ok');

// --- handler tests with mocked fetch
const tg=[]; let orCalls=[]; let mode;
globalThis.fetch=async(url,opts)=>{
  if(String(url).includes('telegram.org')){tg.push([String(url).split('/').pop(), typeof opts.body==='string'?JSON.parse(opts.body).text:'(form)']);return new Response('{}');}
  const b=JSON.parse(opts.body); orCalls.push(b.model);
  const m=mode(b.model, b);
  if(m==='throw') throw new Error('net');
  if(m==='hang') return new Promise((_,rej)=>opts.signal.addEventListener('abort',()=>{const e=new Error('a');e.name='AbortError';rej(e)}));
  return new Response(JSON.stringify(m.body),{status:m.status||200});
};
const ok=(t)=>({body:{choices:[{message:{content:t}}]}});
const empty={body:{choices:[{message:{content:''}}]}};
const img='data:image/jpeg;base64,'+'A'.repeat(2000);
const req=(o)=>({request:{json:async()=>o},env:{OPENROUTER_API_KEY:'k',LEAD_TELEGRAM_BOT_TOKEN:'t',LEAD_TELEGRAM_CHAT_ID:'c',...(o.env||{})},waitUntil:(p)=>{pend.push(p)}});
let pend=[];
const call=async(o)=>{pend=[];orCalls=[];tg.length=0;const r=await onRequestPost(req(o));await Promise.all(pend);return {r,j:await r.json()}};
const lead={name:'JK Wong',phone:'0123456789'};
const photoMsg=[{role:'user',content:[{type:'text',text:'do you have this ?'},{type:'image_url',image_url:{url:img}}]}];

// 1 primary ok
mode=()=>ok('Looks like NdFeB discs, please share size.'); let x=await call({lead,messages:photoMsg,notify:true});
assert.equal(x.j.reply,'Looks like NdFeB discs, please share size.'); assert.equal(orCalls.length,1); assert.equal(tg.length,1); assert.match(tg[0][1],/lead/);
// 2 primary empty -> fallback model answers
mode=(m)=>orCalls.length===1?empty:ok('fallback answer that is long enough'); x=await call({lead,messages:photoMsg,notify:false});
assert.equal(x.j.reply,'fallback answer that is long enough'); assert.deepEqual(orCalls,['google/gemini-2.5-flash-lite','openai/gpt-4o-mini']);
// --- new: primary never openrouter/free even if env says so
mode=()=>ok('Looks like NdFeB discs, please share size.'); x=await call({lead,messages:photoMsg,env:{LLM_MODEL:'openrouter/free'}});
assert.equal(orCalls[0],'google/gemini-2.5-flash-lite'); x=await call({lead,messages:photoMsg,env:{LLM_MODEL:'openai/gpt-4o-mini'}}); assert.equal(orCalls[0],'openai/gpt-4o-mini');
// guard-style reply then next model answers
mode=()=>orCalls.length===1?ok('User Safety: safe\nResponse Safety: safe'):ok('Please share diameter x thickness and grade N35/N42/N52.');
x=await call({lead,messages:[{role:'user',content:'what do you need to know ?'}]});
assert.match(x.j.reply,/diameter x thickness/); assert.equal(orCalls.length,2); assert.ok(!x.j.degraded);
// truncated reply with dangling list, finish=length -> next model gives full answer
const fin=(t,f)=>({body:{choices:[{message:{content:t},finish_reason:f}]}});
mode=()=>orCalls.length===1?fin('Looks like NdFeB discs. Could you please share a few key details? * **','length'):ok('Looks like NdFeB discs. Please share: 1. size 2. grade 3. qty.');
x=await call({lead,messages:photoMsg}); assert.match(x.j.reply,/1\. size 2\. grade/); assert.equal(orCalls.length,2);
// finish=length with clean text -> next model
mode=()=>orCalls.length===1?fin('We supply NdFeB discs in many grades and sizes for you. Please tell me the diameter and then the thick','length'):ok('Complete answer: send diameter, grade, quantity.');
x=await call({lead,messages:photoMsg}); assert.match(x.j.reply,/^Complete answer/);
// every model truncated -> cleaned partial + key questions line + owner alert (no dangling '* **')
mode=()=>fin('Looks like NdFeB discs. Could you please share a few key details? * **','length');
x=await call({lead,messages:photoMsg,notify:false}); assert.ok(x.j.partial); assert.ok(!/\*\s*\*\*\s*$/.test(x.j.reply.split('\n\n')[0])); assert.match(x.j.reply,/diameter x thickness/); assert.ok(tg.some(t=>t[1].includes('could NOT answer')));
// all guard output -> degraded fallback
mode=()=>ok('User Safety: safe\nResponse Safety: safe'); x=await call({lead,messages:photoMsg}); assert.ok(x.j.degraded); assert.doesNotMatch(x.j.reply,/Safety/);
// normal reply with finish=stop passes untouched
mode=()=>fin('**Looks like** NdFeB discs.\n1. size\n2. grade','stop'); x=await call({lead,messages:photoMsg}); assert.equal(x.j.reply,'**Looks like** NdFeB discs.\n1. size\n2. grade');
// 3 all empty -> helpful message, never "(no reply)", Telegram gets failure alert + photo
mode=()=>empty; x=await call({lead,messages:photoMsg,notify:true});
assert.equal(x.r.status,200); assert.ok(x.j.degraded); assert.match(x.j.reply,/could not read your photo/); assert.doesNotMatch(x.j.reply,/no reply/);
console.log(' calls:',orCalls.join(','),'| telegram:',tg.map(t=>t[0]).join(','));
assert.ok(tg.some(t=>t[1].includes('could NOT answer'))); assert.ok(tg.some(t=>t[0]==='sendPhoto'));
// 4 errors + exception
mode=()=>({status:402,body:{error:{message:'Insufficient credits'}}}); x=await call({lead,messages:[{role:'user',content:'hello'}]});
assert.ok(x.j.degraded); assert.match(x.j.reply,/try again/);
mode=()=>'throw'; x=await call({lead,messages:photoMsg}); assert.ok(x.j.degraded);
// 5 missing key
x=await call({lead,messages:photoMsg,env:{OPENROUTER_API_KEY:''}}); assert.ok(x.j.degraded); assert.equal(orCalls.length,0); assert.ok(tg.length>=1);
// 6 oversize image -> note added, still answered
mode=(m,b)=>{ const last=b.messages[b.messages.length-1]; assert.ok(JSON.stringify(last).includes('too large')); return ok('please resend a smaller photo');};
x=await call({lead,messages:[{role:'user',content:[{type:'text',text:'hi'},{type:'image_url',image_url:{url:'data:image/jpeg;base64,'+'A'.repeat(1700000)}}]}]}); assert.equal(x.j.reply,'please resend a smaller photo');
// 7 vision models all fail but text-only works
mode=(m,b)=>{const hasImg=JSON.stringify(b.messages).includes('image_url'); return hasImg?{status:400,body:{error:{message:'no image support'}}}:ok('text only answer that is fine')};
x=await call({lead,messages:photoMsg}); assert.equal(x.j.reply,'text only answer that is fine'); assert.ok(x.j.no_image);
// 8 validation
x=await call({lead:{name:'x'},messages:photoMsg}); assert.equal(x.r.status,400);
x=await call({lead,messages:[]}); assert.equal(x.r.status,400);
// 9 hang -> timeout handled (shorten by faking timers not needed: skip long); 
console.log('handler ok');
