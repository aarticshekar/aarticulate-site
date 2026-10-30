const {chromium}=require('playwright');const fs=require('fs');
const base=`<style>@import url('https://fonts.googleapis.com/css2?family=Lato:wght@700&family=Lora:ital,wght@0,600;1,400&display=swap');*{margin:0;box-sizing:border-box}body{width:1600px;height:900px;overflow:hidden;font-family:Lato}
.k{font:700 26px Lato;letter-spacing:6px;text-transform:uppercase}.t{font:600 74px/1.1 Lora}</style>`;
const C={
'your-client-isnt-difficult':`<body style="background:#1F5C63;color:#F6F1EA;padding:110px 120px">
<div class="k" style="color:#F0B9A6">The Transformation</div>
<div style="margin-top:90px;display:flex;height:150px;border-radius:24px;overflow:hidden">
<div style="flex:50;background:#F6F1EA;color:#1F5C63;display:flex;align-items:center;padding-left:48px;font:600 64px Lora">50 min</div>
<div style="flex:10;background:#BE7C68;display:flex;align-items:center;justify-content:center;font:600 44px Lora">10</div></div>
<div style="display:flex;margin-top:22px;font:700 28px Lato;color:#D5E4E2"><div style="flex:50">monologue</div><div style="flex:10;text-align:center">dialogue</div></div>
<div class="t" style="margin-top:110px;max-width:1200px;font-style:italic;font-weight:400;font-size:58px">Five consultants got there first.</div></body>`,
'more-to-crm-than-data-logging':`<body style="background:#F6F1EA;color:#1C2B33;padding:110px 120px">
<div class="k" style="color:#BE7C68">The Tech Layer</div>
<div class="t" style="margin-top:40px;color:#1F5C63">A CRM is three things.</div>
<div style="display:flex;gap:36px;margin-top:80px">${[['Memory','every promise, kept'],['Rulebook','how a lead becomes a deal'],['Compass','what’s coming next']].map(([a,b],i)=>`<div style="flex:1;background:${i==1?'#1F5C63':'#fff'};color:${i==1?'#F6F1EA':'#1C2B33'};border:2px solid #E4DACB;border-radius:28px;padding:48px"><div style="font:600 56px Lora">${a}</div><div style="font:700 26px Lato;margin-top:18px;opacity:.8">${b}</div></div>`).join('')}</div>
<div style="margin-top:56px;font:italic 400 40px Lora;color:#BE7C68">Data logging was never the point.</div></body>`,
'customer-is-king':`<body style="background:#1C2B33;color:#F6F1EA;padding:110px 120px">
<div class="k" style="color:#F0B9A6">The Handoff</div>
<div class="t" style="margin-top:40px">Customer is king.</div>
<div style="display:flex;align-items:center;gap:0;margin-top:90px">${['Call centre','Billing','Support'].map((x,i)=>`${i?`<div style="width:120px;height:6px;background:repeating-linear-gradient(90deg,#BE7C68 0 18px,transparent 18px 34px)"></div>`:''}<div style="border:3px solid #F6F1EA;border-radius:22px;padding:30px 40px;font:700 34px Lato">${x}</div>`).join('')}</div>
<div style="margin-top:70px;font:italic 400 44px Lora;color:#F0B9A6">So why does the customer fall through the gaps?</div></body>`,
'og-home':`<body style="background:#1F5C63;color:#fff;padding:140px 120px"><div style="font:600 44px Lora">Aarticulate<span style="color:#BE7C68">.</span></div>
<div class="t" style="margin-top:90px;max-width:1300px">Your revenue problem is an <i style="color:#F0B9A6;font-weight:400">integration</i> problem.</div>
<div style="margin-top:60px;font:700 30px Lato;color:#D5E4E2">Aarti Chandrseker on the gaps between sales, marketing, CS and tech</div></body>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
for(const [k,h] of Object.entries(C)){await p.setContent(base+h,{waitUntil:'networkidle'});await p.screenshot({path:`static/covers/${k}.jpg`,type:'jpeg',quality:86})}await b.close();console.log('ok')})();
