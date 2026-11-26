"""Đưa các câu hỏi phổ biến [P] (đã duyệt) từ ngân hàng hỏi đáp lên mục "Hỏi đáp" cuối trang Nailmark.

Nguồn: research/hoi_dap/*.md. Câu có [CHỜ DUYỆT] KHÔNG được đưa lên.
Chạy: python scripts/hoi_dap_web.py  -> cập nhật nailmark/index.html giữa hai mốc <!--HOIDAP--> ... <!--/HOIDAP-->
Thứ tự hiển thị theo THU_TU (cụm từ trong câu hỏi); câu [P] còn lại xếp sau.
"""
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THU_TU = ["Nailmark là gì", "gói nào, giá", "999k được", "Thanh toán xong", "mua tên miền", "đã có tên miền", "người làm hộ", "Tự làm web mất", "Các bước",
          "Năm sau", "Giá có tăng", "tập trung làm", "Đổi giá", "Mã QR", "tăng khách", "lấy thông tin", "người thật hay AI"]


def inline(s):
    s = e(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def md_html(lines):
    out, ul, ol, tbl = [], False, False, []
    def dong():
        nonlocal ul, ol, tbl
        if ul: out.append("</ul>"); ul = False
        if ol: out.append("</ol>"); ol = False
        if tbl:
            rows = [r for r in tbl if not re.match(r"^\|[\s\-|:]+\|$", r)]
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            out.append("<table>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:]) + "</table>")
            tbl = []
    for l in lines:
        s = l.rstrip()
        if s.startswith("|"):
            if ul or ol: dong()
            tbl.append(s); continue
        if tbl: dong()
        m = re.match(r"^\s*[-*] (.+)", s); n = re.match(r"^\s*\d+\. (.+)", s)
        if m:
            if not ul: dong(); out.append("<ul>"); ul = True
            out.append(f"<li>{inline(m.group(1))}</li>")
        elif n:
            if not ol: dong(); out.append("<ol>"); ol = True
            out.append(f"<li>{inline(n.group(1))}</li>")
        elif s.strip():
            dong(); out.append(f"<p>{inline(s.strip())}</p>")
        else:
            dong()
    dong()
    return "".join(out)


def doc_cau():
    ds = []
    for f in sorted((ROOT / "research" / "hoi_dap").glob("*.md")):
        phan = re.split(r"^### ", f.read_text(encoding="utf-8"), flags=re.M)[1:]
        for p in phan:
            tieu, *than = p.split("\n")
            if "[P]" not in tieu or "CHỜ DUYỆT" in p.split("\n---")[0] or "CHỜ DUYỆT" in tieu:
                continue
            body = []
            for l in than:
                if l.startswith("## ") or l.strip() == "---":
                    break
                body.append(l)
            ds.append((tieu.replace("[P]", "").strip(), md_html(body)))
    def hang(q):
        for i, k in enumerate(THU_TU):
            if k.lower() in q.lower():
                return i
        return 99
    return sorted(ds, key=lambda x: hang(x[0]))


def main():
    cau = doc_cau()[:17]
    items = "".join(f"<details><summary>{e(q)}</summary><div class=fa>{a}</div></details>" for q, a in cau)
    sec = (f'<!--HOIDAP--><section class=band id=hoi-dap><div class=in><div class=head><div><div class=eyebrow>Hỏi đáp</div>'
           f'<h2>{len(cau)} câu chủ tiệm <em>hay hỏi nhất</em></h2></div><p class=lead style="margin:0">Câu khác: hỏi trợ lý AI '
           f'hoặc gửi vào buổi hỏi đáp trực tuyến mỗi tuần.</p></div><div class=faq>{items}</div></div></section><!--/HOIDAP-->')
    p = ROOT / "nailmark" / "index.html"
    s = p.read_text(encoding="utf-8")
    if "<!--HOIDAP-->" in s:
        s = re.sub(r"<!--HOIDAP-->.*?<!--/HOIDAP-->", lambda m: sec, s, flags=re.S)
    else:
        s = s.replace("<footer class=band>", sec + "\n<footer class=band>", 1)
        css = (".faq{display:grid;gap:10px}.faq details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px}"
               ".faq summary{cursor:pointer;font-weight:700;font-size:16.5px;list-style:none;display:flex;justify-content:space-between;gap:12px}"
               ".faq summary::-webkit-details-marker{display:none}.faq summary:after{content:'+';color:var(--accent);font-size:22px;line-height:1}"
               ".faq details[open] summary:after{content:'–'}.faq .fa{margin-top:10px;font-size:15px;color:var(--ink)}.faq .fa p{margin:6px 0}"
               ".faq .fa ul,.faq .fa ol{margin:6px 0;padding-left:20px}.faq table{border-collapse:collapse;width:100%;margin:6px 0}"
               ".faq td{border-bottom:1px solid var(--line);padding:6px 4px}.faq td:last-child{text-align:right;font-weight:600}\n")
        s = s.replace(".paths{", css + ".paths{", 1)
    p.write_text(s, encoding="utf-8")
    print(f"Đã đưa {len(cau)} câu lên mục Hỏi đáp:")
    for q, _ in cau:
        print(" -", q)


if __name__ == "__main__":
    main()
