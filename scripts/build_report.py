"""Nap them ngay moi vao file tong hop THANG ANEX (lay file moi nhat user da chinh sua, co ngay 1-13 lam chuan).
- Dong nhat: khach khong co ma / huy / khong den => 'NO COMING' (so khach = so pax tren PDF), nhu ngay 13 cua user.
- Returning: Res No / Guide / Hotel tra theo ma trong cac ngay truoc (ke ca ngay 13 cua user).
- Tong dau trang (E3/G3) cong lai tu moi dong TOTAL AMOUNT.
Chay: python -I -X utf8 build_report.py --days anex_day17.py --pat "<ds benh nhan>.xlsx"
"""
import openpyxl, datetime, copy, glob, os, re
from openpyxl.styles import PatternFill, Alignment

import argparse
ap = argparse.ArgumentParser(description='Nap ngay moi vao file tong hop THANG ANEX')
ap.add_argument('--days', nargs='+', required=True, help='cac file anex_dayNN.py (NN = ngay)')
ap.add_argument('--pat', required=True, help='file Excel danh sach benh nhan (de tim walk-in)')
ap.add_argument('--base', help='file tong hop nen (mac dinh: file moi nhat theo mtime trong --search)')
ap.add_argument('--search', nargs='*', default=[r'C:\Users\Admin\Downloads\TH*ANEX.xlsx', r'D:\BC anex\THANG * - tong hop den *.xlsx'],
                help='glob tim file nen')
ap.add_argument('--outdir', default=r'D:\BC anex')
ap.add_argument('--month', type=int, default=11)
ap.add_argument('--year', type=int, default=2026)
A = ap.parse_args()

MONTH, YEAR = A.month, A.year
DAYS = []
for p_ in A.days:
    m_ = re.search(r'day(\d+)', os.path.basename(p_))
    DAYS.append((int(m_.group(1)), p_))
DAYS.sort()
FROM_DAY, LAST_DAY = DAYS[0][0], DAYS[-1][0]
OUT = os.path.join(A.outdir, 'THANG %d-ANEX - tong hop den %d-%d.xlsx' % (MONTH, LAST_DAY, MONTH))
_cands = [f for g_ in A.search for f in glob.glob(g_) if os.path.abspath(f) != os.path.abspath(OUT)]
BASE = A.base or sorted(_cands, key=os.path.getmtime)[-1]
PATFILE = A.pat
SRC = ''
HOTEL_NAME = {}

wb = openpyxl.load_workbook(BASE)
ws = wb.active
P = lambda r: {c: copy.copy(ws.cell(r, c)._style) for c in range(1, 9)}
S_DATE, S_ROW, S_WALK, S_RET, S_TOT = P(633), P(634), P(696), P(705), P(716)
YEL = PatternFill('solid', fgColor='FFFFE699')
ORG = PatternFill('solid', fgColor='FFF8CBAD')
CENTER_WRAP = Alignment(horizontal='center', vertical='center', wrap_text=True)
CENTER = Alignment(horizontal='center', vertical='center')
L = 'Thấp'

def put(r, st):
    for c in range(1, 9):
        ws.cell(r, c)._style = copy.copy(st[c])

# ---------- chi muc ma -> (ngay, section, guide, res, hotel) tu cac ngay da co
index = {}
def add_index(code, day, sec, guide, res, hotel):
    index.setdefault(code, []).append(dict(day=day, sec=sec, guide=guide, res=res, hotel=hotel))

def block_day(v):
    if isinstance(v, datetime.datetime):
        return v.month if v.day == MONTH else v.day
    if isinstance(v, str) and re.match(r'\d{1,2}/\d{1,2}/\d{4}', v.strip()):
        return int(v.split('/')[0])
    return None

# vi tri bat dau ngay 14 = dong co ngay '14/11/2026' (neu co) hoac dong trong dau tien
start_row = None
day = sec = None
guide = res = hotel = None
last_nonempty = 3
for r in range(4, ws.max_row + 1):
    a = ws.cell(r, 1).value
    if all(ws.cell(r, c).value is None for c in range(1, 9)):
        continue
    last_nonempty = r
    d = block_day(a)
    if d is not None:
        if d >= FROM_DAY:
            start_row = r
            break
        day, sec, guide, res, hotel = d, 'trip', None, None, None
        continue
    if isinstance(a, str):
        s = a.strip().upper()
        if s.startswith('TOTAL'):
            continue
        sec = 'walk' if s.startswith('WALK') else 'ret' if s.startswith('RETURN') else 'trip'
    if ws.cell(r, 2).value is not None: guide = ws.cell(r, 2).value
    if ws.cell(r, 3).value is not None: res = ws.cell(r, 3).value
    if ws.cell(r, 4).value is not None: hotel = ws.cell(r, 4).value
    code = ws.cell(r, 6).value
    if isinstance(code, int):
        add_index(str(code), day, sec, guide, res, (hotel or '').strip() if isinstance(hotel, str) else hotel)
if start_row is None:
    start_row = last_nonempty + 1
for r in range(start_row, ws.max_row + 1):  # xoa dong tam (vd dong ngay 14 trong)
    for c in range(1, 9):
        ws.cell(r, c).value = None

def lookup(code):
    es = index.get(code)
    if not es: return None
    first = [e for e in es if e['sec'] in ('trip', 'walk')]
    return (first or es)[0]

def load_pat(path):
    w = openpyxl.load_workbook(path, read_only=True).active
    out = {}
    for row in w.iter_rows(min_row=2, values_only=True):
        out[str(row[1])] = dict(name=row[2], hotel=(row[9] or '').strip(), date=row[15], note=row[14])
    return out
pat = load_pat(PATFILE)

r = start_row
used_all = set()
summary = []
for dnum, script in DAYS:
    ns = {}
    exec(open(script, encoding='utf-8').read(), ns)
    trips, AMT, RETURNING = ns['trips'], ns['AMT'], ns['RETURNING']
    dstr = '%02d-%02d-%d' % (dnum, MONTH, YEAR)
    put(r, S_DATE); ws.cell(r, 1).value = '%02d/%02d/%d' % (dnum, MONTH, YEAR); r += 1
    start = r
    used = set(used_all)
    for label, slot, gd, ress in trips:
        t0 = r
        for tourist, hotel_, res_, codes, note in ress:
            r0 = r
            for i, (code, conf) in enumerate(codes):
                put(r, S_ROW)
                c = ws.cell(r, 6)
                if code is None or code in ('NO COMING', 'CANCEL'):
                    c.value = 'NO COMING'
                else:
                    c.value = int(code)
                    used.add(code)
                    if conf == L: c.fill = YEL
                    add_index(code, dnum, 'trip', gd, res_, hotel_)
                ws.cell(r, 7).value = AMT.get(code, 0) if code else 0
                if i == 0 and note: ws.cell(r, 8).value = note
                r += 1
            ws.cell(r0, 3).value = res_; ws.cell(r0, 4).value = hotel_; ws.cell(r0, 5).value = len(codes)
            if r - 1 > r0:
                for col in (3, 4, 5): ws.merge_cells(start_row=r0, start_column=col, end_row=r - 1, end_column=col)
        ws.cell(t0, 1).value = label; ws.cell(t0, 2).value = gd
        ws.cell(t0, 1).alignment = CENTER_WRAP; ws.cell(t0, 2).alignment = CENTER
        ws.merge_cells(start_row=t0, start_column=1, end_row=r - 1, end_column=1)
        ws.merge_cells(start_row=t0, start_column=2, end_row=r - 1, end_column=2)
    ret_codes = {x[3] for x in RETURNING}
    # WALK-IN: chi khi co tra tien va khong co trong booking
    walk = {}
    for k, p in sorted(pat.items()):
        if p['date'] == dstr and k not in used and k not in ret_codes and AMT.get(k, 0) > 0:
            walk.setdefault(p['hotel'].title(), []).append(k)
    if walk:
        w0 = r
        for hotel_, cl in walk.items():
            h0 = r
            for k in cl:
                put(r, S_WALK); ws.cell(r, 6).value = int(k); ws.cell(r, 7).value = AMT[k]; r += 1
                add_index(k, dnum, 'walk', 'NO GUIDE', 'NO RED CODE', hotel_)
            ws.cell(h0, 4).value = hotel_; ws.cell(h0, 5).value = len(cl)
            if r - 1 > h0:
                for col in (4, 5): ws.merge_cells(start_row=h0, start_column=col, end_row=r - 1, end_column=col)
        ws.cell(w0, 1).value = 'WALK-IN \nCUSTOMERS'; ws.cell(w0, 2).value = 'NO GUIDE'; ws.cell(w0, 3).value = 'NO RED CODE'
        ws.cell(w0, 1).alignment = CENTER_WRAP
        for col in (1, 2, 3): ws.merge_cells(start_row=w0, start_column=col, end_row=r - 1, end_column=col)
    # RETURNING
    rt0 = r
    unresolved = []
    for gd, rs_, ht, cd, nt, amt in RETURNING:
        e = lookup(cd)
        if e:
            gd2, rs2, ht2 = e['guide'], e['res'], e['hotel']
            gd, rs_, ht = gd2 or gd, (rs2 if rs2 is not None else rs_), ht2 or ht
        if not re.match(r'\d\d/\d\d/\d{4}', nt or ''):
            nt = '%02d/%02d/%d' % (e['day'], MONTH, YEAR) if e else ''
        put(r, S_RET)
        ws.cell(r, 2).value = gd or 'NO GUIDE'
        ws.cell(r, 3).value = ('NO RED CODE' if isinstance(rs_, str) and rs_.strip().upper() == 'NO RED CODE' else (int(rs_) if isinstance(rs_, str) and rs_.isdigit() else rs_)) if rs_ else 'NO RED CODE'
        ws.cell(r, 4).value = ht or None
        if not rs_ or not ht:
            unresolved.append(cd)
            for cc in (2, 3, 4): ws.cell(r, cc).fill = ORG
        ws.cell(r, 5).value = 1; ws.cell(r, 6).value = int(cd); ws.cell(r, 7).value = amt
        ws.cell(r, 8).value = '(' + nt + ')' if nt else None
        r += 1
    ws.cell(rt0, 1).value = 'RETURNING\nCUSTOMERS'; ws.cell(rt0, 1).alignment = CENTER_WRAP
    ws.merge_cells(start_row=rt0, start_column=1, end_row=r - 1, end_column=1)
    end = r - 1
    put(r, S_TOT)
    ws.cell(r, 1).value = 'TOTAL AMOUNT'
    ws.cell(r, 5).value = f'=SUM(E{start}:E{end})'
    ws.cell(r, 7).value = f'=SUM(G{start}:G{end})'
    tot_amt = sum(ws.cell(i, 7).value or 0 for i in range(start, end + 1))
    tot_g = sum(ws.cell(i, 5).value or 0 for i in range(start, end + 1) if isinstance(ws.cell(i, 5).value, (int, float)))
    summary.append((dnum, start, end, r, tot_amt, tot_g, unresolved, sorted(walk)))
    used_all |= used
    r += 1

# dong nhat tong dau trang: cong moi dong TOTAL AMOUNT
tot_rows = [i for i in range(4, ws.max_row + 1) if isinstance(ws.cell(i, 1).value, str) and ws.cell(i, 1).value.strip().upper() == 'TOTAL AMOUNT']
for col in 'EG':
    ws[f'{col}3'].value = '=SUM(' + '+'.join(f'{col}{i}' for i in tot_rows) + ')'
wb.save(OUT)
print('saved', OUT, 'base', os.path.basename(BASE))
for s in summary: print(s)
print('total rows', tot_rows)
