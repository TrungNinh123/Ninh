// Quay video hướng dẫn 4 bước từ app thật (scripts/app_tu_lam.py phải đang chạy ở :8080).
// Chạy: node scripts/video/quay_huong_dan.js <thư mục ảnh mẫu> <thư mục ra>
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const [,,ANH,OUT]=process.argv;
const CAP=[
 ['Bước 1/4','Gõ tên tiệm hoặc dán link Google Maps. Kiểm lại tên, địa chỉ, giờ mở cửa.'],
 ['Bước 2/4','Chọn 4–12 ảnh móng đẹp nhất do tiệm làm. Máy tự cắt khung, chỉnh sáng, giữ màu.'],
 ['Bước 3/4','Gõ bảng giá: mỗi dòng tên dịch vụ | giá. Ghi rõ đã gồm tháo gel cũ chưa.'],
 ['Bước 4/4','Nhập số Zalo, bấm Xuất bản. Web và mã QR có ngay.'],
 ['Xong','Mở web của tiệm, in mã QR đặt ở quầy. Không cần gọi ai.']];
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,recordVideo:{dir:OUT,size:{width:390,height:844}}});
const p=await ctx.newPage();
const cap=async i=>{await p.evaluate(([t,s])=>{let d=document.getElementById('_cap');if(!d){d=document.createElement('div');d.id='_cap';
 d.style.cssText='position:fixed;left:10px;right:10px;bottom:14px;z-index:99;background:rgba(23,16,14,.92);color:#f5eee3;border-radius:16px;padding:12px 14px;font:600 15px/1.4 "Be Vietnam Pro",sans-serif;border:2px solid #c9a14a;pointer-events:none';document.body.appendChild(d);document.body.style.paddingBottom='130px';}
 d.innerHTML='<div style="color:#e9c977;font-size:13px;letter-spacing:.08em">'+t+'</div>'+s;},CAP[i]);};
const go=ms=>p.waitForTimeout(ms);
await p.goto('http://localhost:8080/');await go(800);await cap(0);await go(1500);
await p.type('#ten','Sơn Mài Nail',{delay:90});await p.type('#dc','Quận 1, TP.HCM',{delay:60});await p.type('#gio','09:00–21:00 mỗi ngày',{delay:40});await go(1200);await p.click('#b1');
await go(500);await cap(1);await go(1200);
const files=fs.readdirSync(ANH).filter(f=>/\.(jpe?g|png)$/i.test(f)).slice(0,12).map(f=>path.join(ANH,f));
await p.setInputFiles('#imgs',files);await go(2500);await p.click('#b2');
await go(500);await cap(2);await p.fill('#gia','');await p.type('#gia','Sơn gel trơn | 150.000đ\nĐắp gel, nối móng | 350.000đ\nTháo gel cũ | Miễn phí',{delay:35});await go(1200);await p.click('#b3');
await go(500);await cap(3);await p.type('#zalo','0900000000',{delay:110});await go(900);await p.click('#b4');
await p.waitForSelector('section[data-s="5"].on',{timeout:60000});await cap(4);await go(3500);
const href=await p.getAttribute('#xem','href');await p.goto('http://localhost:8080'+href);await go(900);await cap(4);
const H=await p.evaluate(()=>document.body.scrollHeight);for(let i=0;i<=60;i++){await p.evaluate(y=>scrollTo(0,y),i*(H-844)/60);await go(70);}
await go(800);await ctx.close();await b.close();})();
