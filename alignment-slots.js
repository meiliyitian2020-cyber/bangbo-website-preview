// Keep source text slots and navigation widths fixed when product copy changes.
function alignProductSlots(){
 const reference=ALIGN_REFERENCE[lang];if(!reference)return;
 const issues=[];
 function reserve(element,referenceHtml){
  if(!element)return;
  element.style.removeProperty('height');element.style.removeProperty('min-height');
  const width=element.getBoundingClientRect().width;if(!width)return;
  const probe=element.cloneNode(false);probe.innerHTML=referenceHtml;
  probe.setAttribute('aria-hidden','true');probe.inert=true;
  Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:width+'px',height:'auto',minHeight:'0',maxHeight:'none',visibility:'hidden',pointerEvents:'none'});
  element.parentElement.appendChild(probe);
  const height=probe.getBoundingClientRect().height,referenceScrollHeight=probe.scrollHeight;probe.remove();
  element.style.height=height+'px';element.style.minHeight=height+'px';
  if(element.scrollHeight>referenceScrollHeight+2)issues.push({selector:element.tagName+'.'+element.className,text:element.textContent,referenceHeight:height,actualHeight:element.scrollHeight});
 }
 function reserveIdentity(element,text){
  if(!element)return;
  element.style.removeProperty('width');
  const probe=element.cloneNode(false);probe.textContent=text;
  Object.assign(probe.style,{position:'fixed',top:'-99999px',left:'0',width:'max-content',maxWidth:element.parentElement.clientWidth+'px',height:'auto',minHeight:'0',visibility:'hidden'});
  element.parentElement.appendChild(probe);const rect=probe.getBoundingClientRect();probe.remove();
  element.style.width=rect.width+'px';reserve(element,text);
 }
 reserveIdentity($('.entity-name'),'HAGO SINGAPORE PTE. LTD.');
 reserveIdentity($('.entity-address'),'30 PASIR PANJANG ROAD #15-31A MAPLETREE BUSINESS CITY SINGAPORE 117440');
 if(activePage==='home'){
  reserve($('#hello h1'),reference.home.title);reserve($('#hello .hero-description'),reference.home.description);
  reference.home.scenes.forEach(s=>{
   reserve($('#'+s.id+' .scene-copy h2'),s.title);reserve($('#'+s.id+' .scene-copy>p'),s.description);
  });
  const navLabels=({en:['Voice rooms','Gifts','Badges','Private messages','Games'],zh:['语音房畅聊','礼物互动','房间等级','私聊分享日常','聊天小游戏'],hi:['वॉइस रूम','गिफ़्ट','बैज','निजी चैट','गेम'],id:['Ruang suara','Hadiah','Lencana','Pesan pribadi','Game']})[lang];
  const referenceLabels=[reference.nav.home,...reference.home.scenes.map(s=>s.title)];
  $$('.screen-nav button').forEach((button,i)=>{
   button.style.removeProperty('width');button.style.removeProperty('min-width');
   const probe=button.cloneNode(true);$('span',probe).textContent=referenceLabels[i];
   probe.setAttribute('aria-hidden','true');probe.inert=true;
   Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:'auto',visibility:'hidden',pointerEvents:'none'});
   button.parentElement.appendChild(probe);const width=probe.getBoundingClientRect().width;probe.remove();
   button.style.width=width+'px';button.style.minWidth=width+'px';
   if(i>0)$('span',button).textContent=navLabels[i-1];
  });
  fitMobileHome(true);
 }else{
  reserve($('.page-intro h1'),reference[activePage]?.title||$('.page-intro h1')?.innerHTML);
  let introText=reference[activePage]?.intro;
  if(activePage.startsWith('policy/'))introText=reference.policyDescriptions[activePage.split('/')[1]];
  if(activePage==='law-enforcement')introText=reference.policyDescriptions.law;
  if(introText)reserve($('.page-intro>.wrap>p'),introText);
  if(activePage==='about'){
   reserve($('.about-copy h2'),reference.about.heading);
   $$('.about-copy>p').forEach((p,i)=>reserve(p,reference.about.paragraphs[i]));
   $$('.about-values article').forEach((article,i)=>{reserve($('h3',article),reference.about.values[i][0]);reserve($('p',article),reference.about.values[i][1]);});
  }
  if(activePage==='about'){
   const band=$('.download-band'),left=$('.download-band .wrap>div');
   if(band&&left){
    left.style.removeProperty('width');
    const probe=band.cloneNode(true);probe.inert=true;probe.setAttribute('aria-hidden','true');
    Object.assign(probe.style,{position:'fixed',top:'-99999px',left:'0',width:band.getBoundingClientRect().width+'px',visibility:'hidden'});
    $('h2',probe).innerHTML=reference.home.downloadTitle;$('p',probe).innerHTML=reference.home.downloadText;
    for(const el of [$('.wrap>div',probe),$('h2',probe),$('p',probe)]){el.style.removeProperty('width');el.style.removeProperty('height');el.style.removeProperty('min-height');}
    document.body.appendChild(probe);const width=$('.wrap>div',probe).getBoundingClientRect().width;probe.remove();left.style.width=width+'px';
   }
   reserve($('.download-band h2'),reference.home.downloadTitle);
   reserve($('.download-band p'),reference.home.downloadText);
  }
  if(activePage==='contact'){
   $$('.contact-choice').forEach((el,i)=>{reserve($('p',el),i===0?reference.contact.supportText:reference.contact.businessText);});
  }
  if(activePage==='help'){
   const rows=reference.faqs.filter(f=>(helpCategory==='all'||f[0]===helpCategory));
   $$('.faq-item summary').forEach((el,i)=>reserve(el,rows[i]?.[1]||el.innerHTML));
   $$('.support-guide li').forEach((el,i)=>reserve(el,reference.help.preparation[helpCategory][i]));
  }
  if(activePage==='safety'){
   $$('.policy-row p').forEach((el,i)=>reserve(el,reference.policyDescriptions[policyKeys[i]]));
  }
  reserve($('.footer-brand>p'),reference.footer.tagline);
  if(activePage==='contact'){
   const email=$('.contact-choice a[href^="mailto:"]');
   if(email){
    email.style.removeProperty('width');const probe=email.cloneNode(true);
    const text=[...probe.childNodes].find(n=>n.nodeType===Node.TEXT_NODE);if(text)text.textContent='olapartyservice@gmail.com';
    probe.setAttribute('aria-hidden','true');probe.inert=true;
    Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:'auto',visibility:'hidden'});
    email.parentElement.appendChild(probe);const width=probe.getBoundingClientRect().width;probe.remove();
    email.style.width=width+'px';email.style.justifyContent='space-between';
   }
  }
 }
 window.INFRIENDS_ALIGNMENT={sourceVersion:19,issues};
 document.documentElement.setAttribute('data-alignment-issues',JSON.stringify(issues));
 document.documentElement.setAttribute('data-alignment-language',lang);
 document.documentElement.setAttribute('data-alignment-width',String(window.innerWidth));
}
const renderAlignedProduct=render;
render=function(){renderAlignedProduct();requestAnimationFrame(alignProductSlots);document.fonts?.ready.then(alignProductSlots);};
const renderOriginalFaq=renderFaq;renderFaq=function(){renderOriginalFaq();requestAnimationFrame(alignProductSlots);};
window.addEventListener('resize',()=>requestAnimationFrame(alignProductSlots));
