const {chromium}=require('playwright');
const fs=require('fs');const assert=require('assert');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const results=[],errors=[],network=[];
 const routes=['home','about','help','contact','safety','policy/terms','policy/privacy','policy/children','policy/community','policy/bullying','policy/cookies','law-enforcement'];
 const selectors=['#site-header','.brand','.header-download','.language','.hero-media-video','.screen-nav','#mobile-home-downloads','.entity-name','.entity-address','.compact-footer'];
 for(const viewport of [{width:1440,height:900},{width:390,height:844}]){
  const ctx=await browser.newContext({viewport});const page=await ctx.newPage();const base=await ctx.newPage();
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  page.on('response',r=>{if(r.status()>=400)network.push({url:r.url(),status:r.status()})});
  for(const lang of ['en','zh','hi','id']){
   await Promise.all([page.goto(`http://127.0.0.1:8768/dist/?lang=${lang}#/home`),base.goto(`http://127.0.0.1:8769/?lang=${lang}#/home`)]);
   await page.waitForTimeout(1200);await base.waitForTimeout(500);
   const rects=async p=>p.evaluate(ss=>Object.fromEntries(ss.map(s=>{const e=document.querySelector(s);if(!e)return[s,null];const r=e.getBoundingClientRect();return[s,{x:r.x,y:r.y,w:r.width,h:r.height}]})),selectors);
   const a=await rects(page),b=await rects(base),diff=[];
   for(const key of selectors){if(!a[key]||!b[key])continue;for(const dim of ['x','y','w','h'])if(Math.abs(a[key][dim]-b[key][dim])>1.1)diff.push({selector:key,dimension:dim,bangbo:a[key][dim],baseline:b[key][dim]});}
   console.log('Checking',viewport.width,lang);results.push({viewport,lang,rectDiff:diff,alignment:await page.evaluate(()=>window.BANGBO_ALIGNMENT),hero:await page.locator('.hero-media-video').first().boundingBox()});
   assert.equal(await page.locator('.home-slide:not(.loop-clone)').count(),6);
   assert.equal(await page.locator('video').count(),0);
   if(lang==='zh')await page.screenshot({path:`tests/bangbo-${viewport.width}-home.png`});
   for(let i=1;i<=5;i++){
    await page.locator(`[data-slide="${i}"]`).click();await page.waitForTimeout(700);
    assert((await page.locator('.scene-artwork').nth(i-1).getAttribute('src')).includes('placeholder-feature-'));
    if(lang==='zh'&&i===1)await page.screenshot({path:`tests/bangbo-${viewport.width}-feature.png`});
   }
   for(const route of routes.slice(1)){
    await page.goto(`http://127.0.0.1:8768/dist/?lang=${lang}#/${route}`);await page.waitForTimeout(140);
    assert(await page.locator('#main-content').innerText());
    if(route==='contact'){
     assert.equal(await page.locator('#contact-form').evaluate(f=>f.checkValidity()),false);
     await page.locator('[name=name]').fill('Review');await page.locator('[name=email]').fill('review@example.com');await page.locator('[name=message]').fill('Bangbo preview validation only.');await page.locator('[name=consent]').check();
     await page.locator('#contact-form button[type=submit]').click();assert(await page.locator('.form-result').isVisible());
    }
    if(route==='help'){
     await page.locator('#faq-search').fill('zzznomatch');assert.equal(await page.locator('#faq-results details').count(),0);await page.locator('#faq-search').fill('');
    }
   }
  }
  await page.goto('http://127.0.0.1:8768/dist/?lang=zh#/home');await page.waitForTimeout(500);
  await page.locator('[data-slide="0"]').click();await page.waitForTimeout(900);await page.locator('.home-slide:not(.loop-clone):not([inert]) [data-action=more-downloads], #mobile-home-downloads [data-action=more-downloads]').filter({visible:true}).first().click();assert(await page.locator('#more-download-panel').isVisible());
  await page.locator('#more-download-panel [data-channel=huawei]').click();assert((await page.locator('body').innerText()).includes('尚未核实'));
  await page.goto('http://127.0.0.1:8768/dist/?lang=zh#/contact');
  await page.locator('[data-action=cookies]:visible').first().click();await page.locator('[data-action=cookie-reject]').click();
  assert(await page.evaluate(()=>localStorage.getItem('bangbo-preview-cookies')));
  await page.evaluate(()=>document.querySelector('a[href=""]').click());assert((await page.locator('body').innerText()).includes('不会发起支付'));
  await ctx.close();
 }
 await browser.close();
 fs.writeFileSync('tests/review-results.json',JSON.stringify({results,errors,network},null,2));
 assert.deepEqual(errors,[]);assert.deepEqual(network,[]);assert(results.every(r=>r.rectDiff.length===0&&r.alignment.issues.length===0));
 console.log(JSON.stringify({cases:results.length,rectangleDifferences:results.reduce((n,r)=>n+r.rectDiff.length,0),errors,network}));
})().catch(e=>{console.error(e);process.exit(1)});
