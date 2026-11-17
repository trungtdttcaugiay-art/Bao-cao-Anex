# MAU file du lieu 1 ngay: copy thanh anex_dayNN.py (NN = ngay) roi dien.
# Xem examples/anex_day16.py de co vi du day du.

# Ma khach -> so tien (doc tu anh bang tien; ma nam duoi cung o gop thi lay so o dong dau o gop)
AMT = {
    # '11332': 23250000,
}
H, M, L, NF = 'Cao', 'Trung bình', 'Thấp', 'Không tìm thấy'   # do tin cay cua ma (L => o vang)
NC = ('NO COMING', 'NO COMING')                               # khach huy / X / no show / khong co ma

# trips = [ (nhan_gio, slot, guide, [ (ten_khach, khach_san, res_no, [(ma, do_tin_cay), ...], ghi_chu), ... ]), ... ]
#  - nhan_gio: 'HxMM\n(Sxx)' lay tu "DENTAL CLINIC @ hh:mm" tren moi trang PDF, vd '8H40\n(S01)'
#  - res_no  : so 9 chu so (int) hoac 'NO RED CODE' voi Go show
#  - so dong ma = so pax tren PDF; khach huy => [NC]*pax
trips = [
    # ('8H40\n(S01)', 'S01', 'MK 134', [
    #     ('TEN KHACH', 'Ten Khach San', 112962665, [('11644', H)], ''),
    # ]),
]

# ---- build main sheet   (dong nay bat buoc, giu nguyen)
# RETURNING = khach da tao ma tu ngay truoc, quay lai hom nay (co trong anh tien).
# guide/res/hotel de None/'' -> script tu tra theo ma trong file thang; note = ngay tao ho so dd/mm/yyyy.
RETURNING = [  # guide, res, hotel, code, note, tien
    # (None, None, '', '11332', '12/11/2026', 23250000),
]
