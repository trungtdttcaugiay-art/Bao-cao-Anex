---
name: bao-cao-anex
description: Làm BÁO CÁO NGÀY ANEX "Report on Viet-Xo International Dental Service Usage" cho phòng khám Viet-Xo và nối vào file tổng hợp tháng (THÁNG xx-ANEX.xlsx). Đầu vào mỗi ngày - PDF booking ANEX (bản scan), file Excel danh sách bệnh nhân (Mã hồ sơ = Customer code), ảnh bảng mã + số tiền. Đầu ra - các dòng Date / Guide / Res No / Hotel / Number of Guests / Customer code / Amount paid VND / note theo chuyến (S01, S02...), mục WALK-IN CUSTOMERS, RETURNING CUSTOMERS, TOTAL AMOUNT, tổng đầu trang E3/G3 đồng nhất. Dùng khi người dùng nói "báo cáo ANEX", "làm báo cáo ngày ANEX", "nối ngày mới vào file tháng ANEX", gửi PDF booking anex + danh sách bệnh nhân + ảnh tiền, hoặc gọi /bao-cao-anex.
---

# Skill: Báo cáo ngày ANEX (Viet-Xo)

Người dùng làm báo cáo này mỗi ngày. Tự quyết định theo quy tắc dưới đây, không hỏi lại những điều đã chốt; chỉ hỏi khi thiếu dữ liệu thật sự (vd mã có tiền nhưng không có trong DS bệnh nhân).

## Đầu vào mỗi ngày (người dùng gửi)
1. **PDF "Booking anex <ngày>"** – bản scan, KHÔNG có lớp chữ.
2. **Danh sách bệnh nhân.xlsx** – cột B "Mã hồ sơ" = Customer code, cột "Địa chỉ" = khách sạn (viết tắt), "Ngày tạo".
3. **Ảnh bảng mã + số tiền** (ô gộp) và tổng tiền của ảnh.
4. **File tháng** – bản người dùng tự sửa `Downloads\THÁNG xx-ANEX.xlsx` (có thể có 2 file khác chuẩn Unicode → lấy file mới nhất theo mtime) là **NGUỒN ĐÚNG**. Không ghi đè ngày cũ, chỉ nối ngày mới vào cuối.

## Quy trình
1. **Đọc PDF**: `pip install pymupdf` (nếu thiếu), rồi
   `python -I -X utf8 scripts/render_pdf.py "<pdf>" "<thư_mục_ra>"` → đọc từng PNG bằng Read (xem hình). Mỗi trang = 1 chuyến; guide ở dưới tiêu đề; nhãn giờ lấy từ "DENTAL CLINIC @ hh:mm" (vd `8H40\n(S01)`). Res No bị xuống dòng chữ số cuối → ghép đủ 9 số.
   Chữ viết tay: xem `references/quy-tac.md`.
2. **Ghép mã** từ DS bệnh nhân (chỉ lấy mã có Ngày tạo = ngày báo cáo; khớp khách sạn + tên, tên có thể đảo/sai chính tả; người đi cùng = cùng khách sạn + mã liền kề). Thiếu thông tin → mã thường chạy liên tục từ trên xuống: suy ra từ dãy mã liền kề / "lỗ hổng", tô vàng (`L`).
3. **Đọc ảnh tiền** → `AMT`. Mã nằm dưới cùng ô gộp lấy số của dòng đầu ô gộp. **Tổng phải bằng tổng ảnh** – lệch là sai.
4. **Viết `anex_dayNN.py`** (NN = ngày) từ `scripts/day_template.py`; ví dụ đầy đủ ở `examples/`. Lưu vào thư mục làm việc của người dùng.
5. **Nối vào file tháng**:
   ```
   python -I -X utf8 scripts/build_report.py --days anex_day17.py [anex_day18.py ...] --pat "<ds_benh_nhan.xlsx>" [--base "<file_nền>"] [--outdir "D:\BC anex"] [--month 11 --year 2026]
   ```
   Xuất `THANG <m>-ANEX - tong hop den <ngày>.xlsx` vào `--outdir`. Nền mặc định = file mới nhất trong Downloads (`TH*ANEX.xlsx`) hoặc các file `tong hop den` đã xuất. Nếu nhiều ngày một lần, `--days` liệt kê theo thứ tự; ngày đầu tiên là ngày bắt đầu ghi lại (từ đó trở đi bị xoá và dựng lại).
   Excel đang mở file → PermissionError: đóng file hoặc đổi `--outdir`.
6. **Kiểm tra**: in ra `(ngày, dòng đầu, dòng cuối, dòng TOTAL, tiền, khách, returning chưa tra được, walk-in)`. Đối chiếu tiền với ảnh, số khách với PDF (tính cả NO COMING). Dòng returning không tra được ra ô cam.
7. **Báo cáo cho người dùng**: các ô vàng (mã suy ra), ô cam, mã đọc không chắc (nêu mã cụ thể), khách chưa có hồ sơ/không có mã, Res No cụt chữ số. Liên kết file kết quả. Mở file giúp nếu người dùng nhờ (`start "" "<file>"` qua Bash).

## Quy ước (người dùng đã chốt – xem chi tiết `references/quy-tac.md`)
- Khách không có mã / hủy / gạch X / no show → dòng `NO COMING` (số dòng = số pax PDF, tính vào Number of Guests). Không dùng NOT FOUND/CANCEL.
- **WALK-IN CUSTOMERS** chỉ khi khách **có trả tiền** (mã + số tiền trong ảnh) mà **không có trong booking**.
- **RETURNING CUSTOMERS** = mã tạo từ ngày trước, đến lại hôm nay: E=1 mỗi mã, note `(dd/mm/yyyy)` = ngày tạo/lần đầu xuất hiện; Res/Guide/Hotel tra theo mã trong file tháng (script tự làm). Hàng returning khác màu (xám) so với hàng thường – giữ đúng mẫu cũ.
- Tin file của người dùng hơn DS bệnh nhân khi hai bên mâu thuẫn.
- Tổng đầu trang `E3/G3` = cộng mọi dòng `TOTAL AMOUNT` (script tự dựng lại).
- Mỗi khách có một mã riêng; chỉ làm đúng nội dung file booking.

## Cấu trúc skill
- `scripts/render_pdf.py` – PDF scan → PNG
- `scripts/day_template.py` – mẫu file dữ liệu ngày
- `scripts/build_report.py` – nối ngày mới vào file tháng, giữ style mẫu, dựng tổng
- `examples/anex_day00_mau.py` – ví dụ giả để xem cấu trúc (dữ liệu thật day14-16 chỉ lưu trên máy, không đưa lên GitHub vì có tên khách)
- `references/quy-tac.md` – quy tắc đọc chữ tay, ghép mã, ảnh tiền, định dạng file mẫu
