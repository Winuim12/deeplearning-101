"""Executed by build_bank.py; figures are explicit application examples or verified crops."""
def table_svg(name,title,grids,footer='',height=330):
 body=f'<text x="28" y="32" font-size="18">{title}</text>'
 for x,y,heading,rows in grids:
  body+=f'<text x="{x}" y="{y}" font-size="16">{heading}</text>'
  for r,row in enumerate(rows):
   for c,v in enumerate(row):
    xx=x+c*64;yy=y+18+r*45
    body+=f'<rect x="{xx}" y="{yy}" width="60" height="41" rx="5" fill="white" stroke="#b3c2d9"/><text x="{xx+30}" y="{yy+27}" text-anchor="middle" font-size="17">{v}</text>'
 if footer:body+=f'<text x="28" y="{height-18}" font-size="14">{footer}</text>'
 svg(name,body,h=height)

table_svg('causal.svg','Additive mask · hàng = query i · cột = key j',[(180,65,'Các cột j=1,2,3,4',[[0,'−∞','−∞','−∞'],[0,0,'−∞','−∞'],[0,0,0,'−∞'],[0,0,0,0]])],'Các scores chưa mask đều hữu hạn; softmax được tính theo hàng.')
add('5.5',37,'causal-read-row','Đọc ma trận mask trong hình. Query ở hàng i=3 có thể attend tới tập key nào sau softmax?','j=1,2,3',[('Chỉ j=4','j=4 bị −∞ ở hàng 3 nên weight bằng 0.'),('j=3,4','Bạn đọc nhầm phía tương lai; j=4 đang bị che.'),('Chỉ j=3','Hai keys quá khứ j=1,2 cũng được phép vì mask bằng 0.')],'Hàng 3 là [0,0,0,−∞]. Cộng mask trước softmax giữ keys 1,2,3 và chặn key 4. Hình vẽ lại đúng pattern causal mask trên slide.','visual','causal.svg')
table_svg('padding.svg','Padding mask · hàng = query · cột = key',[(180,65,'Các cột j=1,2,3,4',[[0,0,'−∞','−∞'],[0,0,'−∞','−∞'],[0,0,'−∞','−∞'],[0,0,'−∞','−∞']])],'Key 3 và 4 là PAD; attention scores ban đầu hữu hạn.')
add('5.5',37,'padding-read-columns','Trong padding mask ở hình, ở một query hợp lệ, tổng attention weight lên key 3 và 4 là bao nhiêu?','0',[('1','Hai cột PAD bị −∞ trước softmax nên không nhận probability mass.'),('0.5','Không chia đều weight cho masked keys.'),('Không xác định vì mask không tác động softmax','Additive mask tác động trực tiếp logits; −∞ cho exp=0.')],'Với scores hữu hạn ở ít nhất một key hợp lệ, softmax cho mỗi masked score −∞ weight 0. Tổng hai cột PAD bằng 0.','visual','padding.svg')
table_svg('attention-values.svg','Một hàng attention và scalar values',[(80,65,'Key j',[['1','2','3','4'],['0.05','0.70','0.20','0.05'],['0','10','20','30']])],'Hàng giữa: αj · hàng dưới: vj · output y=Σ αj vj',height=290)
add('5.5',34,'attention-values-read','Từ bảng weights và values, output scalar của query là bao nhiêu?','12.5',[('10','Đây là hard chọn value của weight lớn nhất, không weighted sum.'),('60','Bạn cộng các values mà không dùng weights.'),('15','Bạn lấy trung bình không trọng số của 4 values.')],'y=0.05×0+0.70×10+0.20×20+0.05×30=0+7+4+1.5=12.5. Hình là tình huống áp dụng weighted-sum theo slide, với bộ values cho trong đề.','visual','attention-values.svg')
table_svg('conv-patch.svg','Ví dụ áp dụng · Conv stride=1,padding=0,bias=1',[(50,65,'Input 3×3',[[1,2,0],[0,1,3],[2,0,1]]),(380,65,'Kernel 2×2',[[1,0],[0,1]])],'Tính output tại góc trên bên trái; không dùng activation.',height=290)
add('3.1',6,'conv-patch-numeric','Đọc input và kernel trong hình. Output ở vị trí góc trên trái sau Conv, có bias=1, là bao nhiêu?','3',[('2','Bạn tính đúng dot product nhưng quên bias=1.'),('5','Bạn đã cộng mọi phần tử của patch thay vì nhân kernel rồi cộng.'),('1','Bạn chỉ lấy bias, bỏ spatial dot product.')],'Patch trên trái [[1,2],[0,1]]. Dot product=1×1+2×0+0×0+1×1=2. Thêm bias 1 được 3. Hình minh họa bài áp dụng theo định nghĩa convolution.','visual','conv-patch.svg')
table_svg('pool-window.svg','Ví dụ áp dụng · pooling một cửa sổ 2×2',[(220,65,'Input window',[[1,5],[2,4]])],'Không padding; cửa sổ chứa đủ bốn giá trị.',height=240)
add('3.6','8,9','pool-compare-window','Cùng cửa sổ trong hình, cặp (max pooling, average pooling) nào đúng?','(5,3)',[('(3,5)','Bạn đã đảo max và average.'),('(5,12)','12 là tổng, average phải chia 4.'),('(4,3)','Max trong [1,5,2,4] là 5, không phải phần tử cuối 4.')],'Max=5. Average=(1+5+2+4)/4=12/4=3. Pooling thực hiện riêng từng channel; đây là một cửa sổ minh họa.','visual','pool-window.svg')
table_svg('hungarian.svg','Cost matrix · hàng = GT · cột = Query',[(180,60,'Q1       Q2       Q3       Q4',[[0.32,0.81,0.44,0.96],[0.77,0.25,0.58,0.69],[0.66,0.49,0.21,0.73]])],'GT1,GT2,GT3 lần lượt là ba hàng; ràng buộc one-to-one.',height=290)
add('8.1','76,77,78','hungarian-unmatched-figure','Với matrix trong hình và matching cost nhỏ nhất, query nào không được ghép với ba GT?','Q4',[('Q1','GT1→Q1 đạt row minimum 0.32 và không xung đột với hai row minima khác.'),('Q2','GT2→Q2 có cost 0.25 và thuộc assignment tối ưu.'),('Q3','GT3→Q3 có cost 0.21 và thuộc assignment tối ưu.')],'Min từng hàng lần lượt ở Q1,Q2,Q3, không xung đột cột; vì vậy assignment đạt tổng cận dưới 0.32+0.25+0.21=0.78. Q4 unmatched và học no-object. Hình vẽ lại số liệu cost matrix của slide, bỏ tô sẵn lời giải.','visual','hungarian.svg')
table_svg('nms-values.svg','Dữ liệu NMS từ ví dụ bài giảng',[(40,60,'Box / score',[['A1','0.95'],['A2','0.82'],['A3','0.74'],['B1','0.90']]),(350,60,'IoU với A1',[['A2','0.68'],['A3','0.73']])],'Threshold=0.50 · A1 đã được giữ · xử lý cùng nhóm NMS.',height=325)
add('8.1','48,49,50','nms-two-suppression','Sau khi giữ A1, từ hai IoU trong hình, xử lý A2 và A3 thế nào?','Loại cả A2 và A3',[('Giữ cả hai','Cả hai overlap với A1 đều vượt threshold 0.50.'),('Chỉ loại A2','IoU(A1,A3)=0.73 cũng lớn hơn 0.50.'),('Chỉ loại A3','IoU(A1,A2)=0.68 cũng lớn hơn 0.50.')],'Theo các bước ví dụ slide, A1 có score cao hơn; A2 và A3 đều overlap vượt 0.50 nên bị suppress. Bảng giữ đúng scores/IoUs từ các trang nguồn.','visual','nms-values.svg')
table_svg('shift-labels.svg','Causal LM training · token IDs minh họa',[(120,70,'Chuỗi gốc',[['A','B','C','D']]),(120,160,'Input đã cho',[['A','B','C']])],'Mỗi position phải dự đoán token kế tiếp.',height=285)
add('10.1',10,'shift-labels-figure','Từ sequence và input trong hình, label sequence aligned với ba output positions là gì?','[B,C,D]', [('[A,B,C]','Đây là input copy, không dịch một bước.'),('[D,C,B]','Không đảo thứ tự thời gian của target.'),('[A,C,D]','Vị trí đầu cần dự đoán B sau A, không phải chính A.')],'Input [A,B,C] tương ứng targets [B,C,D]; loss CE được tính trên từng position để học next-token. Hình là ví dụ alignment áp dụng theo slide.','visual','shift-labels.svg')
table_svg('confusion.svg','Confusion matrix · hàng Actual · cột Predicted',[(190,60,'Positive      Negative',[[8,2],[6,18]])],'Hàng 1: Actual Positive · hàng 2: Actual Negative',height=235)
add('2.6','12,13','confusion-read-fn','Đọc đúng trục confusion matrix trong hình. False negative là giá trị nào?','2',[('6','6 là actual negative nhưng predicted positive: FP.'),('8','8 là actual positive và predicted positive: TP.'),('18','18 là actual negative và predicted negative: TN.')],'FN là actual positive bị dự đoán negative, nằm hàng Positive/cột Negative =2. Dữ liệu là tình huống áp dụng; trục tuân theo định nghĩa trên slide.','visual','confusion.svg')
table_svg('logit-temp.svg','Logits cho một bước decoding',[(130,70,'Token A       Token B       Token C',[[4,2,0]])],'Không top-k/top-p ở bước này; rescale zi/T rồi softmax.',height=195)
add('10.3',16,'temperature-ranking-figure','Giữ logits trong hình, đổi temperature từ 1 sang 2. Phát biểu nào đúng?','A vẫn có xác suất cao nhất nhưng distribution phẳng hơn',[('C trở thành cao nhất','Chia mọi logits cho cùng số dương giữ thứ tự.'),('Prob(A) chắc chắn bằng 1','Temperature lớn hơn làm bớt tập trung, không hard argmax.'),('Logits không đổi nên probabilities không đổi','Logits sau rescale đổi từ [4,2,0] thành [2,1,0].')],'Scale dương giữ ranking A>B>C; chênh lệch logits giảm nên softmax ít sắc hơn. Hình là bộ logits ví dụ áp dụng temperature.','visual','logit-temp.svg')
table_svg('clip-pairs.svg','Batch pairing đúng trước khi shuffle',[(100,70,'Image index   Text index',[[1,1],[2,2],[3,3]])],'Chỉ shuffle thứ tự text thành [text3,text1,text2].',height=280)
add('11.1','30,33','clip-shuffled-target','Sau khi text columns bị shuffle như mô tả trong hình, positive text column của image1 nằm ở đâu?','Cột 2',[('Cột 1','Cột 1 bây giờ là text3; diagonal không còn đúng nếu không cập nhật pairing.'),('Cột 3','Cột 3 là text2 sau permutation được cho.'),('Cả ba cột đều positive','Không theo giả thiết một matched caption cho mỗi image trong ví dụ.')],'Text1 chuyển sang cột 2, nên image1 phải match cột 2. Diagonal target chỉ đúng khi giữ pairing order; shuffle độc lập mà không đổi targets gây supervision sai.','visual','clip-pairs.svg')

# Crop diagrams with original values intact, remove takeaway/answer paragraphs where feasible.
crop_tasks={
 'linear-feature-space':('m2-7',4,(.02,.13,.84,.90),'Nhìn các đồ thị trong hình: cùng dữ liệu nhưng polynomial features/MLP fit đường cong tốt hơn linear model trên input gốc. Giải thích nào đúng?'),
 'chain-rule-paths':('m2-9',20,(.04,.16,.84,.86),None),
 'conv-channel-sum':('m3-1',13,(.02,.17,.83,.78),None),
 'lstm-forget':('m4-1',25,(.03,.20,.84,.72),None),
 'gru-update-convention':('m4-1',31,(.03,.20,.84,.73),None),
 'pre-norm-order':('m5-2',22,(.03,.24,.84,.67),None),
 'simclr-projector':('m6-1',37,(.02,.19,.85,.74),None),
 'ntxent-denominator':('m6-1',41,(.03,.20,.83,.82),None),
 'vae-latent-numeric':('m9-1',19,(.03,.18,.83,.72),None),
 'ddpm-noising-numeric':('m9-1',46,(.04,.21,.83,.84),None),
 'qformer-cross-who':('m11-1',70,(.03,.16,.97,.5),None),
 'grounded-sam-order':('m11-1',64,(.02,.25,.83,.47),None),
 'llava-bridge':('m11-1',77,(.02,.18,.83,.51),None),
 'clip-diagonal':('m11-1',30,(.02,.18,.96,.53),None),
}
from PIL import Image
for concept,(mid,page,box,prompt) in crop_tasks.items():
 candidates=[q for q in bank if q['concept']==concept]
 if not candidates:continue
 q=candidates[0];src=ROOT/'public/assets/sources'/mid/f'{page}.webp'
 if not src.exists():continue
 im=Image.open(src);w,h=im.size
 if concept in ['lstm-forget','gru-update-convention']:
  doc=fitz.open(ROOT/next(m['path'] for m in modules if m['id']==mid));pdfpage=doc[page-1]
  rects=[r for image in pdfpage.get_images() for r in pdfpage.get_image_rects(image[0])]
  rect=max(rects,key=lambda r:r.width*r.height)
  box=(rect.x0/pdfpage.rect.width,rect.y0/pdfpage.rect.height,rect.x1/pdfpage.rect.width,rect.y1/pdfpage.rect.height)
 out=ROOT/'public/assets/questions'/(concept+'.webp');im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box))).save(out,'WEBP',quality=92)
 q['imageSource']={'module':mid,'page':page,'cropBoxNormalized':list(box),'kind':'original-crop'}
 q.update(image='/assets/questions/'+out.name,imageAlt=f'Sơ đồ trích nguyên từ {next(m["file"] for m in modules if m["id"]==mid)} trang PDF {page}; xem cấu trúc và nhãn trong hình.',type='visual')
 if prompt:q['prompt']=prompt
 if not any(s['module']==mid and s['page']==page for s in q['sources']):q['sources'].append({'module':mid,'page':page,'region':'Sơ đồ trong hình minh họa'})
