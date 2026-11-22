"""Read-only PDF ingestion. All generated files live outside slides/."""
import hashlib, json, re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
CONTENT.mkdir(exist_ok=True)
(CONTENT / 'pages').mkdir(exist_ok=True)

TITLES = {
'1.1':'Tổng quan Deep Learning','2.1':'Problem Formulation','2.2':'Datasets & Data Splits',
'2.3':'Linear Regression','2.4':'Classification','2.5':'Loss Functions','2.6':'Evaluation Metrics',
'2.7':'Model Capacity & Inductive Bias','2.8':'Multilayer Perceptron','2.9':'Training Neural Networks',
'3.1':'Convolution: nền tảng','3.2':'Efficient Convolutions','3.3':'Transposed Convolution','3.4':'Dilated Convolution',
'3.5':'Normalization','3.6':'Pooling & Dropout','3.7':'CNN Building Blocks','3.8':'CNN Architectures','3.9':'Data Pipeline & Augmentation',
'4.1':'RNN, LSTM & GRU','5.1':'Position, Mask & Training','5.2':'Attention & Transformer Core',
'5.3':'BERT, GPT, T5 & ViT','5.4':'Fine-tuning & Efficiency','5.5':'Transformer — Core Mechanisms',
'5.6':'Transformer — Families & Practice','5.7':'Transformer — Lecture Notes',
'6.1':'Self-Supervised Learning','6.2':'Self-Supervised — Lecture Notes',
'7.1':'Image Segmentation','8.1':'Object Detection','9.1':'VAE, GAN & Diffusion',
'10.1':'Generative Text','10.2':'GPT Decoder Architecture','10.3':'Modern LLMs & QLoRA','11.1':'Multimodal & Multitask Learning'}
GROUPS={'1':'Nền tảng','2':'Neural Networks','3':'Convolutional Networks','4':'Sequence Models','5':'Transformers','6':'Self-Supervised','7':'Segmentation','8':'Detection','9':'Generative Images','10':'Language Models','11':'Multimodal'}
ISSUES={'2.6':{20:'Phần diễn giải cuối trang bị cắt; bảng và đầu vào đọc được.'},'3.2':{25:'Chú thích shape cuối khung code bị cắt.'},'3.3':{10:'Công thức dài sát sidebar; đối chiếu trang 12.'},'8.1':{76:'Tiêu đề lấn sidebar; bảng cost đọc được.'}}
modules=[];sources=[];coverage=[]
files=sorted((ROOT/'slides').rglob('*.pdf'),key=lambda p:tuple(map(int,p.name.split('-')[0].split('.'))))
for path in files:
 key=path.name.split('-')[0]; mid='m'+key.replace('.','-'); doc=fitz.open(path); pages=[]
 for page in doc:
  full=page.get_text(); main=full.split('TP.HCM\n')[-1].strip(); lines=main.splitlines()
  title=' '.join(lines[:1]) or 'Trang không có văn bản'
  skipped=page.number==0 or bool(re.match(r'^(Outline|Content|Table of Contents|References|Key references)\b',title,re.I))
  entry={'page':page.number+1,'title':title,'text':main,'fullText':full,'width':page.rect.width,'height':page.rect.height,'rasterImages':len(page.get_images()),'vectorPaths':len(page.get_drawings()),'visualReviewed':False,'issue':ISSUES.get(key,{}).get(page.number+1)}
  pages.append(entry)
  sources.append({'id':f'{mid}-p{page.number+1}','module':mid,'page':page.number+1,'title':title,'printedSlide':None,'image':f'/api/pages/{mid}/{page.number+1}.webp'})
  coverage.append({'module':mid,'page':page.number+1,'classification':'reference-or-outline' if skipped else 'pending-review','questionIds':[],'issue':entry['issue'],'visualReviewed':False})
 modules.append({'id':mid,'key':key,'file':path.name,'path':path.relative_to(ROOT).as_posix(),'title':TITLES[key],'group':GROUPS[key.split('.')[0]],'pages':len(doc),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'description':f'{TITLES[key]} · {len(doc)} trang PDF','questionCount':0})
 (CONTENT/'pages'/f'{mid}.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')

for name,data in [('modules',modules),('sources',sources),('coverage',coverage),('topics',[{'id':k,'title':v} for k,v in GROUPS.items()])]:
 (CONTENT/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(f'Indexed {len(modules)} PDF / {len(sources)} pages; originals untouched.')
