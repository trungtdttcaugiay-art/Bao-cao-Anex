# Quy tắc chi tiết – báo cáo ANEX

## Chữ viết tay trên PDF booking
| Dấu hiệu | Ý nghĩa | Ghi vào báo cáo |
|---|---|---|
| Gạch ngang tên / "cancel" | Hủy | `[NC]*pax`, note "PDF gạch bỏ: hủy" |
| Dấu X | Không đến | `[NC]*pax`, note "PDF gạch X: không đến" |
| "No show" | Không đến | như X |
| Số pax sửa tay | Số sửa thay số in | dùng số sửa, note "PDF sửa tay a→b" |
| "Go show", "+ Hotel N pax" | Khách thêm | Res `'NO RED CODE'`, note "Go show (PDF ghi tay), voucher …" |
| Res No xuống dòng | Chữ số cuối bị rớt | ghép lại đủ 9 số |
| Hai dòng trùng Res (2+2) | Gộp một Res | note "PDF liệt kê 2 dòng trùng Res" |
| Xe supplier (S011, S091…) | Chuyến phụ, Guide `NO GUIDE` | note "Xe supplier" |

## Ghép mã khách (DS bệnh nhân)
- Chỉ nhận mã có **Ngày tạo = ngày báo cáo** (lệch 1 ngày chấp nhận nếu tên khớp rõ + cùng khách sạn + mã đúng dãy).
- Khớp theo khách sạn + tên; họ/tên có thể đảo hoặc sai chính tả.
- Người đi cùng: cùng khách sạn + mã liền kề.
- Không khớp theo tên: dùng dãy mã liền kề và các "lỗ hổng" trong khoảng mã của chuyến/khách sạn; đánh dấu `L` (ô vàng) và nêu rõ là suy ra.
- Độ tin cậy: `H` cao, `M` trung bình (vẫn không tô), `L` thấp → ô vàng.
- Mã trong ảnh tiền nhưng không có trong DS bệnh nhân → hỏi người dùng khách sạn/Res No.
- Người dùng sửa mã khác DS bệnh nhân (vd 11226 = Costabella res 112844453) → theo người dùng.
- Trẻ sơ sinh không có hồ sơ: ghi note, không tạo mã.

## Ảnh bảng tiền
- Ô gộp: mã nằm dưới cùng ô gộp lấy số tiền ở dòng đầu ô gộp.
- Kiểm tra: tổng `AMT` (gồm cả returning/walk-in) = tổng cuối ảnh. Các ngày đã khớp: 156.444.000; 211.844.000; 94.844.500; 90.121.000; 61.919.000.
- Mã bị cắt (vd "160") → đoán theo dãy (11160) và báo người dùng xác nhận.

## Định dạng file mẫu (script tự áp)
- Hàng ngày: ngày 1–12 lưu `datetime(2026, d, 11)` định dạng `mm-dd-yy`; từ ngày 13 người dùng dùng chuỗi `dd/mm/yyyy` → script ghi chuỗi.
- Style lấy từ file nền: dòng ngày (633), dòng chuyến (634), walk-in (696), returning (705, xám), tổng (716, vàng). Nếu file nền đổi layout, kiểm tra các dòng prototype này trong `build_report.py` (`P(633)…P(716)`).
- Nhãn chuyến `8H40\n(S01)` merge cột A và B theo chuyến; C/D/E merge theo Res.
- Returning chưa tra được Res/Hotel → tô cam, `NO RED CODE`/`NO GUIDE`, báo người dùng.

## Lưu ý Windows
- Python: dùng đường dẫn `D:/…`, chạy `python -I -X utf8`.
- Tên file tiếng Việt có thể khác chuẩn Unicode (NFC/NFD) → dùng glob (`Bo*anex*`).
- Heredoc dài trong Bash dễ lỗi → ghi script bằng Write.
