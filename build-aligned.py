"""Build Bangbo with the vendored, hash-verified Ola v19 structural template."""
from pathlib import Path
import re,json,copy,hashlib,shutil,base64,html,runpy
from PIL import Image
root=Path(__file__).resolve().parent
source=(root/'template/index.html').read_text('utf-8')
manifest=json.loads((root/'template/manifest.json').read_text('utf-8'))
assert hashlib.sha256((root/'template/index.html').read_bytes()).hexdigest()==manifest['sha256']
out=root/'dist'; assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
def extract(text,name):
 a=text.index('const '+name+'=')+len('const '+name+'='); value,n=json.JSONDecoder().raw_decode(text[a:]);return value,a,a+n
def replace(text,name,value):
 _,a,b=extract(text,name);return text[:a]+json.dumps(value,ensure_ascii=False)+text[b:]
content,_,_=extract(source,'CONTENT');reference=copy.deepcopy(content)
product=json.loads((root/'product-copy.json').read_text('utf-8'))
def neutral(value):
 if isinstance(value,str):return value.replace('Ola Party','Bangbo').replace('OlaParty','Bangbo').replace('olapartyservice@gmail.com','woola2024@gmail.com')
 if isinstance(value,list):return [neutral(v) for v in value]
 if isinstance(value,dict):return {k:neutral(v) for k,v in value.items()}
 return value
content=neutral(content)
for lang,t in content.items():
 c=product[lang];t['home']['title']=c['title'];t['home']['description']=c['description']
 for i,scene in enumerate(t['home']['scenes']):
  scene['title'],scene['description']=c['scenes'][i];scene['source']=f'placeholder-feature-{i+1}.svg'
 t['home']['downloadTitle']=c['title'];t['home']['downloadText']=c['downloadText']
 t['footer']['tagline']='Read & Joy';t['footer']['copyright']='© 2017–2026 Woola Singapore Pte. Ltd.'
 t['about'].update(title=c['aboutTitle'],heading=c['aboutHeading'],intro=c['aboutIntro'],paragraphs=c['paragraphs'],values=c['values'],eyebrow={'en':'A novel reader','zh':'小说阅读应用','hi':'उपन्यास रीडर','id':'Pembaca novel'}[lang])
 t['help'].update(title=c['helpTitle'],intro=c['helpIntro'])
 prep={'en':['Choose the relevant question category.','Prepare your account ID and a brief description.'],'zh':['选择与你的问题相关的分类。','准备账号标识和简短的问题说明。'],'hi':['संबंधित सवाल की श्रेणी चुनें।','खाता ID और समस्या का संक्षिप्त विवरण तैयार रखें।'],'id':['Pilih kategori pertanyaan yang sesuai.','Siapkan ID akun dan uraian singkat.']}[lang]
 t['help']['preparation']['all']=prep
 for k in ['account','payment','safety','download']:t['help']['preparation'][k]=prep
 t['faqs']=c['faqs']
 t['contact']['supportText']=c['supportText'];t['contact']['businessText']=c['businessText']
 t['safety']['intro']={'zh':'查看 Bangbo 的公开协议、隐私信息与待确认的政策入口。','en':'Find Bangbo terms, privacy information and policy entries awaiting confirmation.','hi':'Bangbo की शर्तें, गोपनीयता और पुष्टि के लिए नीति प्रविष्टियाँ देखें।','id':'Temukan ketentuan, privasi dan kebijakan yang menunggu konfirmasi.'}[lang]
 t['safety']['current']={'zh':'官方正文','en':'Official text','hi':'आधिकारिक पाठ','id':'Teks resmi'}[lang]
 t['safety']['draft']={'zh':'待确认','en':'To confirm','hi':'पुष्टि बाकी','id':'Perlu konfirmasi'}[lang]
 t['policy']['source']={'zh':'Bangbo 公开官方政策','en':'Published Bangbo policy','hi':'Bangbo आधिकारिक नीति','id':'Kebijakan resmi Bangbo'}[lang]
 t['policy']['draftNote']=c['policyPending'];t['policy']['draftLabel']=t['safety']['draft']
 t['policyDescriptions']['children']={'en':'Official text awaiting confirmation.','zh':'独立正式政策正文待确认。','hi':'आधिकारिक पाठ की पुष्टि बाकी है।','id':'Teks resmi menunggu konfirmasi.'}[lang]
 # Product-specific language in the remaining fixed template slots.
 t['contact']['topics'][2]={'zh':'内容咨询','en':'Content inquiry','hi':'कहानी के बारे में','id':'Pertanyaan konten'}[lang]
links={'apple':'','google':'https://play.google.com/store/apps/details?id=com.bangbo.app','apk':'','recharge':'','email':'woola2024@gmail.com','terms':'https://www.bangboapp.com/user-policy','privacy':'https://www.bangboapp.com/policy','children':'','xiaomi':'','oppo':'','vivo':'','huawei':''}
page=replace(source,'CONTENT',content);page=replace(page,'LINKS',links)
policies={}
for key,file in [('privacy','official-privacy.json'),('terms','official-user.json')]:
 body=json.loads((root/'sources'/file).read_text('utf-8'))['content']
 body=re.sub(r'<script\b[^>]*>.*?</script>','',body,flags=re.S|re.I)
 body=re.sub(r'\son\w+="[^"]*"','',body,flags=re.I)
 policies[key]=body
page=replace(page,'POLICIES',policies)
# Unverified policy entries remain pending, with no borrowed legal outline.
outlines,_,_=extract(page,'OUTLINES')
outlines={key:{lang:[[content[lang]['safety']['draft'],product[lang]['policyPending']]] for lang in content} for key in outlines}
page=replace(page,'OUTLINES',outlines)
page=page.replace("['terms','privacy','children'].includes(key)","['terms','privacy'].includes(key)")
page=page.replace("i>2?'draft-status':''","i>1?'draft-status':''").replace('i<3?s.current:s.draft','i<2?s.current:s.draft')
paint=runpy.run_path(str(root/'brand-paint.py'))
asset_map={}
for f in (root/'template/assets').iterdir():
 shutil.copy2(f,assets/f.name);asset_map[f.name]='assets/'+f.name
def wrap_logo(name,w,h):
 data=base64.b64encode((root/'brand/logo.png').read_bytes()).decode()
 (assets/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><image width="100%" height="100%" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/></svg>','utf-8')
 return 'assets/'+name
oldassets,_,_=extract(source,'ASSETS')
for old,name in [('ola-share-icon.png','bangbo-logo.svg'),('hero-brand-logo.png','bangbo-hero-logo.svg')]:
 # Read source canvas dimensions from the original; persisted for portable rebuilds.
 sizes={'ola-share-icon.png':(500,170),'hero-brand-logo.png':(350,90)}
 # The header CSS fixes image dimensions; canvas proportions retain full logo.
 asset_map[old]=wrap_logo(name,*sizes[old])
shutil.copy2(root/'brand/app-icon.png',assets/'bangbo-app-icon.png')
Image.open(root/'brand/app-icon.png').resize((64,64)).save(assets/'bangbo-favicon.png')
asset_map['company-app-logo.png']='assets/bangbo-app-icon.png';asset_map['favicon-32x32-new.png']='assets/bangbo-favicon.png'
def placeholder(name,w,h,hero=False):
 label='首屏素材待替换' if hero else '功能素材待替换'
 text=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#e8faf5"/><rect x="18" y="18" width="{w-36}" height="{h-36}" rx="24" fill="none" stroke="#beded7" stroke-dasharray="6 9"/><g text-anchor="middle" fill="#50756e" font-family="Arial,sans-serif"><text x="50%" y="48%" font-size="24">{label}</text><text x="50%" y="53%" font-size="18">{'Hero media' if hero else 'Feature media'} · {w} × {h}</text></g></svg>'''
 (assets/name).write_text(text,'utf-8');return 'assets/'+name
for i,scene in enumerate(reference['en']['home']['scenes'],1):asset_map[scene['image']]=placeholder(f'placeholder-feature-{i}.svg',720,1280)
asset_map['p1_youngs-38ed979a0c.png']=placeholder('placeholder-about.svg',822,756)
placeholder('placeholder-hero-desktop.svg',1600,900,True);placeholder('placeholder-hero-mobile.svg',900,1600,True)
(assets/'bangbo-background.svg').write_text(paint['decorative_background'](1600,900),'utf-8')
asset_map['p1_bg-105ed6b6c9.png']='assets/bangbo-background.svg'
page=replace(page,'ASSETS',asset_map)
page=re.sub(r'const HERO_MEDIA=\{[^\n]*\};','const HERO_MEDIA={};',page)
poster='''function heroVideoPlaceholder(){return `<div class="hero-media-video"><div class="hero-video-stage"><picture><source media="(max-width:680px)" srcset="assets/placeholder-hero-mobile.svg"><img class="hero-loop-freeze" src="assets/placeholder-hero-desktop.svg" alt="Bangbo media placeholder" loading="eager" decoding="async"></picture></div></div>`;}
'''
page=re.sub(r'function heroVideoPlaceholder\(\)\{.*?\n(?=function homePage)',lambda _:poster,page,flags=re.S)
page=page.replace("if(action==='preview-download'){toast(downloadCopy().note);return;}","if(action==='preview-download'){const url=LINKS[event.target.closest('[data-channel]').dataset.channel];if(url)window.open(url,'_blank','noopener,noreferrer');else toast(BANGBO_COPY[lang].pending);return;}")
page=page.replace("i<3?s.current:s.draft","i<2?s.current:s.draft")
page=page.replace('यह केवल प्रीव्यू है। डाउनलोड लिंक अभी सक्रिय नहीं हैं।','Google Play उपलब्ध है। अन्य लिंक की पुष्टि बाकी है।').replace('当前为样式预览，暂未配置下载跳转。','Google Play 已接通，其他渠道待核实。').replace('Preview only. Download destinations are not configured.','Google Play is available. Other links await verification.').replace('Hanya pratinjau. Tujuan unduhan belum dikonfigurasi.','Google Play tersedia. Tautan lain belum terverifikasi.')
page=re.sub(r'function ambient\(\)\{[^\n]*',"function ambient(){return '<div class=\"ambient\" aria-hidden=\"true\"></div>';}",page)
page=paint['paint_styles'](page)
page=re.sub(r'function sceneBackground\(\)\{[^\n]*',lambda _:paint['SCENE'],page)
# Real company information follows the original website; store discrepancy is in SOURCES.md.
page=page.replace('HAGO SINGAPORE PTE. LTD.','Woola Singapore Pte. Ltd.').replace('30 PASIR PANJANG ROAD #15-31A MAPLETREE BUSINESS CITY SINGAPORE 117440','9 Straits View, #06-07, Marina One West Tower, Singapore 018937')
page=page.replace('Ola Party','Bangbo').replace('OlaParty','Bangbo').replace('olapartyservice@gmail.com','woola2024@gmail.com').replace('ola-preview-','bangbo-preview-')
page=page.replace('href="assets/favicon-32x32-new.png"','href="assets/bangbo-favicon.png"')
page=re.sub(r'<meta name="description"[^>]+>','<meta name="description" content="Bangbo — Read &amp; Joy. Discover romance, web novels and new authors.">',page,count=1)
page=page.replace('Bangbo — Make a little more connection','Bangbo — Read & Joy').replace('name="theme-color" content="#146d58"','name="theme-color" content="#52f4e4"')
slots=(root/'alignment-slots.js').read_text('utf-8')
slots=slots.replace('INFRIENDS_ALIGNMENT','BANGBO_ALIGNMENT')
slots=re.sub(r'const navLabels=.*?\[lang\];',"const navLabels=BANGBO_COPY[lang].nav;",slots)
slots=slots.replace("'HAGO SINGAPORE PTE. LTD.'", "atob('SEFHTyBTSU5HQVBPUkUgUFRFLiBMVEQu')").replace("'30 PASIR PANJANG ROAD #15-31A MAPLETREE BUSINESS CITY SINGAPORE 117440'", "atob('MzAgUEFTSVIgUEFOSkFORyBST0FEICMxNS0zMUEgTUFQTEVUUkVFIEJVU0lORVNTIENJVFkgU0lOR0FQT1JFIDExNzQ0MA==')").replace('olapartyservice@gmail.com','woola2024@gmail.com')
extra='const BANGBO_COPY='+json.dumps(product,ensure_ascii=False)+';\nconst ALIGN_REFERENCE=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(\"'+base64.b64encode(json.dumps(reference,ensure_ascii=False).encode()).decode()+'\"),c=>c.charCodeAt(0))));\n'+slots+'''\ndocument.addEventListener('click',event=>{const a=event.target.closest('a');if(a&&a.getAttribute('href')===''){event.preventDefault();toast(BANGBO_COPY[lang].recharge);}});\n'''
page=page.replace('\nrender();\n})();','\n'+extra+'\nrender();\n})();')
# Public logical asset names carry this brand; event IDs are left untouched.
for old,new in [('ola-share-icon.png','brand-logo'),('hero-brand-logo.png','brand-hero-logo')]:page=page.replace(old,new)
assert [paint['TOKEN'].sub('<color>',x) for x in re.findall(r'<style[^>]*>(.*?)</style>',source,re.S)]==[paint['TOKEN'].sub('<color>',x) for x in re.findall(r'<style[^>]*>(.*?)</style>',page,re.S)]
assert [s['id'] for s in content['en']['home']['scenes']]==[s['id'] for s in reference['en']['home']['scenes']]
assert not re.search(r'olaparty|infriends|HAGO SINGAPORE|PASIR PANJANG',page,re.I)
(out/'index.html').write_text(page,'utf-8')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n','utf-8');(out/'.nojekyll').touch()
(root/'check-script.js').write_text('\n'.join(re.findall(r'<script[^>]*>(.*?)</script>',page,re.S)),'utf-8')
(root/'alignment-reference.json').write_text(json.dumps(manifest|{'scene_ids':[s['id'] for s in reference['en']['home']['scenes']],'css_layout_identical':True,'hero_desktop':[16,9],'hero_mobile':[9,16],'feature_canvas':[720,1280]},indent=2),'utf-8')
print('Bangbo built. v19 CSS layout declarations unchanged; 4 languages; hero + 5 feature placeholders; 2 genuine official policies.')
