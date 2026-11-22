"""Compile curated Vietnamese question records; keep bank separate from UI."""
import json, hashlib, random, math
import fitz
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
modules=json.loads((ROOT/'content/modules.json').read_text(encoding='utf8'))
sources=json.loads((ROOT/'content/sources.json').read_text(encoding='utf8'))
source_map={(s['module'],s['page']):s for s in sources}
bank=[]

def add(key,page,concept,prompt,correct,wrongs,explanation,kind='concept',image=None,extra=None):
 mid='m'+key.replace('.','-'); pages=[int(x) for x in str(page).split(',')]; refs=[]
 for n in pages:
  s=source_map[(mid,n)];refs.append({'module':mid,'page':n,'region':s['title']})
 ident=hashlib.sha256((key+'|'+concept+'|'+prompt).encode()).hexdigest()[:12]
 opts=[{'id':'o0','text':str(correct),'explanation':'Đúng. '+explanation}]+[{'id':f'o{i+1}','text':str(t),'explanation':r} for i,(t,r) in enumerate(wrongs)]
 assert len(opts)==4 and len({x['text'] for x in opts})==4,(key,concept,prompt)
 random.Random(ident).shuffle(opts)
 correct_index=next(i for i,o in enumerate(opts) if o['id']=='o0')
 legacy_map={o['id']:'abcd'[i] for i,o in enumerate(opts)}
 for i,o in enumerate(opts):o['id']='abcd'[i]
 q={'id':'q-'+ident,'modules':[mid],'concept':concept,'status':'ready','type':kind,'difficulty':'medium' if kind!='concept' else 'basic','prompt':prompt,'options':opts,'correct':'abcd'[correct_index],'legacyOptionMap':legacy_map,'explanation':explanation,'sources':refs}
 if image:q.update(image='/assets/questions/'+image,imageAlt=extra or 'Hình dữ liệu cần phân tích; xem nhãn và số liệu trong hình.')
 bank.append(q)
 return q

for file in sorted((ROOT/'content/authoring').glob('*.txt')):
 for line in file.read_text(encoding='utf8').splitlines():
  if not line.strip() or line.startswith('#'):continue
  fields=line.split('|');assert len(fields)==9,(file,line[:90],len(fields))
  key,page,concept,prompt,correct,w1,w2,w3,explain=fields
  add(key,page,concept,prompt,correct,[w.split('~',1) for w in [w1,w2,w3]],explain)

# Numerical applications use explicit assumptions and independently recomputed distractors.
def numeric(key,page,concept,prompt,value,wrong_values,explanation):
 add(key,page,concept,prompt,str(value),[(str(v),r) for v,r in wrong_values],explanation,'calculation')

numeric('3.2','8,9','depthwise-params','Depthwise Conv có Cin=32, kernel 3×3, depth multiplier=1 và bias=True. Tổng số tham số là bao nhiêu?',320,[(288,'Bạn chỉ đếm weights và quên 32 bias.'),(896,'Depthwise không trộn mọi cặp input/output channel như standard Conv.'),(32,'32 là số bias; còn 288 weights.')],'Weights = 32×3×3 = 288; bias = 32. Tổng 288+32 = 320.')
numeric('3.2','14,15','pointwise-params','Pointwise Conv từ 32 lên 64 channel, bias=True, có bao nhiêu tham số?',2112,[(2048,'Thiếu 64 bias ở output.'),(320,'Đây là số tham số depthwise 3×3 với 32 channel, không phải pointwise.'),(18496,'Bạn đã dùng kernel 3×3 thay vì 1×1.')],'Weights = 64×32×1×1 = 2048; bias = 64. Tổng 2112.')
numeric('3.2','20,21','separable-params','Thay standard Conv(Cin=32,Cout=64,k=3) bằng depthwise(k=3,multiplier=1) rồi pointwise. Cả hai lớp đều có bias. Tổng tham số của hai lớp?',2432,[(2368,'Đã bỏ qua cả 32 bias depthwise và 64 bias pointwise.'),(18496,'Đây là tham số của standard Conv trước khi thay.'),(2400,'Bạn quên 32 bias của depthwise.')],'Depthwise: 32×9+32=320. Pointwise: 64×32+64=2112. Tổng = 2432; standard Conv tương ứng có 18496 tham số.')

def svg(name,body,w=720,h=280):
 out=ROOT/'public/assets/questions';out.mkdir(parents=True,exist_ok=True)
 (out/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><rect width="100%" height="100%" fill="#f5f7fc"/><g font-family="Segoe UI,Arial,sans-serif" fill="#192c4a">{body}</g></svg>',encoding='utf8')

body='<text x="32" y="30" font-size="17">Depthwise convolution · 3 input channels · multiplier = 1</text>'
for i,(label,color) in enumerate([('R','#ffe1e4'),('G','#d8f1e7'),('B','#dce7ff')]):
 y=55+i*68
 body+=f'<rect x="48" y="{y}" width="110" height="48" rx="8" fill="{color}" stroke="#8493ab"/><text x="93" y="{y+30}" font-size="20">{label}</text><path d="M158 {y+24}H268M428 {y+24}H538" stroke="#596c84" stroke-width="2"/><rect x="268" y="{y}" width="160" height="48" rx="8" fill="white" stroke="#8493ab"/><text x="294" y="{y+30}" font-size="16">Kernel W{label}</text><rect x="538" y="{y}" width="110" height="48" rx="8" fill="{color}" stroke="#8493ab"/><text x="580" y="{y+30}" font-size="20">{label}′</text>'
svg('depthwise.svg',body)
add('3.2',6,'depthwise-channel-independence','Trong sơ đồ depthwise, giữ nguyên weights, bias và hai kênh R/B. Nếu chỉ dữ liệu kênh G đổi, output nào có thể đổi?','Chỉ G′', [('Cả R′, G′ và B′','Depthwise xử lý riêng từng channel, không cộng chéo như standard Conv.'),('Chỉ R′ và B′','Hai kênh này không nhận dữ liệu từ G.'),('Không output nào','Weights cố định không có nghĩa output độc lập với input.')],'Theo Yc = Xc * Wc + bc, mỗi output chỉ phụ thuộc input cùng channel. Chỉ G′ có thể đổi. Hình vẽ lại từ mô tả depthwise, không thêm pointwise.','visual','depthwise.svg','Ba nhánh riêng: R qua kernel WR ra R′, G qua WG ra G′, B qua WB ra B′.')

body='<text x="32" y="28" font-size="18">1 = foreground · 0 = background</text>'
for x,title,grid in [(75,'Ground truth G',[[1,1,0],[1,0,0],[0,0,0]]),(415,'Prediction Ŷ',[[1,0,0],[1,1,0],[0,0,0]])]:
 body+=f'<text x="{x}" y="62" font-size="19">{title}</text>'
 for r,row in enumerate(grid):
  for c,v in enumerate(row):
   xx=x+c*52;yy=82+r*52;body+=f'<rect x="{xx}" y="{yy}" width="48" height="48" rx="5" fill="'+('#dce7ff' if v else 'white')+f'" stroke="#8493ab"/><text x="{xx+18}" y="{yy+31}" font-size="22">{v}</text>'
svg('masks.svg',body)
add('7.1','53,54','dice-iou-masks','Đọc hai mask trong hình. Chỉ tính foreground và không thêm smoothing. Cặp (Dice, IoU) nào đúng?','(2/3, 1/2)', [('(1/2, 2/3)','Bạn đã đảo hai metric; Dice thường lớn hơn IoU trên cùng cặp mask.'),('(4/5, 2/3)','Bạn đã bỏ FN khỏi mẫu số của cả hai công thức.'),('(7/9, 7/9)','7/9 là pixel accuracy gồm cả 5 TN; không phải Dice hoặc IoU foreground.')],'TP=2 ở (1,1),(2,1); FP=1 ở (2,2); FN=1 ở (1,2). Dice=2TP/(2TP+FP+FN)=4/6=2/3. IoU=TP/(TP+FP+FN)=2/4=1/2.','visual','masks.svg','Ground truth các hàng 110,100,000; prediction 100,110,000.')

# Further applications, each with a distinct reasoning step rather than a page quota.
numeric('2.5',6,'mse-example','Với y=[3,−0.5,2,7], prediction=[2.5,0,2,8], MSE là bao nhiêu?',0.375,[(1.5,'Đây là tổng squared residuals, bạn chưa chia n=4.'),(0.5,'Đây là MAE của ví dụ, không phải MSE.'),(0.6124,'Đây gần RMSE, đã lấy căn ngoài yêu cầu.')],'Residuals=[0.5,−0.5,0,−1]. Bình phương=[0.25,0.25,0,1]. Tổng=1.5; MSE=1.5/4=0.375.')
numeric('2.5',7,'mae-example','Cũng với y=[3,−0.5,2,7] và prediction=[2.5,0,2,8], MAE bằng bao nhiêu?',0.5,[(0.375,'Bạn bình phương residuals nên tính MSE.'),(2,'Đây là tổng absolute residuals, chưa chia 4.'),(-0.25,'Bạn cộng residual có dấu; MAE dùng trị tuyệt đối.')],'Absolute residuals=[0.5,0.5,0,1], tổng 2; MAE=2/4=0.5.')
numeric('2.5',20,'bce-negative','y=0 và predicted p(y=1)=0.7. BCE dùng log tự nhiên, làm tròn 3 chữ số, bằng bao nhiêu?',1.204,[(0.357,'Bạn tính −ln(0.7), phù hợp y=1 chứ không phải y=0.'),(0.7,'Đây là probability, chưa áp logarithm.'),(0.3,'Đây là probability của class đúng, không phải negative log loss.')],'BCE=−[0×ln(0.7)+1×ln(0.3)]=−ln(0.3)≈1.204.')
numeric('2.6',15,'f1-counts','Confusion counts TP=4,FP=1,FN=1,TN=4. F1 của positive class bằng bao nhiêu?',0.8,[(0.4,'Đây là TP/n, không phải F1.'),(0.5,'Không phải tỉ số 2TP/(2TP+FP+FN).'),(1,'FP và FN khác 0 nên F1 không thể hoàn hảo.')],'F1=2TP/(2TP+FP+FN)=8/(8+1+1)=0.8.')
numeric('2.6',16,'specificity-counts','TP=8,FN=2,TN=18,FP=6. Specificity là bao nhiêu?',0.75,[(0.8,'Đây là sensitivity/recall TP/(TP+FN).'),(0.5714,'Đây gần precision 8/(8+6).'),(0.25,'Đây là FPR=FP/(FP+TN), không specificity.')],'Specificity=TN/(TN+FP)=18/24=0.75.')
numeric('2.6',8,'r2-calculation','Với SSE=30 và SST=20>0, R² bằng bao nhiêu?',-0.5,[(0.5,'Bạn đã đảo dấu hoặc bỏ thứ tự 1−SSE/SST.'),(1.5,'Đây là SSE/SST chưa lấy 1 trừ tỉ số.'),(0,'R² không bị chặn dưới bởi 0.')],'R²=1−30/20=1−1.5=−0.5; model kém baseline mean trong phép đo này.')
numeric('2.8',19,'fc-layer-params','FC từ 8 feature lên 5 output, có bias riêng từng output, có bao nhiêu tham số?',45,[(40,'Bạn quên 5 bias.'),(48,'Bạn cộng bias theo số input 8 thay vì output 5.'),(13,'Không cộng trực tiếp input và output dimensions.')],'W có 5×8=40 phần tử; b có 5. Tổng 45.')
numeric('2.8',27,'leaky-relu-value','Leaky ReLU có α=0.01. Với input z=−3, output là gì?',-0.03,[(0,'Đây là ReLU thường ở miền âm.'),(-3,'Bạn dùng slope 1 thay vì 0.01 ở miền âm.'),(0.03,'Slope dương nhân input âm vẫn cho output âm.')],'Ở z<0, Leaky ReLU(z)=αz=0.01×(−3)=−0.03.')
numeric('2.9',19,'sgd-one-step','Scalar weight w=2, gradient dL/dw=−3, learning rate=0.1. Một SGD update không momentum/decay cho w mới là bao nhiêu?',2.3,[(1.7,'Bạn cộng gradient thay vì trừ gradient.'),(1.9,'Bạn dùng learning rate nhưng bỏ gradient −3.'),(-1,'Bạn quên learning rate trong step.')],'wnew=w−ηg=2−0.1×(−3)=2.3. Gradient âm làm weight tăng theo quy tắc descent.')
numeric('2.9',28,'momentum-one-step','Momentum theo v_t=μv_(t−1)+g_t. Cho μ=0.9,v_(t−1)=2,g_t=−1. v_t bằng bao nhiêu?',0.8,[(2.8,'Bạn đã bỏ dấu âm của current gradient.'),(-0.8,'Bạn đảo dấu toàn kết quả.'),(1,'Bạn trừ gradient mà quên hệ số μ.')],'v_t=0.9×2−1=1.8−1=0.8; sau đó optimizer mới dùng velocity để cập nhật weight.')
numeric('2.9',48,'adamw-decay-only','AdamW có gradient update term bằng 0, θ=10,η=0.1,λ=0.2. Theo θ←(1−ηλ)θ, θ mới bằng bao nhiêu?',9.8,[(8,'Bạn quên nhân learning rate vào decay coefficient.'),(10,'Gradient term bằng 0 không loại bỏ decoupled weight decay.'),(10.2,'Weight decay co weight dương lại, không tăng lên.')],'(1−0.1×0.2)×10=0.98×10=9.8.')
numeric('3.1',27,'conv-stride-output','Conv2d có Hin=32,k=3,s=2,p=0,d=1. Hout bằng bao nhiêu?',15,[(16,'Bạn đã coi padding=same hoặc bỏ floor theo công thức explicit.'),(30,'Bạn quên chia stride=2.'),(14,'Bạn bỏ +1 cuối công thức.')],'Hout=floor((32−3)/2)+1=floor(14.5)+1=15.')
numeric('3.1',31,'standard-conv-params','Standard Conv Cin=3,Cout=16,kernel=3×3,bias=True có bao nhiêu tham số?',448,[(432,'Bạn quên 16 output bias.'),(160,'Bạn bỏ nhân Cin=3 trong weights.'),(144,'Bạn chỉ nhân Cout với kernel area.')],'Weights=16×3×3×3=432; bias=16; tổng 448.')
numeric('3.1',37,'strided-receptive-field','Hai lớp Conv k=3,s=2 liên tiếp, không dilation. Receptive field của một output lớp hai theo mỗi trục input gốc là bao nhiêu?',7,[(5,'Bạn dùng công thức stack stride=1 và quên input jump=2 của lớp hai.'),(6,'Không cộng trực tiếp hai kernel sizes.'),(9,'Không nhân kernel sizes; receptive field phụ thuộc stride/jump.')],'R1=3,jump1=2. R2=R1+(3−1)×jump1=3+2×2=7.')
numeric('3.4',12,'dilated-output','Hin=7,k=3,s=1,p=1,d=2. Hout theo công thức explicit bằng bao nhiêu?',5,[(7,'Bạn bỏ ảnh hưởng dilation nên tưởng padding=1 vẫn same.'),(3,'Bạn trừ effective kernel nhưng quên padding.'),(9,'Dilation không tự làm output lớn thêm theo cấu hình này.')],'keff=2×(3−1)+1=5. Hout=floor((7+2−5)/1)+1=5.')
numeric('3.5',21,'layernorm-affine','LayerNorm((8,4,4)), elementwise_affine=True. Số gamma và beta trainable tổng cộng?',256,[(16,'Bạn chỉ đếm theo channel như BatchNorm2d.'),(128,'Đây là số phần tử một trong hai tensors gamma/beta.'),(0,'Affine=True có learnable gamma và beta.')],'Mỗi gamma và beta có 8×4×4=128 phần tử. Tổng 256; không nhân batch size.')
numeric('3.6',14,'gap-numeric','Một channel feature map 2×2 có values [[1,3],[5,7]]. Global average pooling output của channel đó là gì?',4,[(7,'Đây là max, không phải average.'),(16,'Bạn tính tổng nhưng quên chia 4.'),(2,'Không phải trung bình của bốn giá trị.')],'GAP=(1+3+5+7)/4=16/4=4.')
numeric('3.7',15,'bottleneck-count','Bỏ bias/norm: bottleneck 1×1 (64→16),3×3 (16→16),1×1 (16→64) có bao nhiêu weights?',4352,[(36864,'Đây là standard 3×3 (64→64), không bottleneck.'),(2304,'Bạn chỉ đếm spatial 3×3 ở giữa.'),(3328,'Bạn thiếu một projection 1×1 có 1024 weights.')],'64×16 +16×16×9 +16×64=1024+2304+1024=4352.')
numeric('3.7',29,'se-count','SE có C=64,reduction r=16. Bỏ bias, hai FC C→C/r→C có bao nhiêu weights?',512,[(256,'Bạn mới đếm một trong hai FC.'),(8192,'Bạn dùng hidden width 64 thay vì C/r=4.'),(128,'Bạn đếm channel thay vì tích hai chiều FC.')],'Hidden width=64/16=4. Weights=64×4+4×64=512.')
numeric('4.1',27,'lstm-state-update','Ở một chiều LSTM, cprev=2,f=0.5,i=0.25,g=−0.8. Cell state mới c là bao nhiêu?',0.8,[(1.2,'Bạn đã bỏ dấu âm của candidate g.'),(1,'Bạn chỉ giữ f×cprev và bỏ input gate contribution.'),(-0.2,'Bạn chỉ tính i×g, bỏ memory cũ.')],'c=f×cprev+i×g=0.5×2+0.25×(−0.8)=1−0.2=0.8.')
numeric('4.1',32,'gru-interpolation','Theo h=(1−z)h̃+z hprev, cho z=0.8,h̃=2,hprev=5. h mới bằng bao nhiêu?',4.4,[(2.6,'Bạn đảo trọng số z và 1−z so với convention trong slide.'),(7,'Bạn cộng states mà bỏ gates.'),(4,'Bạn chỉ giữ z×hprev và bỏ candidate term.')],'h=0.2×2+0.8×5=0.4+4=4.4. Với z lớn, output gần hidden state cũ.')
numeric('5.1',45,'embedding-count','Vocabulary=10000,d=128. Token embedding lookup có bao nhiêu weights, bỏ positional table?',1280000,[(10128,'Bạn cộng dimensions thay vì nhân.'),(16384,'Đây là d², không vocabulary×d.'),(128000,'Bạn thiếu một hệ số 10 của vocabulary.')],'Embedding table có 10000 hàng, mỗi hàng 128 phần tử: 10000×128=1280000.')
numeric('5.1',45,'learned-pos-count','Learned absolute position table có nmax=256,d=64. Có bao nhiêu weights?',16384,[(0,'Sinusoidal cố định mới có 0 learnable parameters.'),(320,'Bạn cộng 256+64 thay vì tích.'),(4096,'Đây là d², không nmax×d.')],'Mỗi vị trí có vector 64 chiều: 256×64=16384 positional weights.')
numeric('5.2',25,'encoder-param-count','Bỏ toàn bộ bias và LayerNorm parameters. Encoder layer d=64,dff=256 có 4d²+2ddff weights. Kết quả?',49152,[(16384,'Bạn chỉ đếm MHA 4d².'),(32768,'Bạn chỉ đếm FFN 2ddff.'),(8192,'Không tính đúng các projection matrices.')],'MHA=4×64²=16384; FFN=2×64×256=32768; tổng 49152.')
numeric('5.3',29,'patch-dimension','Patch 16×16 từ ảnh RGB, flatten trước linear patch projection. Input dimension mỗi patch là bao nhiêu?',768,[(256,'Bạn quên 3 RGB channels.'),(48,'Bạn chỉ nhân một chiều spatial với channel.'),(196,'Đây có thể là số patches ảnh 224×224, không dimension một patch.')],'Mỗi patch chứa 16×16×3=768 giá trị; linear projection đưa 768 về hidden width d.')
numeric('5.4',22,'linear-warmup','Warmup tuyến tính ηt=ηmax t/Twarmup, ηmax=0.001,Twarmup=1000. Ở t=250, learning rate bằng bao nhiêu?',0.00025,[(0.001,'Bạn dùng peak LR trước khi warmup kết thúc.'),(0.004,'Bạn đảo t/Twarmup.'),(0.00075,'Đây là phần còn lại đến peak, không current LR.')],'ηt=0.001×250/1000=0.00025.')
numeric('6.1',48,'ema-teacher-numeric','Một scalar EMA teacher=10,student=6,m=0.9. Teacher sau update bằng bao nhiêu?',9.6,[(6.4,'Bạn đảo trọng số teacher và student.'),(16,'Bạn cộng hai states nhưng bỏ EMA coefficients.'),(4,'Bạn lấy hiệu hai states, không EMA.')],'θteacher mới=0.9×10+0.1×6=9+0.6=9.6.')
numeric('6.1',40,'ntxent-pair-count','Một SimCLR batch gồm N=4 ảnh, mỗi ảnh hai views. Với một anchor, denominator loại self có bao nhiêu views?',7,[(8,'Bạn chưa loại anchor self-similarity.'),(6,'Bạn còn loại cả positive; positive vẫn nằm denominator.'),(4,'Bạn đếm ảnh gốc thay vì augmented views.')],'Có 2N=8 views; bỏ k=i còn 7, gồm 1 positive và 6 negatives theo giả thiết mỗi ảnh khác nhau.')
numeric('7.1',9,'panoptic-numeric','Panoptic evaluation có matched IoUs [0.6,0.8],TP=2,FP=1,FN=1. PQ bằng bao nhiêu, làm tròn 4 chữ số?',0.4667,[(0.7,'Đây là SQ, chưa nhân RQ.'),(0.6667,'Đây là RQ, chưa nhân SQ.'),(1.3667,'PQ dùng tích SQ×RQ, không cộng.')],'SQ=(0.6+0.8)/2=0.7. RQ=2/(2+0.5+0.5)=2/3. PQ=0.7×2/3≈0.4667.')
numeric('7.1',63,'miou-average','Hai class có IoU lần lượt 0.8 và 0.2. Macro mIoU của hai class bằng bao nhiêu?',0.5,[(0.8,'Bạn chỉ lấy class tốt hơn.'),(1,'Bạn cộng nhưng chưa chia số class.'),(0.16,'Không nhân hai IoU để lấy macro average.')],'mIoU=(0.8+0.2)/2=0.5; mỗi class có trọng số bằng nhau theo macro definition.')
numeric('8.1',27,'pyramid-candidate-count','P3=80×80,P4=40×40,P5=20×20, một prediction/reference point mỗi cell. Tổng Na là bao nhiêu?',8400,[(6400,'Bạn mới đếm P3, bỏ P4 và P5.'),(140,'Bạn chỉ cộng chiều dài mỗi map thay vì diện tích.'),(2560000,'Không nhân số cells giữa các mức pyramid.')],'Na=80²+40²+20²=6400+1600+400=8400 reference points.')
numeric('8.1',78,'hungarian-matrix-cost','Cost matrix của slide có row minima ở (GT1,Q1)=0.32,(GT2,Q2)=0.25,(GT3,Q3)=0.21; ba cột khác nhau. Tổng cost assignment đó?',0.78,[(0.32,'Bạn chỉ lấy một cặp, chưa cộng toàn assignment.'),(0.26,'Đây là mean cost, trong khi objective dùng tổng.'),(0.96,'Đây là một cost khác của matrix, không tổng ba cặp chọn.')],'0.32+0.25+0.21=0.78. Trong ví dụ, row minima không xung đột cột nên assignment đạt tổng cận dưới từng hàng.')
numeric('9.1',30,'vae-latent-numeric','Reparameterization một chiều có μ=1,σ=2,ε=−0.5. z bằng bao nhiêu?',0,[(2,'Bạn bỏ dấu âm của noise.'),(-0.5,'Bạn chỉ trả noise, bỏ μ và σ.'),(0.5,'Bạn cộng μ+ε nhưng quên scale σ.')],'z=μ+σ ε=1+2×(−0.5)=0.')
numeric('9.1',52,'ddpm-noising-numeric','DDPM một scalar: ᾱt=0.64,x0=2,ε=−1. xt=√ᾱt x0+√(1−ᾱt)ε bằng bao nhiêu?',1,[(0.92,'Bạn dùng ᾱ thay vì căn ᾱ và 1−ᾱ.'),(2.2,'Bạn đã bỏ dấu âm của noise.'),(1.6,'Bạn bỏ noise term.')],'√0.64=0.8; √0.36=0.6. xt=0.8×2+0.6×(−1)=1.')
numeric('10.3',28,'lora-rank-count','W0 shape (512,256),rank=4. Không train bias/base. Tổng A,B trainable weights?',3072,[(131072,'Đây là full matrix 512×256, không adapter count.'),(2048,'Bạn mới đếm B, thiếu A.'),(1024,'Bạn mới đếm A, thiếu B.')],'A=(4,256):1024; B=(512,4):2048; tổng 3072.')
numeric('11.1',19,'late-fusion-numeric','Late fusion score=α scoreimg+(1−α)scoretxt. α=0.75,scoreimg=0.8,scoretxt=0.4. Score fused?',0.7,[(1.2,'Bạn cộng scores mà không dùng weights.'),(0.5,'Bạn đảo α và 1−α.'),(0.6,'Bạn chỉ lấy image weighted term, bỏ text contribution.')],'0.75×0.8+0.25×0.4=0.6+0.1=0.7.')
numeric('11.1',87,'multitask-weighted-loss','Ltotal=λ1L1+λ2L2. λ1=1,L1=0.4,λ2=0.2,L2=3. Tổng loss bằng bao nhiêu?',1,[(3.4,'Bạn cộng raw losses mà bỏ λ2.'),(0.68,'Bạn nhân 0.2 cho cả tổng, sai λ1=1.'),(0.6,'Bạn chỉ tính task 2, bỏ task 1.')],'Ltotal=1×0.4+0.2×3=0.4+0.6=1.0; cần xem cả per-task metrics, không chỉ tổng loss.')

exec((ROOT/'scripts/visual_questions.py').read_text(encoding='utf8'))

# Extract the actual printed marker from the PDF, not from PDF page minus one.
for m in modules:
 doc=fitz.open(ROOT/m['path'])
 for p in doc:
  numbers=[]
  for block in p.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     text=span['text'].strip();x0,y0,x1,y1=span['bbox']
     if not text.isdigit():continue
     landscape=p.rect.width>p.rect.height
     if landscape and .84*p.rect.width<x0<.87*p.rect.width and .12*p.rect.height<y0<.9*p.rect.height and span['size']<6:numbers.append(int(text))
     if not landscape and .45*p.rect.width<x0<.55*p.rect.width and y0>.93*p.rect.height:numbers.append(int(text))
  if len(numbers)==1:source_map[(m['id'],p.number+1)]['printedSlide']=numbers[0]

# Link shared concepts to lecture notes without making duplicate bank entries.
note_links={
 'm5-7':{'transformer-pipeline':3,'feature-aggregation':4,'two-mixers':7,'pre-norm-order':8,'qkv-intuition':9,'weighted-sum':10,'self-cross-sources':9,'mask-before-softmax':11,'ffn-parameters':10,'families-mask':14,'t5-cross':15,'linear-probe-freeze':16,'lora-count':16},
 'm6-2':{'ssl-target':2,'ssl-goal':2,'pretext-head':3,'denoising-target':5,'ae-semantic-gap':5,'contrastive-positive':6,'simclr-projector':5,'cosine-invariance':6,'ntxent-denominator':6,'dino-distill':8,'ema-teacher':7,'masked-ar-context':9,'probe-diagnosis':10}}
for target,links in note_links.items():
 for concept,page in links.items():
  candidates=[q for q in bank if q['concept']==concept]
  if not candidates:continue
  q=candidates[0];q['modules'].append(target);q['sources'].append({'module':target,'page':page,'region':source_map[(target,page)]['title']})

# Verified printed slide numbers on inspected pages; other pages remain explicitly unknown.
verified={('m3-2',6):5,('m3-2',9):8,('m3-5',7):6,('m5-5',37):36,('m7-1',53):52,('m7-1',54):53,('m8-1',48):47,('m8-1',76):75}
for s in sources:
 if (s['module'],s['page']) in verified:s['printedSlide']=verified[(s['module'],s['page'])]
for m in modules:m['questionCount']=sum(m['id'] in q['modules'] for q in bank)
coverage=json.loads((ROOT/'content/coverage.json').read_text(encoding='utf8'))
for p in coverage:
 p['questionIds']=[q['id'] for q in bank if any(s['module']==p['module'] and s['page']==p['page'] for s in q['sources'])]
 if p['questionIds']:p['classification']='question-source'
issues=[{'module':m['id'],'file':m['file'],'page':p['page'],'detail':p['issue']} for m in modules for p in coverage if p['module']==m['id'] and p['issue']]
for name,data in [('bank',bank),('modules',modules),('sources',sources),('coverage',coverage),('issues',issues)]:
 (ROOT/'content'/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
out=ROOT/'content/questions';out.mkdir(exist_ok=True)
for m in modules:(out/(m['id']+'.json')).write_text(json.dumps([q for q in bank if q['modules'][0]==m['id']],ensure_ascii=False,indent=2),encoding='utf8')
print('Compiled',len(bank),'questions across',sum(m['questionCount']>0 for m in modules),'modules.')
