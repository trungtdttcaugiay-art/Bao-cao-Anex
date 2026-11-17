# Vi du GIA (du lieu tu bia) - xem cau truc; du lieu that nam trong examples/anex_day14-16.py (khong dua len GitHub)
AMT = {'10001': 3500000, '10004': 1000000, '10010': 2500000}
H, M, L, NF = 'Cao', 'Trung bình', 'Thấp', 'Không tìm thấy'
NC = ('NO COMING', 'NO COMING')
trips = [
 ('8H40\n(S01)', 'S01', 'MK 100', [
  ('NGUYEN VAN A', 'Hotel Alpha', 100000001, [('10001', H), ('10002', H)], ''),
  ('TRAN THI B', 'Hotel Beta', 100000002, [NC]*2, 'PDF gạch bỏ: hủy'),
 ]),
 ('9H10\n(S02)', 'S02', 'AV 200', [
  ('LE VAN C', 'Hotel Gamma', 100000003, [('10004', H), ('10005', L)], ''),
  ('PHAM D', 'Hotel Delta', 'NO RED CODE', [('10010', H)], 'Go show (PDF ghi tay)'),
 ]),
]

# ---- build main sheet
RETURNING = [  # guide, res, hotel, code, note, tien
 (None, None, '', '09990', '10/11/2026', 0),
]
