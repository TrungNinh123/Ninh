"""Kiểm thử chế độ giới thiệu + chi hoa hồng (21 tình huống). Chạy app với NAILMARK_DEV=1 SEPAY_API_KEY=thu-nghiem, xoá du_lieu/don_hang.json, rồi: python scripts/kiem_thu_gioi_thieu.py"""
import json,urllib.request,time
B="http://localhost:8080"; KQ=[]
def call(u,d=None,m="POST"):
    r=urllib.request.Request(B+u,data=None if d is None and m=="GET" else json.dumps(d or {}).encode(),headers={"Content-Type":"application/json"},method=m)
    try: return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e: return json.load(e)
get=lambda u:call(u,m="GET")
def tra(ma,so=None,gd=None):
    d=get("/api/don/"+ma); r=urllib.request.Request(B+"/api/webhook/sepay",data=json.dumps(dict(content="CK "+ma,transferAmount=so or d["so_tien"],transferType="in",id=gd or "GD"+ma)).encode(),headers={"Content-Type":"application/json","Authorization":"Apikey thu-nghiem"},method="POST")
    urllib.request.urlopen(r); time.sleep(.3); return get("/api/don/"+ma)
def mua(goi,ten,zalo,gt="",ma=""):
    d=call("/api/don",dict(goi=goi,ten=ten,zalo=zalo,gt=gt,ma_giam=ma)); return tra(d["ma"]) if "ma" in d else d
def ok(t,v,k): KQ.append((v==k,t,v,k))
a=mua("bo-tet-99k","Tiệm Hoa Mai","0911111111"); G=a["ma_gt_cua_toi"]; K=a["khoa_gt"]
# 1 giảm 5% qua link
b=mua("khoi-dau","Tiệm Bé Na","0922222222",gt=G); ok("1. Khách mới qua link giảm 5%",b["so_tien"],949000)
# 2 khách quen của B mua tiếp, KHÔNG mở link -> vẫn tính cho A, B giảm 10% (không cộng 5%)
b2=mua("chuan","Tiệm Bé Na","0922222222"); ok("2. B mua lại không có link: giảm 10% khách quen",b2["so_tien"],1791000)
ds=get(f"/api/gioi-thieu/{G}?k={K}")["don"]; ok("2b. Đơn mua lại của B vẫn tính hoa hồng cho A",len(ds),2)
# 3 B mua lại kèm link người khác (C) -> vẫn thuộc A
c=mua("bo-tet-99k","Tiệm Cẩm Tú","0933333333"); Gc=c["ma_gt_cua_toi"]
b3=mua("goi-mua","Tiệm Bé Na","0922222222",gt=Gc); ok("3. B dùng link người khác: hoa hồng vẫn của A",len(get(f"/api/gioi-thieu/{G}?k={K}")["don"]),3)
ok("3b. Người khác (C) không cướp được khách của A",get(f"/api/gioi-thieu/{Gc}?k=x").get("so_don"),0)
# 4 tự giới thiệu: số khác nhưng cùng tên tiệm
s=call("/api/don",dict(goi="khoi-dau",ten="tiem hoa mai",zalo="0999999999",gt=G))
ok("4. Cùng tên tiệm, số Zalo khác: không được giảm 5%",s["so_tien"],999000)
# 5 khách quen A dùng KHAUTRU99 cho 999k: 999k-99k=900k, -10% = 810k
a2=mua("khoi-dau","Tiệm Hoa Mai","0911111111",ma="KHAUTRU99"); ok("5. Khách quen dùng KHAUTRU99: trừ 99k rồi giảm 10%",a2["so_tien"],810000)
# 6 trả thiếu tiền -> không tính
d=call("/api/don",dict(goi="khoi-dau",ten="Tiệm Dung",zalo="0944444444",gt=G)); tra(d["ma"],so=100000)
ok("6. Tiệm bạn chuyển thiếu tiền: không tính hoa hồng",get(f"/api/gioi-thieu/{G}?k={K}")["so_don"],3)
# 7 chưa hết hạn giữ -> chưa chi
ok("7. Chưa qua 7 ngày: chưa chi",call("/api/dev/chay-chi?them_ngay=0")["da_chi"],[])
# 8 qua 7 ngày nhưng chưa có tài khoản -> chờ tài khoản
call("/api/dev/chay-chi?them_ngay=8"); st={x["trang_thai"] for x in get(f"/api/gioi-thieu/{G}?k={K}")["don"]}
ok("8. Qua 7 ngày, chưa có tài khoản: 'cần tài khoản' (đơn thiếu tiền: chờ chuyển đủ)",st,{"cho_tai_khoan","cho_thanh_toan"})
# 9 sai khoá không đổi được tài khoản; không thấy chi tiết
ok("9. Người lạ (sai khoá) không đổi được tài khoản",call(f"/api/gioi-thieu/{G}/tai-khoan",dict(k="sai",bin="970436",stk="0123456789",ten_tk="NGUYEN VAN A",dong_y=True)).get("ok"),None)
ok("9b. Người lạ không xem được chi tiết đơn","don" in get(f"/api/gioi-thieu/{G}?k=sai"),False)
ok("10. Chưa đồng ý điều khoản: không lưu",call(f"/api/gioi-thieu/{G}/tai-khoan",dict(k=K,bin="970436",stk="0123456789",ten_tk="NGUYEN VAN A",dong_y=False)).get("ok"),None)
ok("11. Đủ điều kiện: lưu tài khoản",call(f"/api/gioi-thieu/{G}/tai-khoan",dict(k=K,bin="970436",stk="0123456789",ten_tk="nguyen van a",dong_y=True)).get("ok"),True)
r=call("/api/dev/chay-chi?them_ngay=8"); time.sleep(.3); r2=call("/api/dev/chay-chi?them_ngay=9")
bc=get(f"/api/gioi-thieu/{G}?k={K}")
ok("12. Tự chi đủ 3 đơn, mỗi đơn một lần; đơn chuyển thiếu không chi",sorted(x["trang_thai"] for x in bc["don"]),["cho_thanh_toan"]+["da_chi"]*3)
ok("12b. Chạy lại không chi trùng",r2["da_chi"],[])
tong=round(949000*.15)+round(1791000*.15)+round(1341000*.15)
ok("13. Tổng đã chuyển = 15% × số tiền thực trả của 3 đơn",bc["da_nhan"],tong)
# 14 hoàn tiền trước hạn -> huỷ
d=mua("khoi-dau","Tiệm Em Xinh","0955555555",gt=G)
import sys;sys.path.insert(0,"scripts");import thanh_toan as tt;tt.hoan_tien(d["ma"])
call("/api/dev/chay-chi?them_ngay=10"); x=[y for y in get(f"/api/gioi-thieu/{G}?k={K}")["don"] if y["trang_thai"]=="huy"]
ok("14. Đơn hoàn tiền: hoa hồng tự huỷ, không chi",len(x),1)
# 15 đổi tài khoản -> chờ 3 ngày
call(f"/api/gioi-thieu/{G}/tai-khoan",dict(k=K,bin="970407",stk="1900000001",ten_tk="NGUYEN VAN A",dong_y=True))
e=mua("lam-ho","Tiệm Ngọc Lan","0966666666",gt=G); ok("15a. Đơn 9,99tr qua link: tiệm bạn trả 9.490.000đ",e["so_tien"],9490000)
kho=json.load(open("du_lieu/don_hang.json")); kho[e["ma"]]["tra_luc"]-=8*86400; json.dump(kho,open("du_lieu/don_hang.json","w"),ensure_ascii=False)
call("/api/dev/chay-chi?them_ngay=0"); y=[z for z in get(f"/api/gioi-thieu/{G}?k={K}")["don"] if z["hoa_hong"]==1898000][0]
ok("15b. Vừa đổi tài khoản: giữ 3 ngày rồi mới chi",y["trang_thai"],"cho_het_han_giu")
call("/api/dev/chay-chi?them_ngay=3.1"); y=[z for z in get(f"/api/gioi-thieu/{G}?k={K}")["don"] if z["hoa_hong"]==1898000][0]
ok("15c. Sau 3 ngày tự chi 20% = 1.898.000đ, không trừ thuế (dưới ngưỡng)",(y["trang_thai"],y["thuc_nhan"]),("da_chi",1898000))
for g,t,v,k in KQ: print(("ĐÚNG " if g else "SAI  ")+t+("" if g else f" -> {v} (kỳ vọng {k})"))
print(sum(g for g,*_ in KQ),"/",len(KQ))
