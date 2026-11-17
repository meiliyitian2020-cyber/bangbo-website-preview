"""Bangbo paint only: aqua app icon, red bookmark, ink wordmark."""
import re,colorsys
TOKEN=re.compile(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]+\)')
EXACT={'#146d58':'#006960','#d1ff69':'#52f4e4','#ddfaec':'#e4fcf8','#fffdf4':'#fcfffe','#19264b':'#182a2a','#cef5dd':'#ddfaf5','#67c99d':'#73cfc6','#ffe476':'#ffbbc5','#a4e8bb':'#a3e9df','#fcfff3':'#fcfffe','#edfbef':'#f0fcf9','#dcf7e8':'#dff8f4','#dcf4ce':'#e2f8f4','#ffe895':'#ffdce2','#72c99d':'#7acfc6','#c9f3e3':'#d9f7f2','#f9e591':'#ffd1da','#67c6a5':'#7dd4ca'}
def color(t):
 low=t.lower()
 if low in EXACT:return EXACT[low]
 if low.startswith('rgb'):
  a=re.findall(r'[\d.]+',low)
  if len(a)<3:return t
  rgb='#'+''.join(f'{int(float(v)):02x}' for v in a[:3]); updated=color(rgb)
  if updated==rgb:return t
  vals=[int(updated[i:i+2],16) for i in (1,3,5)]
  return ('rgba('+','.join(map(str,vals))+','+a[3]+')') if len(a)>3 else updated
 v=low[1:]
 if len(v)==3:v=''.join(x*2 for x in v)
 if len(v) not in (6,8):return t
 r,g,b=[int(v[i:i+2],16)/255 for i in (0,2,4)];h,l,s=colorsys.rgb_to_hls(r,g,b)
 if s>.04:
  hue=174/360 if 35/360<=h<=185/360 else (350/360 if 185/360<h<335/360 else h)
  r,g,b=colorsys.hls_to_rgb(hue,l,min(s,.6))
  return '#'+''.join(f'{round(x*255):02x}' for x in (r,g,b))+v[6:]
 return t
def paint_styles(page):
 return re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+TOKEN.sub(lambda n:color(n[0]),m[1])+'</style>',page,flags=re.S)
def decorative_background(w,h):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="b" x2="1" y2=".7"><stop stop-color="#e1fbf5"/><stop offset="1" stop-color="#f7fffc"/></linearGradient></defs><rect width="1600" height="900" fill="url(#b)"/><g fill="none" stroke="#6dc9bb" stroke-width="2" opacity=".15"><path d="M1130 130q150-70 260 0v500q-110-70-260 0zM1130 130q-150-70-260 0v500q110-70 260 0z"/><path d="M920 200q85-28 160 0m-160 65q85-28 160 0m110-65q70-28 140 0m-140 65q70-28 140 0"/></g><path d="M180 0h80v200l-40-28-40 28z" fill="#ff2c52" opacity=".055"/><path d="M1460 620h45v150l-22-20-23 20z" fill="#ff2c52" opacity=".07"/></svg>'''
SCENE='''function sceneBackground(){return `<div class="scene-backdrop" aria-hidden="true"><i></i><svg viewBox="0 0 720 420" fill="none"><g stroke="var(--scene-line)" stroke-width="2" opacity=".35"><path d="M420 100q90-45 190 0v230q-100-45-190 0q-90-45-190 0V100q100-45 190 0zM420 100v230"/><path d="M260 145q65-22 125 0m-125 45q65-22 125 0m70-45q60-22 120 0m-120 45q60-22 120 0"/></g><path d="M555 80h40v95l-20-15-20 15z" fill="var(--scene-yellow)" opacity=".45"/></svg></div>`;}'''
