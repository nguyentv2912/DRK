#!/usr/bin/env python3
"""Portable title-overlay renderer. Paths resolve relative to the JSON plan."""
import argparse,json,re,shutil,subprocess,unicodedata
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from fontTools.ttLib import TTFont
SKILL=Path(__file__).resolve().parents[1]
def run(cmd):
 r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-5000:])
 return r

def wrap(text,font,width):
 rows=[];current=''
 for word in text.split():
  if font.getlength(word)>width:raise ValueError('Một từ dài hơn vùng chữ; điều chỉnh font hoặc bề rộng.')
  trial=(current+' '+word).strip()
  if current and font.getlength(trial)>width:rows.append(current);current=word
  else:current=trial
 if current:rows.append(current)
 return rows

def normalized(t):return re.sub(r'\s+',' ',unicodedata.normalize('NFC',t)).strip().casefold()
def asset(p,base):
 q=Path(p).expanduser();q=q if q.is_absolute() else base/q
 if not q.is_file():raise FileNotFoundError(str(q))
 return q.resolve()

def render(p,base,out,ff,prepare,overwrite):
 identifier=str(p.get('id','test'))
 if not re.fullmatch(r'[A-Za-z0-9_-]+',identifier):raise ValueError('id chỉ dùng chữ/số/gạch ngang/gạch dưới')
 dest=out/identifier
 if dest.exists() and any(dest.iterdir()) and not overwrite:raise FileExistsError(f'{dest}; dùng --overwrite cho bản sửa.')
 dest.mkdir(parents=True,exist_ok=True)
 title=unicodedata.normalize('NFC',p['title']);main=unicodedata.normalize('NFC',p.get('main',title));support=unicodedata.normalize('NFC',p.get('supporting',''))
 if normalized(main+' '+support)!=normalized(title):raise ValueError('main/supporting phải giữ toàn bộ title; sửa lỗi gõ ở cả title và text.')
 font=asset(p.get('font',str(SKILL/'assets/fonts/TT-Commons-Pro-ExtraBold.ttf')),base)
 cmap=TTFont(font).getBestCmap();missing=sorted({c for c in main+support if not c.isspace() and ord(c) not in cmap})
 if missing:raise ValueError('Font thiếu glyph: '+''.join(missing))
 w=int(p.get('width',1080));h=int(p.get('height',1920));duration=float(p.get('duration',15));fps=int(p.get('fps',30));ratio=float(p.get('support_ratio',.72));width=int(p.get('text_width',w-120));maxheight=int(p.get('max_text_height',410))
 if w%2 or h%2 or min(w,h,duration,fps,ratio)<=0:raise ValueError('Kích thước phải chẵn và các thông số phải dương.')
 size=int(p.get('font_size',76));minimum=int(p.get('min_font_size',44));stroke=int(p.get('stroke',4));rows=None
 for fs in range(size,minimum-1,-2):
  f1=ImageFont.truetype(str(font),fs);f2=ImageFont.truetype(str(font),int(fs*ratio))
  try:a=wrap(main,f1,width);b=wrap(support,f2,width)
  except ValueError:continue
  mainstep=fs+int(p.get('main_line_gap',-4));substep=int(fs*ratio)+int(p.get('support_line_gap',4))
  height=len(a)*mainstep+len(b)*substep
  if height<=maxheight:rows=(a,b);break
 if rows is None:raise ValueError('Tiêu đề không vừa vùng chữ; cần đổi bố cục, không tự bỏ nội dung.')
 y=int(p.get('y',h*float(p.get('anchor',2/3))-height/2))
 if y<40 or y+height+40>h-100:raise ValueError('Cụm chữ ngoài vùng an toàn.')
 overlay=Image.new('RGBA',(w,h));shadow=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(shadow)
 left=(w-width)//2;sd.rounded_rectangle((max(0,left-32),y-30,min(w,left+width+32),y+height+28),radius=32,fill=(0,0,0,int(p.get('shadow_alpha',135))))
 overlay.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20)));draw=ImageDraw.Draw(overlay);cursor=y
 for lines,f,color,step in [(a,f1,p.get('main_color','white'),mainstep),(b,f2,p.get('support_color','#EBFF2D'),substep)]:
  for line in lines:
   draw.text(((w-f.getlength(line))/2,cursor),line,font=f,fill=color,stroke_width=stroke,stroke_fill='black');cursor+=step
 overlay.save(dest/'overlay.png')
 actual=dict(p,rendered_font_size=fs,rendered_support_size=int(fs*ratio),rendered_y=y,lines=a+b)
 (dest/'plan.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2))
 if prepare:return {'id':identifier,'prepared':True}
 video=asset(p['video'],base);music=asset(p['music'],base);mp4=dest/'video.mp4'
 fade=min(1,duration/4);fadein=min(.4,duration/4);cx=str(p.get('crop_x','(iw-ow)/2'));cy=str(p.get('crop_y','(ih-oh)/2'))
 vf=f'[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:{cx}:{cy},setsar=1,fps={fps}[v];[v][1:v]overlay=0:0:format=auto,format=yuv420p[out];[2:a]loudnorm=I=-18:TP=-2:LRA=11,afade=t=in:d={fadein},afade=t=out:st={duration-fade}:d={fade},aresample=48000[a]'
 run([ff,'-y','-v','error','-stream_loop','-1','-i',str(video),'-loop','1','-i',str(dest/'overlay.png'),'-stream_loop','-1','-i',str(music),'-filter_complex',vf,'-map','[out]','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','23','-threads','4','-c:a','aac','-b:a','192k','-movflags','+faststart',str(mp4)])
 check=run([ff,'-v','error','-i',str(mp4),'-f','null','-'])
 if check.stderr:raise RuntimeError(check.stderr)
 for label,t in [('start',0),('middle',duration/2),('end',max(0,duration-1/fps))]:
  run([ff,'-y','-v','error','-ss',str(t),'-i',str(mp4),'-frames:v','1',str(dest/f'preview-{label}.png')])
 levels=run([ff,'-i',str(mp4),'-af','volumedetect','-vn','-f','null','-']).stderr
 meta=subprocess.run([ff,'-i',str(mp4)],capture_output=True,text=True).stderr
 source_meta=subprocess.run([ff,'-i',str(video)],capture_output=True,text=True).stderr
 source_dur=re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)',source_meta)
 seconds=sum(float(n)*factor for n,factor in zip(source_dur.groups(),[3600,60,1])) if source_dur else None
 qc={'decode':'passed','requested_duration':duration,'source_duration':seconds,'source_looped':seconds is not None and seconds<duration,'visual_review':'required','audio_listening':'not performed by script','volume_measurements':levels[-1800:],'output_metadata':meta[-2600:]}
 (dest/'qc.json').write_text(json.dumps(qc,ensure_ascii=False,indent=2))
 return {'id':identifier,'video':str(mp4),'source_looped':qc['source_looped']}

def main_cli():
 ap=argparse.ArgumentParser();ap.add_argument('--plan',required=True);ap.add_argument('--output',required=True);ap.add_argument('--batch',action='store_true');ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--overwrite',action='store_true');args=ap.parse_args()
 path=Path(args.plan).resolve();data=json.loads(path.read_text());items=data if isinstance(data,list) else [data]
 if not items:raise ValueError('Plan trống')
 if not args.batch:items=items[:1]
 ff=shutil.which('ffmpeg')
 if not ff:
  import imageio_ffmpeg
  ff=imageio_ffmpeg.get_ffmpeg_exe()
 out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
 for p in items:print(json.dumps(render(p,path.parent,out,ff,args.prepare_only,args.overwrite),ensure_ascii=False),flush=True)
if __name__=='__main__':main_cli()
