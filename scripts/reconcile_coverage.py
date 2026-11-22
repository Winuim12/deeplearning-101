"""Record only pages actually inspected visually; never equate rendering with review."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reviewed={'m1-1':[88],'m2-3':[9],'m2-4':[8],'m2-5':[21],'m2-6':[20],'m2-7':[4],'m2-8':[22],'m2-9':[20],
'm3-1':[13],'m3-2':[6,9,21,25,26],'m3-3':[10],'m3-4':[7],'m3-5':[7],'m3-6':[21],'m3-7':[24],'m3-8':[38],'m3-9':[23],
'm4-1':[25,31],'m5-1':[18],'m5-2':[22],'m5-3':[30],'m5-5':[37],'m6-1':[37,41],
'm7-1':[53],'m8-1':[48,76],'m9-1':[19,46],'m10-2':[15],'m10-3':[29],'m11-1':[30,64,70,77]}
def read(name):return json.loads((ROOT/'content'/name).read_text(encoding='utf8'))
modules=read('modules.json');coverage=read('coverage.json');bank=read('bank.json')
for entry in coverage:
 entry['visualReviewed']=entry['page'] in reviewed.get(entry['module'],[])
 entry['concepts']=sorted({q['concept'] for q in bank if q['id'] in entry['questionIds']})
for m in modules:
 path=ROOT/'content/pages'/(m['id']+'.json');pages=json.loads(path.read_text(encoding='utf8'))
 for p in pages:p['visualReviewed']=p['page'] in reviewed.get(m['id'],[])
 path.write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'content/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
def ranges(ns):
 if not ns:return 'Không'
 groups=[];a=b=ns[0]
 for n in ns[1:]:
  if n==b+1:b=n
  else:groups.append(str(a) if a==b else f'{a}–{b}');a=b=n
 groups.append(str(a) if a==b else f'{a}–{b}');return ', '.join(groups)
lines=['# Tình trạng đọc và độ phủ nguồn','',
'Mọi file đã được trích văn bản và render ảnh. Bảng dưới tách rõ nguồn câu hỏi với trang đã kiểm tra trực quan; không tự đánh dấu toàn bộ tài liệu đã đọc kỹ. Một trang không có câu có thể là mục lục/lặp/nền tảng bổ sung; vẫn cần rà nếu muốn chứng nhận phủ toàn bộ.',
'','| File | Câu liên kết | Trang nguồn câu | Đã xem trực quan | Trang chưa xác nhận trực quan |','|---|---:|---:|---|---|']
for m in modules:
 entries=[p for p in coverage if p['module']==m['id']]
 lines.append(f"| {m['file']} | {m['questionCount']} | {sum(bool(p['questionIds']) for p in entries)} | {ranges([p['page'] for p in entries if p['visualReviewed']])} | {ranges([p['page'] for p in entries if not p['visualReviewed']])} |")
(ROOT/'reports/reading-status.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Visual page reviews explicitly recorded:',sum(p['visualReviewed'] for p in coverage))

