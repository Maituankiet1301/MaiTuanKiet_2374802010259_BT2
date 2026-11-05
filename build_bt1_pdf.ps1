# Script build_bt1_pdf.ps1: Tạo hồ sơ BT1 hoàn chỉnh và xuất sang PDF
param()

$baseDir = "C:\Users\Admin\OneDrive\Báo Cáo Buổi 4"
Set-Location $baseDir

Write-Host "Đang đọc các file ảnh..."
$b64_arch = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$baseDir\docs\architecture.png"))
$b64_erd = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$baseDir\docs\erd.png"))
$b64_wireframe = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$baseDir\docs\wireframe.png"))
$b64_usecase = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$baseDir\docs\usecase.png"))

Write-Host "Đang biên soạn nội dung HTML hồ sơ BT1..."

$html = @"
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>HỒ SƠ BÀI TẬP 1 (BT1) - MAI TUẤN KIỆT - 2374802010259</title>
<style>
  @page {
    size: A4 portrait;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-center {
      content: counter(page);
      font-size: 9pt;
      color: #64748b;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }
  }

  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }

  /* Cover Page */
  .cover-page {
    page-break-after: always;
    height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    border: 3px double #0284c7;
    padding: 35px 25px;
    box-sizing: border-box;
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  }

  .cover-header {
    border-bottom: 2px solid #0284c7;
    padding-bottom: 15px;
  }
  .cover-header h3 {
    margin: 0;
    font-size: 13pt;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .cover-header h4 {
    margin: 6px 0 0 0;
    font-size: 11pt;
    color: #475569;
    font-weight: 600;
  }

  .cover-title-box {
    margin: 40px 0;
  }
  .cover-badge {
    display: inline-block;
    padding: 6px 16px;
    background: #e0f2fe;
    color: #0369a1;
    font-weight: 700;
    font-size: 11pt;
    border-radius: 20px;
    border: 1px solid #bae6fd;
    margin-bottom: 15px;
    text-transform: uppercase;
  }
  .cover-title {
    font-size: 20pt;
    font-weight: 800;
    color: #0c4a6e;
    line-height: 1.3;
    margin: 10px 0;
    text-transform: uppercase;
  }
  .cover-subtitle {
    font-size: 13pt;
    font-weight: 600;
    color: #0284c7;
    margin: 12px 0 0 0;
  }
  .cover-case-study {
    font-size: 11.5pt;
    color: #334155;
    margin-top: 8px;
    font-style: italic;
  }

  .cover-info-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 5px solid #0284c7;
    border-radius: 8px;
    padding: 18px 24px;
    text-align: left;
    margin: 0 auto;
    width: 82%;
    box-sizing: border-box;
  }
  .cover-info-table {
    width: 100%;
    border-collapse: collapse;
  }
  .cover-info-table td {
    padding: 5px 8px;
    font-size: 10.5pt;
    border: none !important;
  }
  .cover-info-table td.label {
    width: 38%;
    font-weight: 700;
    color: #334155;
  }
  .cover-info-table td.value {
    color: #0f172a;
    font-weight: 600;
  }

  .cover-footer {
    border-top: 1px solid #cbd5e1;
    padding-top: 15px;
    font-size: 10pt;
    color: #64748b;
  }

  /* Document Typography */
  h1 {
    font-size: 15pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 14px;
    text-transform: uppercase;
  }
  .section-break {
    page-break-before: always;
  }
  h2 {
    font-size: 12.5pt;
    font-weight: 700;
    color: #0369a1;
    margin-top: 20px;
    margin-bottom: 10px;
    border-left: 4px solid #0284c7;
    padding-left: 8px;
  }
  h3 {
    font-size: 11pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 8px;
  }
  p {
    margin: 8px 0;
    text-align: justify;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9.5pt;
    page-break-inside: auto;
  }
  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }
  thead {
    display: table-header-group;
  }
  th {
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #334155;
  }
  td {
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }
  tbody tr:nth-child(even) {
    background-color: #f8fafc;
  }

  /* Highlights & Badges */
  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 8.5pt;
  }
  .badge-must { background: #fee2e2; color: #991b1b; border: 1px solid #f87171; }
  .badge-should { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
  .badge-could { background: #e0f2fe; color: #075985; border: 1px solid #7dd3fc; }
  .badge-code { background: #f1f5f9; color: #0f172a; font-family: Consolas, monospace; font-size: 9pt; padding: 1px 5px; }

  /* Callout boxes */
  .callout {
    padding: 12px 16px;
    border-radius: 6px;
    margin: 14px 0;
    font-size: 10pt;
    page-break-inside: avoid;
  }
  .callout-info {
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    color: #0369a1;
  }
  .callout-warn {
    background: #fffbeb;
    border-left: 4px solid #d97706;
    color: #92400e;
  }
  .callout-grain {
    background: #f0fdf4;
    border: 1.5px solid #22c55e;
    border-left: 6px solid #16a34a;
    color: #14532d;
    font-weight: 600;
  }

  /* Image containers */
  .figure-box {
    margin: 16px 0;
    text-align: center;
    page-break-inside: avoid;
  }
  .figure-box img {
    max-width: 98%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06);
  }
  .figure-caption {
    font-size: 9pt;
    font-style: italic;
    color: #475569;
    margin-top: 6px;
  }

  /* Code block */
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: Consolas, 'Fira Code', monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 8px 0;
  }

  /* Table of Contents */
  .toc-list {
    list-style: none;
    padding-left: 0;
    margin: 15px 0;
  }
  .toc-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 10.5pt;
    border-bottom: 1px dotted #94a3b8;
    padding-bottom: 2px;
  }
  .toc-item.level-1 {
    font-weight: 700;
    color: #0f172a;
    margin-top: 10px;
    border-bottom: 1px solid #cbd5e1;
  }
  .toc-item.level-2 {
    padding-left: 20px;
    color: #334155;
    font-weight: 500;
  }
</style>
</head>
<body>

<!-- ================= TRANG BÌA ================= -->
<div class="cover-page">
  <div class="cover-header">
    <h3>BỘ GIÁO DỤC VÀ ĐÀO TẠO — TRƯỜNG ĐẠI HỌC VĂN LANG</h3>
    <h4>KHOA CÔNG NGHỆ THÔNG TIN — BỘ MÔN HỆ THỐNG THÔNG TIN</h4>
  </div>

  <div class="cover-title-box">
    <div class="cover-badge">HỒ SƠ BÁO CÁO BÀI TẬP 1 (BT1)</div>
    <div class="cover-title">ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)<br>&amp; THIẾT KẾ KHO DỮ LIỆU ĐA CHIỀU</div>
    <div class="cover-subtitle">PHÂN HỆ BÁO CÁO DOANH THU &amp; PHÂN TÍCH KINH DOANH CHUỖI BÁN LẺ</div>
    <div class="cover-case-study">Case Study: Mekong Mobile Smart CRM — Phân hệ Luồng L6</div>
  </div>

  <div class="cover-info-card">
    <table class="cover-info-table">
      <tr>
        <td class="label">Sinh viên thực hiện:</td>
        <td class="value">Mai Tuấn Kiệt</td>
      </tr>
      <tr>
        <td class="label">Mã số sinh viên (MSSV):</td>
        <td class="value">2374802010259</td>
      </tr>
      <tr>
        <td class="label">Học phần:</td>
        <td class="value">Chuyên đề tốt nghiệp 1 (Học kỳ 1, Năm học 2026 – 2027)</td>
      </tr>
      <tr>
        <td class="label">Chuyên ngành đào tạo (Track):</td>
        <td class="value">Data Analytics (DA)</td>
      </tr>
      <tr>
        <td class="label">Luồng nghiệp vụ được giao:</td>
        <td class="value">Luồng L6 — Kho dữ liệu bán hàng &amp; Báo cáo doanh thu</td>
      </tr>
      <tr>
        <td class="label">Giảng viên phụ trách:</td>
        <td class="value">TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh</td>
      </tr>
      <tr>
        <td class="label">Kho lưu trữ mã nguồn (GitHub):</td>
        <td class="value"><span class="badge-code">https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2</span></td>
      </tr>
    </table>
  </div>

  <div class="cover-footer">
    Thành phố Hồ Chí Minh — Tháng 11 Năm 2026
  </div>
</div>

<!-- ================= MỤC LỤC ================= -->
<div class="section-break"></div>
<h1>MỤC LỤC BÁO CÁO BT1</h1>
<ul class="toc-list">
  <li class="toc-item level-1"><span>PHẦN 1. GIỚI THIỆU TỔNG QUAN VÀ BỐI CẢNH LUỒNG L6</span><span>Trang 3</span></li>
  <li class="toc-item level-2"><span>1.1. Bối cảnh bài toán chuỗi bán lẻ Mekong Mobile</span><span>Trang 3</span></li>
  <li class="toc-item level-2"><span>1.2. Mục tiêu hệ thống kho dữ liệu và dashboard</span><span>Trang 3</span></li>
  <li class="toc-item level-2"><span>1.3. Phạm vi trong và ngoài (MoSCoW - In Scope vs. WON'T Have)</span><span>Trang 3</span></li>

  <li class="toc-item level-1"><span>PHẦN 2. BẢNG THUẬT NGỮ CHUYÊN NGÀNH THỐNG NHẤT (GLOSSARY)</span><span>Trang 4</span></li>

  <li class="toc-item level-1"><span>PHẦN 3. BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM RÚT GỌN (SRS 6 MỤC)</span><span>Trang 5</span></li>
  <li class="toc-item level-2"><span>3.1. Các bên liên quan và Vai trò người dùng (Stakeholders &amp; Actors)</span><span>Trang 5</span></li>
  <li class="toc-item level-2"><span>3.2. Yêu cầu chức năng (FR1 – FR6)</span><span>Trang 5</span></li>
  <li class="toc-item level-2"><span>3.3. Danh sách User Story chuẩn INVEST kèm tiêu chí AC (GIVEN-WHEN-THEN)</span><span>Trang 6</span></li>
  <li class="toc-item level-2"><span>3.4. Yêu cầu phi chức năng có ngưỡng đo lường định lượng (NFR1 – NFR4)</span><span>Trang 8</span></li>
  <li class="toc-item level-2"><span>3.5. Ràng buộc và Quy tắc nghiệp vụ chuỗi (QT-01 – QT-05)</span><span>Trang 8</span></li>
  <li class="toc-item level-2"><span>3.6. Bảng truy vết yêu cầu (Requirements Traceability Matrix - 100% không ô trống)</span><span>Trang 9</span></li>

  <li class="toc-item level-1"><span>PHẦN 4. SƠ ĐỒ USE CASE VÀ ĐẶC TẢ CHI TIẾT (UML)</span><span>Trang 10</span></li>
  <li class="toc-item level-2"><span>4.1. Sơ đồ Use Case Diagram chuẩn UML</span><span>Trang 10</span></li>
  <li class="toc-item level-2"><span>4.2. Đặc tả chi tiết Use Case UC2: Làm sạch và kiểm tra chất lượng dữ liệu</span><span>Trang 11</span></li>
  <li class="toc-item level-2"><span>4.3. Đặc tả chi tiết Use Case UC4: Xem dashboard doanh thu chi nhánh</span><span>Trang 12</span></li>

  <li class="toc-item level-1"><span>PHẦN 5. THIẾT KẾ KIẾN TRÚC HỆ THỐNG VÀ LUỒNG DỮ LIỆU (DATA FLOW)</span><span>Trang 13</span></li>
  <li class="toc-item level-2"><span>5.1. Sơ đồ kiến trúc phân tầng và luồng luân chuyển dữ liệu L6</span><span>Trang 13</span></li>
  <li class="toc-item level-2"><span>5.2. Mô tả các phân tầng kiến trúc và cơ chế kiểm soát chất lượng</span><span>Trang 14</span></li>
  <li class="toc-item level-2"><span>5.3. Bốn (04) lập luận kiến trúc gắn với NFR và phân tích đánh đổi (Trade-offs)</span><span>Trang 14</span></li>
  <li class="toc-item level-2"><span>5.4. Các thành phần ngoài phạm vi thiết kế (Out of Scope)</span><span>Trang 15</span></li>

  <li class="toc-item level-1"><span>PHẦN 6. MÔ HÌNH DỮ LIỆU PHÂN TÍCH STAR SCHEMA ( Ralph Kimball)</span><span>Trang 16</span></li>
  <li class="toc-item level-2"><span>6.1. Sơ đồ Star Schema (1 Fact Table + 4 Dimension Tables)</span><span>Trang 16</span></li>
  <li class="toc-item level-2"><span>6.2. Phát biểu Grain chuẩn Kimball và lập luận lựa chọn</span><span>Trang 17</span></li>
  <li class="toc-item level-2"><span>6.3. Chi tiết bảng Fact và 4 bảng Dimension</span><span>Trang 17</span></li>
  <li class="toc-item level-2"><span>6.4. Bảng câu hỏi phân tích nghiệp vụ CH1 – CH4</span><span>Trang 18</span></li>
  <li class="toc-item level-2"><span>6.5. Từ điển dữ liệu nguồn với tỷ lệ thiếu (Null Rate) đo đạc thực tế</span><span>Trang 18</span></li>
  <li class="toc-item level-2"><span>6.6. Quy tắc chất lượng dữ liệu có ngưỡng đo lường và truy vấn kiểm chứng (CL1–CL5)</span><span>Trang 19</span></li>
  <li class="toc-item level-2"><span>6.7. Bảng quy tắc biến đổi dữ liệu (ETL Transformation Rules)</span><span>Trang 20</span></li>

  <li class="toc-item level-1"><span>PHẦN 7. THIẾT KẾ GIAO DIỆN DASHBOARD (WIREFRAME 3 MÀN HÌNH)</span><span>Trang 21</span></li>
  <li class="toc-item level-2"><span>7.1. Bản vẽ Wireframe tổng hợp 3 màn hình phân tích</span><span>Trang 21</span></li>
  <li class="toc-item level-2"><span>7.2. Đặc tả màn hình 1: Dashboard Doanh thu chi nhánh theo thời gian (UC4 / US3)</span><span>Trang 22</span></li>
  <li class="toc-item level-2"><span>7.3. Đặc tả màn hình 2: Cơ cấu doanh thu theo nhóm sản phẩm theo quý (UC5 / US5)</span><span>Trang 22</span></li>
  <li class="toc-item level-2"><span>7.4. Đặc tả màn hình 3: So sánh cửa hàng &amp; Cảnh báo giảm 3 tháng liên tiếp (UC6 / US4)</span><span>Trang 23</span></li>
  <li class="toc-item level-2"><span>7.5. Bảng ma trận ánh xạ Wireframe ↔ Chỉ số KPI ↔ Thuộc tính nguồn</span><span>Trang 23</span></li>

  <li class="toc-item level-1"><span>PHẦN 8. KẾ HOẠCH TRIỂN KHAI VÀ CHUẨN BỊ CHO BÀI TẬP 2 (BT2)</span><span>Trang 24</span></li>

  <li class="toc-item level-1"><span>PHẦN 9. PHỤ LỤC: KHAI BÁO CÔNG CỤ AI VÀ CAM KẾT LIÊM CHÍNH HỌC THUẬT</span><span>Trang 25</span></li>
</ul>

<!-- ================= PHẦN 1 ================= -->
<div class="section-break"></div>
<h1>PHẦN 1. GIỚI THIỆU TỔNG QUAN VÀ BỐI CẢNH LUỒNG L6</h1>

<h2>1.1. Bối cảnh bài toán chuỗi bán lẻ Mekong Mobile</h2>
<p>
  <strong>Mekong Mobile</strong> là chuỗi bán lẻ thiết bị di động, máy tính bảng và phụ kiện công nghệ gồm 24 chi nhánh trải rộng tại các tỉnh thành khu vực Đồng bằng sông Cửu Long. Trong suốt quá trình hoạt động giai đoạn 2024 – 2026, các cửa hàng sử dụng phần mềm quản lý bán lẻ độc lập tại điểm bán (cục bộ). Hàng tháng, mỗi chi nhánh xuất dữ liệu giao dịch thành các tệp bảng tính (CSV/Excel) riêng biệt gửi về trung tâm điều hành.
</p>
<p>
  Hiện tại, Ban Giám đốc và các Quản lý chi nhánh đang gặp những rào cản nghiêm trọng trong công tác quản trị dữ liệu:
</p>
<ul>
  <li><strong>Dữ liệu phân tán, không đồng nhất:</strong> Dữ liệu chứa 26 tháng giao dịch (~26.000 đơn hàng, ~48.000 dòng chi tiết sản phẩm) phân mảnh tại 24 nguồn khác nhau.</li>
  <li><strong>Chất lượng dữ liệu suy giảm:</strong> Tồn tại song song 3 định dạng ngày tháng (<span class="badge-code">dd/mm/yyyy</span>, <span class="badge-code">d-m-yy</span>, <span class="badge-code">yyyy.mm.dd</span>), 137 mã đơn hàng bị trùng lặp giữa các chi nhánh khác nhau do hệ thống cục bộ tự sinh mã, số điện thoại khách hàng không đồng nhất định dạng, chuỗi tiền tệ dính ký tự lạ (chữ "đ", dấu phân cách), sai lệch giữa thành tiền và phép nhân số lượng × đơn giá.</li>
  <li><strong>Thiếu công cụ phân tích thời gian thực:</strong> Chưa có kho dữ liệu tập trung và Dashboard trực quan để ban giám đốc phát hiện kịp thời các cửa hàng sụt giảm doanh số hay theo dõi nhóm sản phẩm bán chạy theo mùa vụ.</li>
</ul>

<h2>1.2. Mục tiêu hệ thống</h2>
<p>
  Hệ thống thuộc phân hệ <strong>Luồng L6 – Kho dữ liệu bán hàng và báo cáo doanh thu</strong> giải quyết triệt để bài toán trên thông qua 4 mục tiêu trọng tâm:
</p>
<ol>
  <li><strong>Tự động hóa pipeline trích xuất:</strong> Thu thập dữ liệu định kỳ từ 24 tệp CSV của các cửa hàng vào vùng Staging.</li>
  <li><strong>Chuẩn hóa &amp; Làm sạch dữ liệu tự động:</strong> Loại bỏ dị biệt định dạng, đối soát thành tiền, cách ly 100% dòng lỗi vào bảng Reject với mã lỗi rõ ràng để kiểm toán.</li>
  <li><strong>Mô hình hóa kho dữ liệu Star Schema:</strong> Xây dựng bảng Fact (<span class="badge-code">fact_sales</span>) và 4 bảng Dimension (<span class="badge-code">dim_date</span>, <span class="badge-code">dim_store</span>, <span class="badge-code">dim_product</span>, <span class="badge-code">dim_customer</span>) tối ưu hóa truy vấn phân tích OLAP.</li>
  <li><strong>Xây dựng Dashboard phân tích trực quan:</strong> Dashboard tương tác bằng Streamlit cung cấp 3 góc nhìn phục vụ Quản lý cửa hàng và Ban giám đốc chuỗi.</li>
</ol>

<h2>1.3. Phạm vi trong và ngoài hệ thống (MoSCoW - In Scope vs. WON'T Have)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Phân loại MoSCoW</th>
      <th style="width: 40%;">Nội dung nghiệp vụ / Tính năng</th>
      <th style="width: 40%;">Lý do và Ghi chú kỹ thuật</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="badge badge-must">IN-SCOPE (MUST)</span></td>
      <td>
        • Trích xuất ~26.000 đơn hàng và ~48.000 dòng chi tiết từ 24 chi nhánh vào Staging.<br>
        • Chuẩn hóa ngày ISO-8601, SĐT 10 số, số tiền nguyên VNĐ.<br>
        • Khử trùng lặp qua khóa nghiệp vụ kết hợp <span class="badge-code">(ma_cua_hang, ma_don)</span>.<br>
        • Nạp dữ liệu vào lược đồ Star Schema (DuckDB/PostgreSQL).<br>
        • Dashboard phân tích doanh thu chi nhánh theo ngày/tháng (UC4).
      </td>
      <td>Cốt lõi bài toán Luồng L6 nhằm chuẩn hóa dữ liệu bán lẻ và cung cấp báo cáo doanh số cho cấp quản lý chi nhánh.</td>
    </tr>
    <tr>
      <td><span class="badge badge-should">IN-SCOPE (SHOULD)</span></td>
      <td>
        • Báo cáo so sánh 24 cửa hàng và cảnh báo sụt giảm doanh thu 3 tháng liên tiếp (UC6).<br>
        • Phân tích cơ cấu doanh thu theo nhóm danh mục sản phẩm theo quý (UC5).
      </td>
      <td>Cung cấp góc nhìn chiến lược cho Ban giám đốc ra quyết định điều chuyển hàng hóa và tối ưu chuỗi cung ứng.</td>
    </tr>
    <tr>
      <td><span class="badge badge-could">IN-SCOPE (COULD)</span></td>
      <td>
        • Phân tích tỷ lệ khách hàng quay lại mua lần 2 (Repeat Purchase Rate) qua SĐT chuẩn hóa.
      </td>
      <td>Hỗ trợ bộ phận tiếp thị đánh giá độ trung thành của khách hàng (yêu cầu phụ trợ).</td>
    </tr>
    <tr>
      <td><span class="badge badge-must">OUT-OF-SCOPE (WON'T)</span></td>
      <td>
        • Không xây dựng phần mềm POS tính tiền tại quầy thu ngân.<br>
        • Không quản lý tồn kho vật lý chi tiết tại từng kệ tủ.<br>
        • Không tích hợp cổng thanh toán trực tuyến &amp; ngân hàng.<br>
        • Không tự động gửi tin nhắn SMS/Email thông báo doanh số.
      </td>
      <td>Thuộc phạm vi các hệ thống POS, WMS, ERP khác; kho dữ liệu L6 chỉ tiếp nhận và phân tích dữ liệu bán hàng đã phát sinh.</td>
    </tr>
  </tbody>
</table>

<!-- ================= PHẦN 2 ================= -->
<div class="section-break"></div>
<h1>PHẦN 2. BẢNG THUẬT NGỮ CHUYÊN NGÀNH THỐNG NHẤT (GLOSSARY)</h1>

<p>Để đảm bảo tính nhất quán giữa các tài liệu kỹ thuật, bảng thuật ngữ dưới đây định nghĩa chính xác các khái niệm sử dụng trong toàn bộ đồ án:</p>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Thuật ngữ tiếng Việt</th>
      <th style="width: 25%;">Thuật ngữ tiếng Anh</th>
      <th style="width: 53%;">Định nghĩa &amp; Ý nghĩa kỹ thuật trong Luồng L6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Đơn hàng</strong></td>
      <td>Sales Order / Order</td>
      <td>Một giao dịch mua sắm hoàn tất tại cửa hàng Mekong Mobile, chứa thông tin ngày giao dịch, tổng tiền, mã cửa hàng và khách hàng.</td>
    </tr>
    <tr>
      <td><strong>Dòng chi tiết đơn hàng</strong></td>
      <td>Order Item / Line Item</td>
      <td>Một bản ghi đại diện cho một sản phẩm cụ thể nằm trong một đơn hàng, bao gồm số lượng, đơn giá và thành tiền dòng.</td>
    </tr>
    <tr>
      <td><strong>Chi nhánh / Cửa hàng</strong></td>
      <td>Store / Branch</td>
      <td>Một trong 24 điểm bán lẻ vật lý thuộc hệ thống Mekong Mobile (được mã hóa từ CH01 đến CH24).</td>
    </tr>
    <tr>
      <td><strong>Khách hàng</strong></td>
      <td>Customer</td>
      <td>Người mua hàng, được định danh duy nhất thông qua số điện thoại di động 10 chữ số đã chuẩn hóa.</td>
    </tr>
    <tr>
      <td><strong>Kho dữ liệu</strong></td>
      <td>Data Warehouse (DWH)</td>
      <td>Cơ sở dữ liệu phân tích hướng chủ đề, tích hợp, ổn định theo thời gian, được tổ chức theo mô hình chiều (Star Schema).</td>
    </tr>
    <tr>
      <td><strong>Bảng sự kiện</strong></td>
      <td>Fact Table (<span class="badge-code">fact_sales</span>)</td>
      <td>Bảng trung tâm của kho dữ liệu, chứa các số đo định lượng (doanh thu, số lượng, đơn giá) và các khóa ngoại liên kết tới bảng chiều.</td>
    </tr>
    <tr>
      <td><strong>Bảng chiều</strong></td>
      <td>Dimension Table (<span class="badge-code">dim_*</span>)</td>
      <td>Bảng chứa các thuộc tính mô tả bối cảnh kinh doanh (thời gian, địa điểm, sản phẩm, thông tin khách hàng) phục vụ lọc và phân nhóm.</td>
    </tr>
    <tr>
      <td><strong>Mức chi tiết</strong></td>
      <td>Grain (Granularity)</td>
      <td>Định nghĩa mức độ chi tiết nguyên tử của một dòng trong bảng Fact. Trong L6: một dòng đại diện cho một sản phẩm trong một đơn hàng.</td>
    </tr>
    <tr>
      <td><strong>Vùng tạm nạp</strong></td>
      <td>Staging Area (<span class="badge-code">stg_*</span>)</td>
      <td>Vùng lưu trữ dữ liệu thô trung gian sau khi trích xuất từ 24 file nguồn, giữ nguyên bản chất dữ liệu để phục vụ kiểm toán và xử lý làm sạch.</td>
    </tr>
    <tr>
      <td><strong>Vùng dữ liệu lỗi</strong></td>
      <td>Reject Table (<span class="badge-code">reject_*</span>)</td>
      <td>Bảng cách ly các bản ghi vi phạm quy tắc chất lượng dữ liệu (sai ngày, lệch tiền, sai mã cửa hàng) kèm mã lỗi và thời gian ghi nhận.</td>
    </tr>
    <tr>
      <td><strong>Khóa tự nhiên</strong></td>
      <td>Natural / Business Key</td>
      <td>Khóa định danh nghiệp vụ từ hệ thống nguồn. Trong L6, mã đơn bị trùng nên khóa nghiệp vụ là cặp kết hợp: <span class="badge-code">(ma_cua_hang, ma_don)</span>.</td>
    </tr>
    <tr>
      <td><strong>Khóa đại diện</strong></td>
      <td>Surrogate Key</td>
      <td>Khóa số nguyên tự sinh độc lập với nghiệp vụ (VD: <span class="badge-code">sales_fact_key</span>, <span class="badge-code">store_key</span>) giúp tối ưu hiệu năng join bảng chiều.</td>
    </tr>
    <tr>
      <td><strong>Che dữ liệu</strong></td>
      <td>Data Masking</td>
      <td>Cơ chế ẩn 4 chữ số cuối của số điện thoại (<span class="badge-code">090123****</span>) tại tầng hiển thị nhằm tuân thủ quy định bảo vệ dữ liệu cá nhân.</td>
    </tr>
    <tr>
      <td><strong>Giá trị đơn trung bình</strong></td>
      <td>Average Order Value (AOV)</td>
      <td>Chỉ số đo lường trung bình số tiền thu được trên mỗi đơn hàng: <span class="badge-code">AOV = Tổng doanh thu / Tổng số đơn</span>.</td>
    </tr>
  </tbody>
</table>

<!-- ================= PHẦN 3 ================= -->
<div class="section-break"></div>
<h1>PHẦN 3. BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM RÚT GỌN (SRS)</h1>

<p>Tài liệu đặc tả yêu cầu phần mềm rút gọn tuân thủ tinh thần tiêu chuẩn quốc tế <strong>ISO/IEC/IEEE 29148</strong>, được cô đọng trong 6 mục bắt buộc nhằm đảm bảo tính chặt chẽ và khả năng kiểm chứng.</p>

<h2>3.1. Các bên liên quan và Vai trò người dùng (Stakeholders &amp; User Roles)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 12%;">Mã Actor</th>
      <th style="width: 22%;">Vai trò người dùng</th>
      <th style="width: 38%;">Trách nhiệm và Quyền hạn trong hệ thống</th>
      <th style="width: 28%;">Giới hạn quyền hạn (Không được làm gì)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>ACT-01</strong></td>
      <td><strong>Kỹ sư dữ liệu</strong><br><em>(Data Engineer)</em></td>
      <td>Vận hành và giám sát pipeline ETL; theo dõi dữ liệu cách ly tại bảng reject; bảo trì và sao lưu kho dữ liệu DuckDB/PostgreSQL.</td>
      <td>Không chỉnh sửa trực tiếp số liệu doanh thu đã chốt; không có quyền xem thông tin cá nhân chưa che.</td>
    </tr>
    <tr>
      <td><strong>ACT-02</strong></td>
      <td><strong>Quản lý cửa hàng</strong><br><em>(Store Manager)</em></td>
      <td>Xem báo cáo doanh thu chi nhánh theo ngày/tháng; theo dõi số lượng đơn hàng, AOV và hiệu quả bán lẻ của cửa hàng mình phụ trách.</td>
      <td>Tuyệt đối không xem được dữ liệu doanh thu và khách hàng của 23 cửa hàng còn lại.</td>
    </tr>
    <tr>
      <td><strong>ACT-03</strong></td>
      <td><strong>Ban giám đốc / Giám đốc kinh doanh</strong><br><em>(Executive / Business Director)</em></td>
      <td>Xem báo cáo doanh thu tổng hợp toàn bộ 24 cửa hàng; xem danh sách cảnh báo chi nhánh sụt giảm 3 tháng liên tiếp; phân tích cơ cấu nhóm sản phẩm theo quý.</td>
      <td>Không thao tác trực tiếp vào hạ tầng database và cấu hình kỹ thuật của hệ thống ETL.</td>
    </tr>
    <tr>
      <td><strong>ACT-04</strong></td>
      <td><strong>Hệ thống lập lịch tự động</strong><br><em>(Cron Scheduler / Timer)</em></td>
      <td>Tác nhân hệ thống: Tự động kích hoạt pipeline trích xuất, làm sạch và nạp kho dữ liệu vào lúc 02:00 sáng hàng ngày.</td>
      <td>Không tự ý can thiệp hoặc thay đổi thuật toán làm sạch và logic tính toán doanh thu.</td>
    </tr>
  </tbody>
</table>

<h2>3.2. Danh sách Yêu cầu chức năng (Functional Requirements - FR)</h2>
<ul>
  <li><strong>FR1 (Trích xuất dữ liệu thô vào Staging):</strong> Hệ thống phải có khả năng tự động đọc và nạp toàn bộ dữ liệu từ 24 tệp CSV/Excel bán hàng của các chi nhánh vào các bảng tạm <span class="badge-code">stg_orders</span> và <span class="badge-code">stg_order_items</span> mà không làm mất mát bản ghi nguồn.</li>
  <li><strong>FR2 (Làm sạch và Chuẩn hóa dữ liệu):</strong> Hệ thống phải tự động chuẩn hóa ngày tháng về chuẩn ISO-8601 (<span class="badge-code">YYYY-MM-DD</span>), chuẩn hóa số điện thoại về 10 chữ số, loại bỏ ký tự tiền tệ và khoảng trắng thừa, đồng thời chuyển hướng toàn bộ các dòng lỗi vào bảng <span class="badge-code">reject_orders</span>.</li>
  <li><strong>FR3 (Khử trùng lặp và Xác thực nghiệp vụ):</strong> Hệ thống phải khử trùng lặp đơn hàng dựa trên khóa kết hợp <span class="badge-code">(ma_cua_hang, ma_don)</span> và kiểm tra tính toàn vẹn thành tiền theo công thức <span class="badge-code">|thanh_tien - (so_luong * don_gia)| &le; 1 VNĐ</span>. Các dòng sai lệch phải chuyển vào <span class="badge-code">reject_order_items</span>.</li>
  <li><strong>FR4 (Mô hình hóa và Nạp kho dữ liệu Dimensional Model):</strong> Hệ thống phải nạp dữ liệu sạch vào bảng Fact <span class="badge-code">fact_sales</span> và 4 bảng Dimension (<span class="badge-code">dim_date</span>, <span class="badge-code">dim_store</span>, <span class="badge-code">dim_product</span>, <span class="badge-code">dim_customer</span>) theo cấu trúc Star Schema.</li>
  <li><strong>FR5 (Dashboard phân tích doanh thu cửa hàng):</strong> Hệ thống phải cung cấp giao diện dashboard trực quan cho phép lọc theo ngày, tháng, xem biểu đồ đường doanh thu, KPI Cards và danh sách đơn hàng đã được che 4 số cuối SĐT.</li>
  <li><strong>FR6 (Báo cáo so sánh chi nhánh và Phân tích danh mục sản phẩm):</strong> Hệ thống phải tự động phát hiện và cảnh báo các chi nhánh có doanh thu giảm liên tiếp 3 tháng, đồng thời biểu diễn cơ cấu doanh thu theo nhóm danh mục sản phẩm theo từng quý.</li>
</ul>

<h2>3.3. Danh sách User Story chuẩn INVEST kèm tiêu chí nghiệm thu Acceptance Criteria (GWT)</h2>

<div class="callout callout-info">
  <strong>Ghi chú tiêu chuẩn chất lượng:</strong> Toàn bộ 6 User Story đều tuân thủ nguyên tắc INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) và phân bổ theo thang ưu tiên MoSCoW. Mỗi User Story đều có ít nhất 2 tiêu chí nghiệm thu định dạng GIVEN-WHEN-THEN (bao gồm Happy Path và Luồng ngoại lệ/Validation).
</div>

<h3>US1: Trích xuất dữ liệu bán hàng vào vùng Staging (Mức ưu tiên: MUST)</h3>
<p><em>Là <strong>Kỹ sư dữ liệu</strong>, tôi muốn hệ thống tự động đọc và nạp 24 file dữ liệu đơn hàng từ các chi nhánh vào vùng Staging, để có kho dữ liệu tập trung phục vụ xử lý mà không phải thu thập thủ công.</em></p>
<ul>
  <li><strong>AC1.1 (Luồng chính):</strong> <em>GIVEN</em> 24 file dữ liệu bán hàng tồn tại hợp lệ trong thư mục nguồn, <em>WHEN</em> pipeline kích hoạt, <em>THEN</em> toàn bộ ~26.000 dòng đơn và ~48.000 dòng chi tiết được nạp đủ 100% vào <span class="badge-code">stg_orders</span> và <span class="badge-code">stg_order_items</span>.</li>
  <li><strong>AC1.2 (Ngoại lệ file hỏng/thiếu):</strong> <em>GIVEN</em> một tệp chi nhánh bị lỗi I/O hoặc sai cấu trúc header, <em>WHEN</em> tiến trình đọc file, <em>THEN</em> hệ thống ghi log cảnh báo lỗi tệp, tiếp tục xử lý 23 tệp còn lại và gửi cảnh báo mức High cho kỹ sư dữ liệu.</li>
</ul>

<h3>US2: Làm sạch, chuẩn hóa và kiểm soát chất lượng dữ liệu (Mức ưu tiên: MUST)</h3>
<p><em>Là <strong>Kỹ sư dữ liệu</strong>, tôi muốn tự động chuẩn hóa ngày tháng, số điện thoại và loại bỏ ký tự tiền tệ dị biệt, để dữ liệu đạt chất lượng cao trước khi nạp vào kho phân tích.</em></p>
<ul>
  <li><strong>AC2.1 (Luồng chính chuẩn hóa ngày):</strong> <em>GIVEN</em> cột ngày chứa các dạng <span class="badge-code">dd/mm/yyyy</span>, <span class="badge-code">d-m-yy</span>, <span class="badge-code">yyyy.mm.dd</span>, <em>WHEN</em> bộ parser thực thi, <em>THEN</em> 100% dòng hợp lệ được chuyển về chuẩn ISO-8601 <span class="badge-code">YYYY-MM-DD</span>.</li>
  <li><strong>AC2.2 (Ngoại lệ ngày sai logic):</strong> <em>GIVEN</em> dòng dữ liệu chứa ngày không có thật (VD: 31/02) hoặc ngày trong tương lai, <em>WHEN</em> kiểm tra hợp lệ, <em>THEN</em> dòng đó bị đẩy vào bảng <span class="badge-code">reject_orders</span> với mã lỗi <span class="badge-code">INVALID_DATE_FORMAT</span>.</li>
  <li><strong>AC2.3 (Ngoại lệ lệch thành tiền):</strong> <em>GIVEN</em> dòng chi tiết có <span class="badge-code">thanh_tien != so_luong * don_gia</span> lệch quá 1 VNĐ, <em>WHEN</em> đối soát, <em>THEN</em> dòng đó bị cách ly vào bảng <span class="badge-code">reject_order_items</span> với mã lỗi <span class="badge-code">INCONSISTENT_TOTAL_AMOUNT</span>.</li>
</ul>

<h3>US3: Xem dashboard doanh thu chi nhánh theo ngày và tháng (Mức ưu tiên: MUST)</h3>
<p><em>Là <strong>Quản lý cửa hàng</strong>, tôi muốn xem biểu đồ doanh thu theo ngày và tổng doanh thu tháng của cửa hàng mình, để đánh giá tiến độ kinh doanh kịp thời.</em></p>
<ul>
  <li><strong>AC3.1 (Luồng chính):</strong> <em>GIVEN</em> Quản lý cửa hàng đăng nhập chọn chi nhánh phụ trách và chọn khoảng ngày trong tháng, <em>WHEN</em> mở dashboard, <em>THEN</em> hệ thống render biểu đồ đường doanh thu ngày, thẻ KPI tổng doanh thu, số đơn và AOV trong thời gian dưới 2.5 giây.</li>
  <li><strong>AC3.2 (Ngoại lệ không có dữ liệu):</strong> <em>GIVEN</em> khoảng ngày được chọn chưa phát sinh đơn hàng nào, <em>WHEN</em> truy vấn, <em>THEN</em> dashboard hiển thị thông báo "Không có giao dịch phát sinh trong khoảng thời gian này" và các chỉ số hiển thị 0 VNĐ thay vì bị lỗi chia cho 0 hay NaN.</li>
</ul>

<h3>US4: Báo cáo so sánh cửa hàng và Cảnh báo suy giảm 3 tháng liên tiếp (Mức ưu tiên: SHOULD)</h3>
<p><em>Là <strong>Giám đốc kinh doanh</strong>, tôi muốn xem bảng xếp hạng doanh thu 24 chi nhánh kèm danh sách cảnh báo các cửa hàng sụt giảm doanh thu 3 tháng liên tiếp, để chỉ đạo can thiệp kịp thời.</em></p>
<ul>
  <li><strong>AC4.1 (Luồng chính):</strong> <em>GIVEN</em> Ban giám đốc truy cập mục Báo cáo Hiệu quả Chi nhánh, <em>WHEN</em> áp dụng bộ lọc tháng, <em>THEN</em> hiển thị bảng so sánh doanh thu 24 cửa hàng kèm cờ cảnh báo đỏ cho các chi nhánh có <span class="badge-code">DoanhThu(Tháng N) &lt; DoanhThu(Tháng N-1) &lt; DoanhThu(Tháng N-2)</span>.</li>
  <li><strong>AC4.2 (Ngoại lệ kỳ đầu lịch sử):</strong> <em>GIVEN</em> người dùng chọn tháng 01 hoặc tháng 02 năm 2024 (chưa đủ 3 tháng dữ liệu lịch sử), <em>WHEN</em> tính toán chỉ số, <em>THEN</em> hệ thống hiển thị trạng thái "Chưa đủ dữ liệu kỳ trước" thay vì cảnh báo sai lệch.</li>
</ul>

<h3>US5: Phân tích cơ cấu doanh thu theo nhóm danh mục sản phẩm theo quý (Mức ưu tiên: SHOULD)</h3>
<p><em>Là <strong>Ban giám đốc</strong>, tôi muốn xem biểu đồ tỷ trọng đóng góp doanh thu của các nhóm sản phẩm (điện thoại cao cấp, tầm trung, phụ kiện...) theo từng quý, để tối ưu kế hoạch nhập hàng.</em></p>
<ul>
  <li><strong>AC5.1 (Luồng chính):</strong> <em>GIVEN</em> người dùng chọn năm và quý cần phân tích, <em>WHEN</em> bấm áp dụng lọc, <em>THEN</em> hệ thống hiển thị biểu đồ tròn/cột thể hiện tỷ lệ % doanh thu từng nhóm hàng trên tổng doanh thu quý.</li>
  <li><strong>AC5.2 (Ngoại lệ sản phẩm chưa phân loại):</strong> <em>GIVEN</em> đơn hàng bán sản phẩm chưa có tên trong bảng <span class="badge-code">products.csv</span>, <em>WHEN</em> nạp vào Fact, <em>THEN</em> sản phẩm được gắn vào chiều dự phòng <span class="badge-code">product_key = -1</span> (Tên: "Chưa rõ danh mục") và vẫn được cộng đầy đủ vào tổng tiền.</li>
</ul>

<h3>US6: Phân tích tỷ lệ khách hàng quay lại mua lần 2 (Mức ưu tiên: COULD)</h3>
<p><em>Là <strong>Chuyên viên phân tích dữ liệu</strong>, tôi muốn tính tỷ lệ khách hàng phát sinh đơn hàng thứ 2 (Repeat Purchase Rate) dựa trên số điện thoại, để đánh giá mức độ giữ chân khách hàng.</em></p>
<ul>
  <li><strong>AC6.1 (Luồng chính):</strong> <em>GIVEN</em> kho dữ liệu đã chuẩn hóa số điện thoại khách hàng, <em>WHEN</em> chạy truy vấn tần suất mua hàng, <em>THEN</em> hệ thống hiển thị tỷ lệ % khách có từ 2 đơn hàng trở lên trên tổng số khách duy nhất.</li>
  <li><strong>AC6.2 (Ngoại lệ khách vãng lai rỗng SĐT):</strong> <em>GIVEN</em> các đơn hàng khách vãng lai không để lại số điện thoại (NULL), <em>WHEN</em> tính toán, <em>THEN</em> hệ thống gán vào nhóm khách vãng lai dự phòng (<span class="badge-code">customer_key = 0</span>) và loại khỏi mẫu số tính tỷ lệ quay lại.</li>
</ul>

<h2>3.4. Yêu cầu phi chức năng có ngưỡng đo lường định lượng (NFR)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 10%;">Mã NFR</th>
      <th style="width: 18%;">Thuộc tính chất lượng</th>
      <th style="width: 25%;">Câu hỏi kiểm chứng</th>
      <th style="width: 47%;">Phát biểu yêu cầu có NGƯỠNG ĐO ĐƯỢC cụ thể</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>NFR1</strong></td>
      <td><strong>Hiệu năng xử lý</strong><br><em>(Performance)</em></td>
      <td>Pipeline nạp mất bao lâu? Dashboard tải trong bao lâu?</td>
      <td>
        • Toàn bộ pipeline ETL nạp và làm sạch ~26.000 dòng đơn phải hoàn tất trong <strong>dưới 45 giây</strong> trên máy tính tiêu chuẩn (4 cores, 8GB RAM).<br>
        • Dashboard Streamlit phải phản hồi và render biểu đồ trong <strong>dưới 2.5 giây</strong> đối với truy vấn phạm vi 12 tháng.
      </td>
    </tr>
    <tr>
      <td><strong>NFR2</strong></td>
      <td><strong>Chất lượng dữ liệu</strong><br><em>(Data Quality)</em></td>
      <td>Dữ liệu sau nạp có sạch không? Lỗi được kiểm soát thế nào?</td>
      <td>
        • Tỷ lệ khuyết thiếu (NULL) của các cột cốt lõi (<span class="badge-code">ngay_dat</span>, <span class="badge-code">thanh_tien</span>, <span class="badge-code">ma_cua_hang</span>) trong bảng Fact phải đạt <strong>bằng đúng 0%</strong>.<br>
        • Tỷ lệ thỏa mãn quy tắc nhất quán <span class="badge-code">|thanh_tien - so_luong*don_gia| &le; 1 VNĐ</span> đạt <strong>&ge; 99.5%</strong>. Các dòng vi phạm được cách ly 100% vào bảng Reject.
      </td>
    </tr>
    <tr>
      <td><strong>NFR3</strong></td>
      <td><strong>Bảo mật &amp; Quyền riêng tư</strong><br><em>(Security &amp; Privacy)</em></td>
      <td>Ai được xem số liệu gì? Dữ liệu cá nhân bảo vệ ra sao?</td>
      <td>
        • Mọi số điện thoại khách hàng hiển thị trên Dashboard bắt buộc phải được <strong>che (mask) 4 chữ số cuối</strong> (dạng <span class="badge-code">090123****</span>).<br>
        • Quản lý cửa hàng chỉ xem được số liệu của <strong>đúng 01 chi nhánh</strong> được phân công.
      </td>
    </tr>
    <tr>
      <td><strong>NFR4</strong></td>
      <td><strong>Khả chuyển &amp; Triển khai</strong><br><em>(Portability)</em></td>
      <td>Cài đặt môi trường mất bao lâu và chạy ở đâu?</td>
      <td>
        • Toàn bộ hệ thống kho dữ liệu và Dashboard phải đóng gói chạy được trên Windows, macOS, Linux thông qua Docker Compose với <strong>đúng 02 câu lệnh</strong>: <span class="badge-code">docker compose build</span> và <span class="badge-code">docker compose up</span>.
      </td>
    </tr>
  </tbody>
</table>

<h2>3.5. Ràng buộc và Quy tắc nghiệp vụ chuỗi Mekong Mobile</h2>
<ul>
  <li><strong>QT-01 (Khóa nghiệp vụ kết hợp):</strong> Do các chi nhánh tự đánh số đơn dẫn đến trùng mã giữa các cửa hàng, khóa nghiệp vụ duy nhất bắt buộc phải là bộ kết hợp: <span class="badge-code">(ma_cua_hang, ma_don)</span>. Tuyệt đối không dùng riêng <span class="badge-code">ma_don</span> để join hoặc khử trùng lặp.</li>
  <li><strong>QT-02 (Chuẩn hóa ngày giao dịch):</strong> Chấp nhận đầu vào 3 định dạng ngày, quy chuẩn lưu trữ về ISO-8601 (<span class="badge-code">YYYY-MM-DD</span>). Từ chối và chuyển vào Reject các đơn có ngày lớn hơn ngày hiện tại hoặc trước năm 2020.</li>
  <li><strong>QT-03 (Toàn vẹn tiền tệ):</strong> Thành tiền là số nguyên VNĐ. Cho phép sai số làm tròn tối đa 1 VNĐ: <span class="badge-code">|thanh_tien - (so_luong * don_gia)| &le; 1</span>. Lệch lớn hơn 1 VNĐ phải cách ly vào <span class="badge-code">reject_order_items</span>. Không tự tiện suy diễn khoản chênh lệch là chiết khấu khi nguồn không có cột giảm giá rõ ràng.</li>
  <li><strong>QT-04 (Chuẩn hóa số điện thoại):</strong> SĐT khách hàng phải chuẩn hóa về định dạng viễn thông Việt Nam gồm đúng 10 chữ số (bắt đầu bằng 0). Đổi đầu số quốc tế 84 thành 0. Số không hợp lệ gán cờ <span class="badge-code">is_valid_phone = FALSE</span> và gán vào khách vãng lai khóa 0.</li>
  <li><strong>QT-05 (Toàn vẹn tham chiếu cửa hàng &amp; sản phẩm):</strong> 100% đơn hàng phải có <span class="badge-code">ma_cua_hang</span> tồn tại trong danh mục 24 cửa hàng chính thức. Sản phẩm không có trong từ điển được gán vào mã dự phòng <span class="badge-code">product_key = -1</span> ("Chưa rõ danh mục").</li>
</ul>

<h2>3.6. Bảng truy vết yêu cầu (Requirements Traceability Matrix)</h2>
<div class="callout callout-grain">
  <strong>Cam kết kiểm chứng:</strong> Toàn bộ 6 Yêu cầu chức năng (FR) đều được kết nối chặt chẽ tới ít nhất một User Story, Use Case, phân loại MoSCoW và mã kịch bản kiểm thử (Test Case dự kiến ở BT3). Bảng truy vết đạt 100% đầy đủ, không có ô trống.
</div>

<table>
  <thead>
    <tr>
      <th style="width: 10%;">Mã FR</th>
      <th style="width: 30%;">Nội dung Yêu cầu chức năng</th>
      <th style="width: 12%;">User Story</th>
      <th style="width: 12%;">Use Case</th>
      <th style="width: 12%;">MoSCoW</th>
      <th style="width: 24%;">Test Case dự kiến (BT3)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>FR1</strong></td>
      <td>Trích xuất dữ liệu từ 24 tệp cửa hàng vào Staging</td>
      <td>US1</td>
      <td>UC1</td>
      <td><span class="badge badge-must">MUST</span></td>
      <td><span class="badge-code">TC_ETL_01, TC_ETL_02</span></td>
    </tr>
    <tr>
      <td><strong>FR2</strong></td>
      <td>Làm sạch ngày, SĐT, số tiền, chuyển lỗi vào Reject</td>
      <td>US2</td>
      <td>UC2</td>
      <td><span class="badge badge-must">MUST</span></td>
      <td><span class="badge-code">TC_CLN_01, TC_CLN_02, TC_CLN_03</span></td>
    </tr>
    <tr>
      <td><strong>FR3</strong></td>
      <td>Khử trùng lặp khóa nghiệp vụ và đối soát thành tiền</td>
      <td>US2</td>
      <td>UC2</td>
      <td><span class="badge badge-must">MUST</span></td>
      <td><span class="badge-code">TC_VAL_01, TC_VAL_02</span></td>
    </tr>
    <tr>
      <td><strong>FR4</strong></td>
      <td>Nạp dữ liệu vào bảng Fact và các bảng Dimension</td>
      <td>US1, US2</td>
      <td>UC3</td>
      <td><span class="badge badge-must">MUST</span></td>
      <td><span class="badge-code">TC_DWH_01, TC_DWH_02</span></td>
    </tr>
    <tr>
      <td><strong>FR5</strong></td>
      <td>Dashboard doanh thu chi nhánh theo ngày/tháng có che SĐT</td>
      <td>US3</td>
      <td>UC4</td>
      <td><span class="badge badge-must">MUST</span></td>
      <td><span class="badge-code">TC_DSH_01, TC_DSH_02</span></td>
    </tr>
    <tr>
      <td><strong>FR6</strong></td>
      <td>Báo cáo so sánh cửa hàng, cảnh báo giảm 3 tháng &amp; nhóm hàng</td>
      <td>US4, US5</td>
      <td>UC5, UC6</td>
      <td><span class="badge badge-should">SHOULD</span></td>
      <td><span class="badge-code">TC_ANL_01, TC_ANL_02, TC_ANL_03</span></td>
    </tr>
  </tbody>
</table>

<!-- ================= PHẦN 4 ================= -->
<div class="section-break"></div>
<h1>PHẦN 4. SƠ ĐỒ USE CASE VÀ ĐẶC TẢ CHI TIẾT (UML)</h1>

<h2>4.1. Sơ đồ Use Case Diagram chuẩn UML</h2>
<p>
  Sơ đồ Use Case được thiết kế chuẩn mực theo ký pháp UML, thể hiện rõ ranh giới hệ thống (System Boundary), 4 tác nhân (bao gồm actor hệ thống Cron Scheduler), 6 Use Case nghiệp vụ chính, các quan hệ phụ thuộc <span class="badge-code">&laquo;include&raquo;</span>, <span class="badge-code">&laquo;extend&raquo;</span>, bảng chú thích ký hiệu (Legend) và khung cảnh báo ngoài phạm vi (Out of Scope).
</p>

<div class="figure-box">
  <img src="data:image/png;base64,$b64_usecase" alt="Sơ đồ Use Case Diagram Luồng L6" style="width: 95%;">
  <div class="figure-caption">Hình 4.1: Sơ đồ Use Case Diagram hệ thống Kho dữ liệu bán hàng &amp; Báo cáo doanh thu (Luồng L6)</div>
</div>

<h2>4.2. Đặc tả chi tiết Use Case cốt lõi UC2: Làm sạch, chuẩn hóa và kiểm tra chất lượng dữ liệu</h2>
<table>
  <tr>
    <td style="width: 25%; font-weight: 700; background: #f8fafc;">Tên Use Case:</td>
    <td style="width: 75%; font-weight: 700; color: #0284c7;">UC2: Làm sạch, chuẩn hóa và kiểm tra chất lượng dữ liệu (Data Cleaning &amp; Quality Validation)</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Tác nhân (Actor):</td>
    <td>Kỹ sư dữ liệu (Data Engineer) / Tự động kích hoạt bởi Hệ thống lập lịch (Cron Scheduler).</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Mục tiêu Use Case:</td>
    <td>Xử lý toàn bộ dị biệt dữ liệu nguồn (3 định dạng ngày, trùng mã đơn, chuẩn hóa SĐT, chuỗi tiền tệ dính chữ 'đ') và cách ly 100% dòng lỗi vào bảng Reject trước khi nạp kho.</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Điều kiện tiên quyết (Pre-conditions):</td>
    <td>
      1. Pipeline trích xuất (UC1) đã hoàn tất nạp dữ liệu thô vào <span class="badge-code">stg_orders</span> và <span class="badge-code">stg_order_items</span>.<br>
      2. Các tệp danh mục chuẩn (<span class="badge-code">stores.csv</span>, <span class="badge-code">products.csv</span>) đã sẵn sàng trong hệ thống.
    </td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Điều kiện kết thúc (Post-conditions):</td>
    <td>
      1. Dữ liệu sạch đạt chuẩn được chuẩn bị sẵn sàng để nạp vào bảng Fact và các Dimension.<br>
      2. 100% các dòng không hợp lệ được lưu trữ an toàn trong bảng Reject kèm mã lỗi và thời gian kiểm toán.
    </td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">User Story &amp; Ưu tiên:</td>
    <td>Truy vết: <strong>US2</strong> | Mức ưu tiên: <span class="badge badge-must">MUST</span></td>
  </tr>
</table>

<h3>Luồng sự kiện chính (Happy Path):</h3>
<ol>
  <li>Hệ thống đọc từng lô bản ghi dữ liệu đơn hàng từ bảng tạm <span class="badge-code">stg_orders</span>.</li>
  <li>Hệ thống thực hiện giải mã định dạng ngày tháng qua bộ parser ưu tiên và chuẩn hóa về chuẩn ISO-8601 (<span class="badge-code">YYYY-MM-DD</span>).</li>
  <li>Hệ thống tạo Khóa nghiệp vụ phức hợp duy nhất: <span class="badge-code">store_id || '_' || order_id</span> nhằm giải quyết 137 mã đơn trùng lặp giữa các chi nhánh.</li>
  <li>Hệ thống chuẩn hóa số điện thoại khách hàng (xóa ký tự lạ, chuyển đầu số 84 thành 0, kiểm tra đủ 10 chữ số).</li>
  <li>Hệ thống loại bỏ ký tự tiền tệ ("đ") và dấu phân cách, chuyển đổi trường thành tiền sang số nguyên chuẩn VNĐ.</li>
  <li>Hệ thống kiểm tra tính nhất quán dòng chi tiết: kiểm tra <span class="badge-code">|thanh_tien - (so_luong * don_gia)| &le; 1 VNĐ</span>.</li>
  <li>Hệ thống đối chiếu mã cửa hàng với danh mục 24 cửa hàng chính thức.</li>
  <li>Hệ thống xuất dữ liệu sạch sang bảng tạm chuẩn bị nạp (Ready-to-Load) và ghi nhật ký hoàn tất quy trình làm sạch.</li>
</ol>

<h3>Các luồng ngoại lệ (Exceptions):</h3>
<ul>
  <li><strong>2a. Ngày đặt hàng sai định dạng hoặc giá trị bất hợp lý:</strong> Nếu chuỗi ngày không parse được hoặc có ngày không tồn tại (VD: 31/02) hay ngày trong tương lai &rarr; Hệ thống từ chối nạp bản ghi, đẩy sang bảng <span class="badge-code">reject_orders</span> với mã lỗi <span class="badge-code">INVALID_DATE_FORMAT</span>, pipeline tiếp tục xử lý các bản ghi tiếp theo mà không bị dừng đột ngột.</li>
  <li><strong>4a. Số điện thoại khách hàng không đúng chuẩn:</strong> Nếu chuỗi SĐT ít hơn hoặc nhiều hơn 10 chữ số sau khi chuẩn hóa &rarr; Hệ thống vẫn tiếp nhận đơn hàng nhưng gán cờ <span class="badge-code">is_valid_phone = FALSE</span> và gán <span class="badge-code">customer_key = 0</span> (Khách vãng lai), không làm gián đoạn việc tính doanh thu.</li>
  <li><strong>6a. Chênh lệch thành tiền vượt quá sai số cho phép (&gt; 1 VNĐ):</strong> Nếu <span class="badge-code">|thanh_tien - so_luong * don_gia| &gt; 1</span> &rarr; Hệ thống cách ly dòng chi tiết vào bảng <span class="badge-code">reject_order_items</span> với mã lỗi <span class="badge-code">INCONSISTENT_LINE_TOTAL</span>; ghi log cảnh báo mức High.</li>
  <li><strong>7a. Mã cửa hàng không tồn tại trong danh mục 24 cửa hàng:</strong> Nếu mã cửa hàng nằm ngoài danh mục chuẩn &rarr; Đẩy toàn bộ đơn hàng vào bảng <span class="badge-code">reject_orders</span> với mã lỗi <span class="badge-code">UNKNOWN_STORE_ID</span>.</li>
</ul>

<h2>4.3. Đặc tả chi tiết Use Case cốt lõi UC4: Xem dashboard doanh thu chi nhánh</h2>
<table>
  <tr>
    <td style="width: 25%; font-weight: 700; background: #f8fafc;">Tên Use Case:</td>
    <td style="width: 75%; font-weight: 700; color: #0284c7;">UC4: Xem dashboard doanh thu theo ngày và tháng của cửa hàng (Store Revenue Dashboard)</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Tác nhân (Actor):</td>
    <td>Quản lý cửa hàng (Store Manager) / Ban giám đốc chuỗi.</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Mục tiêu Use Case:</td>
    <td>Cung cấp báo cáo trực quan về doanh số bán hàng, số lượng đơn hoàn tất và so sánh với chỉ tiêu doanh thu theo ngày và tháng của chi nhánh.</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Điều kiện tiên quyết:</td>
    <td>Người dùng đã xác thực vào ứng dụng Dashboard Streamlit; kho dữ liệu đã hoàn tất nạp dữ liệu kỳ mới nhất.</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">Điều kiện kết thúc:</td>
    <td>Giao diện hiển thị đầy đủ biểu đồ đường biểu diễn doanh thu ngày, KPI Cards và bảng chi tiết giao dịch đã che 4 số cuối SĐT.</td>
  </tr>
  <tr>
    <td style="font-weight: 700; background: #f8fafc;">User Story &amp; Ưu tiên:</td>
    <td>Truy vết: <strong>US3</strong> | Mức ưu tiên: <span class="badge badge-must">MUST</span></td>
  </tr>
</table>

<h3>Luồng sự kiện chính (Happy Path):</h3>
<ol>
  <li>Quản lý cửa hàng truy cập màn hình "Báo cáo Doanh thu Chi nhánh".</li>
  <li>Hệ thống tự động nhận diện chi nhánh được phân quyền (hoặc cho phép chọn cửa hàng nếu là Ban giám đốc).</li>
  <li>Người dùng chọn khoảng thời gian cần xem (Từ ngày ... Đến ngày ...).</li>
  <li>Người dùng bấm nút "Áp dụng bộ lọc" (Apply Filter).</li>
  <li>Hệ thống gửi truy vấn SQL tổng hợp đến kho dữ liệu DuckDB/PostgreSQL.</li>
  <li>Hệ thống nhận kết quả trong &lt; 2.5s và hiển thị: KPI Cards (Doanh thu, Đơn hàng, AOV), Biểu đồ đường doanh thu theo ngày, Bảng kê chi tiết đơn hàng (đã che 4 số cuối SĐT dạng <span class="badge-code">090123****</span>).</li>
</ol>

<h3>Các luồng ngoại lệ (Exceptions):</h3>
<ul>
  <li><strong>3a. Khoảng thời gian chọn không hợp lệ (Ngày bắt đầu &gt; Ngày kết thúc):</strong> Dashboard hiển thị cảnh báo đỏ ngay dưới bộ lọc: <em>"Ngày bắt đầu không được lớn hơn ngày kết thúc"</em> và vô hiệu hóa nút Áp dụng bộ lọc.</li>
  <li><strong>5a. Cửa hàng chưa có giao dịch trong kỳ báo cáo đã chọn:</strong> Dashboard hiển thị thông báo trung tính: <em>"Không có giao dịch phát sinh trong khoảng thời gian này"</em>; các chỉ số KPI hiển thị 0 VNĐ thay vì phát sinh lỗi chia cho 0 hoặc NaN.</li>
  <li><strong>6a. Mất kết nối tới cơ sở dữ liệu kho:</strong> Dashboard hiển thị thông báo thân thiện: <em>"Dịch vụ kho dữ liệu tạm thời không phản hồi. Vui lòng thử lại sau ít phút hoặc liên hệ Quản trị viên"</em> kèm mã lỗi dịch vụ.</li>
</ul>

<!-- ================= PHẦN 5 ================= -->
<div class="section-break"></div>
<h1>PHẦN 5. THIẾT KẾ KIẾN TRÚC HỆ THỐNG VÀ LUỒNG DỮ LIỆU</h1>

<h2>5.1. Sơ đồ kiến trúc và luồng dữ liệu L6</h2>
<p>
  Kiến trúc phân hệ Luồng L6 được thiết kế theo mô hình luồng dữ liệu 5 phân tầng hoàn chỉnh, đảm bảo tính tách biệt trách nhiệm, khả năng kiểm toán nguồn gốc dữ liệu (data lineage) và kiểm soát chất lượng nghiêm ngặt trước khi nạp vào kho dữ liệu.
</p>

<div class="figure-box">
  <img src="data:image/png;base64,$b64_arch" alt="Sơ đồ Kiến trúc và Luồng dữ liệu Luồng L6" style="width: 95%;">
  <div class="figure-caption">Hình 5.1: Sơ đồ kiến trúc 5 tầng và luồng luân chuyển dữ liệu Luồng L6 — Mekong Mobile</div>
</div>

<h2>5.2. Mô tả các phân tầng kiến trúc</h2>
<ol>
  <li><strong>Tầng nguồn dữ liệu (Data Source Layer):</strong> Tiếp nhận 24 tệp CSV bán lẻ định kỳ từ 24 chi nhánh và các tệp danh mục chuẩn (<span class="badge-code">orders_2024_2026.csv</span>, <span class="badge-code">order_items.csv</span>, <span class="badge-code">products.csv</span>, <span class="badge-code">stores.csv</span>). Khi nạp, pipeline gắn thẻ mã cửa hàng vào từng dòng chi tiết để bảo toàn ngữ cảnh.</li>
  <li><strong>Tầng nạp và điều phối (Ingestion &amp; Staging Layer):</strong> Bộ lập lịch Cron kích hoạt pipeline lúc 02:00 sáng. Dữ liệu nguồn được đọc theo lô vào các bảng tạm Staging (<span class="badge-code">stg_orders</span>, <span class="badge-code">stg_order_items</span>) mà không can thiệp thay đổi giá trị gốc, phục vụ đối soát.</li>
  <li><strong>Tầng làm sạch, xác thực và Vùng cách ly lỗi (Data Cleaning, Validation &amp; Reject Layer):</strong> Áp dụng các bộ parser và regex chuẩn hóa ngày, số điện thoại, tiền tệ; đối soát thành tiền và kiểm tra toàn vẹn tham chiếu. Dòng hợp lệ chuyển tiếp sang tầng kho; 100% dòng vi phạm được đẩy vào bảng <span class="badge-code">reject_orders</span> và <span class="badge-code">reject_order_items</span> kèm mã lỗi và dấu thời gian.</li>
  <li><strong>Tầng kho dữ liệu đa chiều (Data Warehouse Layer):</strong> Lưu trữ dữ liệu sạch theo mô hình Star Schema trên DuckDB (hỗ trợ PostgreSQL khi mở rộng), gồm 1 bảng Fact (<span class="badge-code">fact_sales</span>) và 4 bảng chiều (<span class="badge-code">dim_date</span>, <span class="badge-code">dim_store</span>, <span class="badge-code">dim_product</span>, <span class="badge-code">dim_customer</span>).</li>
  <li><strong>Tầng trình bày và phân tích (Presentation &amp; Dashboard Layer):</strong> Ứng dụng Streamlit truy vấn kho dữ liệu thông qua Lớp truy cập dữ liệu (Data Access Layer). Lớp này thực thi kiểm soát phân quyền (Quản lý cửa hàng chỉ xem 01 chi nhánh) và tự động che 4 chữ số cuối số điện thoại khách hàng.</li>
</ol>

<h2>5.3. Bốn (04) lập luận kiến trúc gắn với NFR và phân tích đánh đổi (Trade-offs)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Mã NFR liên quan</th>
      <th style="width: 35%;">Quyết định kiến trúc lựa chọn</th>
      <th style="width: 25%;">Lợi ích mang lại</th>
      <th style="width: 25%;">Đánh đổi &amp; Biện pháp khắc phục</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>NFR1 (Hiệu năng)<br>&lt; 45s ETL, &lt; 2.5s UI</strong></td>
      <td>Chọn pipeline xử lý theo lô trong một tiến trình (Single-process Batch ETL) kết hợp DuckDB embedded in-process thay vì tách nhiều microservices.</td>
      <td>Loại bỏ độ trễ mạng và chi phí vận hành container phức tạp; tốc độ đọc/ghi cột của DuckDB cực nhanh trên tập ~26.000 dòng.</td>
      <td><strong>Đánh đổi:</strong> Tiến trình đơn nếu gặp lỗi nghiêm trọng có thể ảnh hưởng cả mẻ chạy.<br><strong>Khắc phục:</strong> Cơ chế try-catch, ghi log audit và khả năng chạy lại an toàn (idempotency).</td>
    </tr>
    <tr>
      <td><strong>NFR2 (Chất lượng)<br>Null = 0%, Khớp &ge; 99.5%</strong></td>
      <td>Thiết kế Cổng kiểm soát chất lượng (Quality Gate) với vùng cách ly lỗi (Reject Table) riêng biệt trước khi nạp Fact, thay vì âm thầm thay giá trị mặc định.</td>
      <td>Bảo toàn khả năng kiểm toán nguồn gốc; bảng Fact luôn giữ độ sạch 100% không bị ô nhiễm bởi dữ liệu rác.</td>
      <td><strong>Đánh đổi:</strong> Các bản ghi lỗi chưa hiển thị ngay trên báo cáo doanh thu.<br><strong>Khắc phục:</strong> Cung cấp báo cáo Reject cho Kỹ sư dữ liệu đối soát và nạp bù.</td>
    </tr>
    <tr>
      <td><strong>NFR3 (Bảo mật)<br>Masking SĐT, Cửa hàng</strong></td>
      <td>Áp dụng phân quyền và che số điện thoại tại Lớp truy cập dữ liệu (Data Access Layer) trước khi trả về UI, tạo trường <span class="badge-code">phone_masked</span> riêng.</td>
      <td>Triệt tiêu nguy cơ lộ dữ liệu cá nhân qua API hoặc giao diện báo cáo; tuân thủ quy định bảo vệ dữ liệu.</td>
      <td><strong>Đánh đổi:</strong> Phải quản lý bảng ánh xạ người dùng – chi nhánh và kiểm thử mọi nhánh truy vấn.<br><strong>Khắc phục:</strong> Áp dụng role-based filter nhất quán tại tầng DAL.</td>
    </tr>
    <tr>
      <td><strong>NFR4 (Khả chuyển)<br>2 lệnh Docker</strong></td>
      <td>Đóng gói trọn gói DuckDB, Python ETL và Streamlit trong một cấu hình Docker Compose đồng nhất.</td>
      <td>Đảm bảo môi trường chạy ổn định 100% trên Windows, macOS, Linux chỉ với 2 lệnh <span class="badge-code">build</span> và <span class="badge-code">up</span>.</td>
      <td><strong>Đánh đổi:</strong> DuckDB phù hợp truy vấn phân tích đơn nút, không hỗ trợ ghi đồng thời từ nhiều service phân tán.<br><strong>Khắc phục:</strong> Sẵn sàng cấu trúc schema tương thích để chuyển sang PostgreSQL khi cần quy mô lớn.</td>
    </tr>
  </tbody>
</table>

<h2>5.4. Các thành phần ngoài phạm vi thiết kế (Out of Scope)</h2>
<p>
  Hệ thống L6 chủ ý không thiết kế các thành phần: Máy bán hàng POS tại quầy, Cổng thanh toán trực tuyến, Hệ thống quản lý tồn kho vật lý tại kho tổng, và Hạ tầng đám mây phân tán đa cụm. Những thành phần này thuộc các bài toán nghiệp vụ khác và không nằm trong mục tiêu của bài tập phân tích kho dữ liệu bán hàng.
</p>

<!-- ================= PHẦN 6 ================= -->
<div class="section-break"></div>
<h1>PHẦN 6. MÔ HÌNH DỮ LIỆU PHÂN TÍCH STAR SCHEMA</h1>

<h2>6.1. Sơ đồ mô hình Star Schema</h2>
<p>
  Mô hình dữ liệu phân tích của Luồng L6 được thiết kế theo đúng chuẩn lược đồ hình sao (Star Schema) của Ralph Kimball, gồm 01 bảng Fact trung tâm liên kết với 04 bảng Dimension thông qua các khóa ngoại.
</p>

<div class="figure-box">
  <img src="data:image/png;base64,$b64_erd" alt="Sơ đồ Mô hình Star Schema Luồng L6" style="width: 92%;">
  <div class="figure-caption">Hình 6.1: Lược đồ hình sao (Star Schema) phân hệ Kho dữ liệu bán hàng Luồng L6</div>
</div>

<h2>6.2. Phát biểu mức chi tiết (GRAIN) và Lập luận thiết kế</h2>
<div class="callout callout-grain">
  <strong>PHÁT BIỂU GRAIN CHUẨN RALPH KIMBALL:</strong><br>
  "Một dòng trong bảng <span class="badge-code">fact_sales</span> đại diện cho MỘT MẶT HÀNG (DÒNG CHI TIẾT SẢN PHẨM) trong MỘT ĐƠN HÀNG, được bán tại MỘT CỬA HÀNG vào MỘT NGÀY cụ thể."
</div>
<p>
  <strong>Lập luận lựa chọn mức Grain này:</strong>
</p>
<ul>
  <li>Câu hỏi phân tích nghiệp vụ <strong>CH4</strong> yêu cầu: <em>"Nhóm danh mục sản phẩm nào đóng góp doanh thu lớn nhất theo từng quý?"</em>. Nếu thiết kế grain ở mức tổng hợp đơn hàng ("mỗi dòng là một đơn hàng"), hệ thống sẽ đánh mất toàn bộ thông tin về sản phẩm và không thể phân tích cơ cấu mặt hàng theo quý.</li>
  <li>Mức grain chi tiết nhất (Line Item Level) cho phép trả lời linh hoạt mọi góc nhìn phân tích: tổng hợp theo ngày, theo tháng, theo cửa hàng, theo danh mục sản phẩm, hoặc theo hành vi khách hàng mua lặp lại mà không làm méo mó số liệu.</li>
</ul>

<h2>6.3. Chi tiết cấu trúc Bảng Fact và 4 Bảng Dimension</h2>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Tên bảng</th>
      <th style="width: 15%;">Loại bảng</th>
      <th style="width: 45%;">Thuộc tính và Khóa chính / Khóa ngoại</th>
      <th style="width: 25%;">Ý nghĩa phân tích &amp; Vai trò</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="badge-code">fact_sales</span></td>
      <td>Bảng sự kiện<br>(Fact Table)</td>
      <td>
        • <span class="badge-code">sales_fact_key BIGINT PK</span> (Khóa thay thế)<br>
        • <span class="badge-code">date_key INTEGER FK</span> (tham chiếu dim_date)<br>
        • <span class="badge-code">store_key BIGINT FK</span> (tham chiếu dim_store)<br>
        • <span class="badge-code">product_key BIGINT FK</span> (tham chiếu dim_product)<br>
        • <span class="badge-code">customer_key BIGINT FK</span> (tham chiếu dim_customer)<br>
        • <span class="badge-code">order_id VARCHAR(50)</span>, <span class="badge-code">order_line_number INT</span><br>
        • Số đo: <span class="badge-code">quantity INT</span>, <span class="badge-code">unit_price BIGINT</span>, <span class="badge-code">line_total BIGINT</span>, <span class="badge-code">discount_amount BIGINT</span>
      </td>
      <td>Lưu trữ các số đo định lượng doanh thu bán lẻ ở mức chi tiết sản phẩm. Lưu mã đơn và lineage để đối soát.</td>
    </tr>
    <tr>
      <td><span class="badge-code">dim_date</span></td>
      <td>Bảng chiều<br>(Dimension)</td>
      <td>
        • <span class="badge-code">date_key INTEGER PK</span> (Định dạng YYYYMMDD)<br>
        • <span class="badge-code">full_date DATE</span>, <span class="badge-code">day_of_month INT</span>, <span class="badge-code">month_number INT</span>, <span class="badge-code">quarter_number INT</span>, <span class="badge-code">year_number INT</span>, <span class="badge-code">day_name VARCHAR(15)</span>
      </td>
      <td>Hỗ trợ lọc và tổng hợp đa cấp thời gian: ngày, tuần, tháng, quý, năm.</td>
    </tr>
    <tr>
      <td><span class="badge-code">dim_store</span></td>
      <td>Bảng chiều<br>(Dimension)</td>
      <td>
        • <span class="badge-code">store_key BIGINT PK</span> (Khóa thay thế)<br>
        • <span class="badge-code">store_id INT</span> (Mã nghiệp vụ: 1 đến 24)<br>
        • <span class="badge-code">store_code VARCHAR(10)</span> (VD: CH01..CH24)<br>
        • <span class="badge-code">store_name VARCHAR(150)</span>, <span class="badge-code">region_name VARCHAR(50)</span>
      </td>
      <td>Chi nhánh bán lẻ phát sinh giao dịch; hỗ trợ phân quyền hiển thị theo cửa hàng.</td>
    </tr>
    <tr>
      <td><span class="badge-code">dim_product</span></td>
      <td>Bảng chiều<br>(Dimension)</td>
      <td>
        • <span class="badge-code">product_key BIGINT PK</span> (Khóa thay thế)<br>
        • <span class="badge-code">product_id VARCHAR(50)</span> (Mã nghiệp vụ)<br>
        • <span class="badge-code">product_name VARCHAR(200)</span>, <span class="badge-code">normalized_name VARCHAR(200)</span><br>
        • <span class="badge-code">category_name VARCHAR(100)</span><br>
        • <em>Có bản ghi dự phòng: product_key = -1 ("Chưa rõ danh mục")</em>
      </td>
      <td>Phân nhóm thiết bị: Điện thoại cao cấp, tầm trung, phụ kiện sạc, tai nghe phục vụ phân tích cơ cấu doanh thu theo quý.</td>
    </tr>
    <tr>
      <td><span class="badge-code">dim_customer</span></td>
      <td>Bảng chiều<br>(Dimension)</td>
      <td>
        • <span class="badge-code">customer_key BIGINT PK</span> (Khóa thay thế)<br>
        • <span class="badge-code">normalized_phone VARCHAR(15)</span> (Nhạy cảm)<br>
        • <span class="badge-code">phone_masked VARCHAR(15)</span> (Hiển thị UI: 090123****)<br>
        • <span class="badge-code">is_valid_phone BOOLEAN</span><br>
        • <em>Có bản ghi dự phòng: customer_key = 0 ("Khách vãng lai")</em>
      </td>
      <td>Định danh khách hàng qua số điện thoại để phân tích tỷ lệ khách quay lại mua lần 2 (Repeat Rate).</td>
    </tr>
  </tbody>
</table>

<h2>6.4. Bảng câu hỏi phân tích nghiệp vụ</h2>
<table>
  <thead>
    <tr>
      <th style="width: 10%;">Mã CH</th>
      <th style="width: 35%;">Câu hỏi phân tích nghiệp vụ</th>
      <th style="width: 25%;">Nhu cầu thực tế từ lãnh đạo chuỗi</th>
      <th style="width: 18%;">Mức chi tiết (Grain)</th>
      <th style="width: 12%;">User Story</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CH1</strong></td>
      <td>Doanh thu của từng cửa hàng theo từng ngày và từng tháng là bao nhiêu?</td>
      <td>Giám đốc: "Theo dõi tiến độ doanh số chi nhánh so với chỉ tiêu tháng"</td>
      <td>Cửa hàng + Ngày / Tháng</td>
      <td><strong>US3</strong></td>
    </tr>
    <tr>
      <td><strong>CH2</strong></td>
      <td>Những cửa hàng nào có doanh thu sụt giảm liên tiếp trong 3 tháng gần nhất?</td>
      <td>Ban giám đốc: "Cảnh báo sớm chi nhánh suy yếu để điều chỉnh kinh doanh"</td>
      <td>Cửa hàng + 3 tháng liên tiếp</td>
      <td><strong>US4</strong></td>
    </tr>
    <tr>
      <td><strong>CH3</strong></td>
      <td>Tỷ lệ khách hàng quay lại mua hàng lần thứ hai (Repeat Purchase Rate) là bao nhiêu?</td>
      <td>Tiếp thị &amp; CSKH: "Đo lường mức độ giữ chân khách hàng qua SĐT"</td>
      <td>Khách hàng (SĐT) + Lịch sử đơn</td>
      <td><strong>US6</strong></td>
    </tr>
    <tr>
      <td><strong>CH4</strong></td>
      <td>Nhóm danh mục sản phẩm nào đóng góp tỷ trọng doanh thu lớn nhất theo từng quý?</td>
      <td>Chuỗi cung ứng: "Nắm bắt thị hiếu sản phẩm bán chạy theo mùa vụ"</td>
      <td>Nhóm sản phẩm + Quý</td>
      <td><strong>US5</strong></td>
    </tr>
  </tbody>
</table>

<h2>6.5. Từ điển dữ liệu nguồn (Data Dictionary) với tỷ lệ thiếu đo đạc thực tế</h2>
<p>
  Tỷ lệ khuyết thiếu (Null Rate) dưới đây là số liệu đo đạc thực nghiệm trên tập dữ liệu lịch sử (~26.000 dòng đơn và ~48.000 dòng chi tiết) bằng lệnh Python <span class="badge-code">df.isna().mean()</span>:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 15%;">Tệp nguồn</th>
      <th style="width: 15%;">Cột nguồn</th>
      <th style="width: 15%;">Kiểu dữ liệu thực</th>
      <th style="width: 25%;">Hiện trạng &amp; Vấn đề ghi nhận</th>
      <th style="width: 15%;">Tỷ lệ thiếu (Đo được)</th>
      <th style="width: 15%;">Kiểu đích (DWH)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="5"><span class="badge-code">orders_2024_2026.csv</span><br>(~26.000 dòng)</td>
      <td><span class="badge-code">Ngay</span></td>
      <td>String</td>
      <td>3 định dạng lẫn lộn: dd/mm/yyyy, d-m-yy, yyyy.mm.dd</td>
      <td><strong>0.4%</strong></td>
      <td><span class="badge-code">DATE</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">Ma don</span></td>
      <td>String</td>
      <td>Có 137 mã đơn bị trùng lặp giữa 24 chi nhánh</td>
      <td><strong>0.0%</strong></td>
      <td><span class="badge-code">VARCHAR(50)</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">SDT</span></td>
      <td>String</td>
      <td>Lẫn khoảng trắng, dấu chấm, đầu số 84 hoặc 0</td>
      <td><strong>6.2%</strong></td>
      <td><span class="badge-code">VARCHAR(15)</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">Thanh tien</span></td>
      <td>String / Number</td>
      <td>Có 218 dòng bị lưu dính chữ "đ" phía sau số tiền</td>
      <td><strong>1.1%</strong></td>
      <td><span class="badge-code">BIGINT</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">Ma cua hang</span></td>
      <td>String / Number</td>
      <td>Mã cửa hàng từ CH01 đến CH24 (hoặc số 1 đến 24)</td>
      <td><strong>0.0%</strong></td>
      <td><span class="badge-code">INTEGER</span></td>
    </tr>
    <tr>
      <td rowspan="4"><span class="badge-code">order_items.csv</span><br>(~48.000 dòng)</td>
      <td><span class="badge-code">ma_don</span></td>
      <td>String</td>
      <td>Mã đơn hàng đối soát với bảng orders</td>
      <td><strong>0.0%</strong></td>
      <td><span class="badge-code">VARCHAR(50)</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">ma_san_pham</span></td>
      <td>String</td>
      <td>Tham chiếu danh mục sản phẩm</td>
      <td><strong>0.2%</strong></td>
      <td><span class="badge-code">VARCHAR(50)</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">so_luong</span></td>
      <td>Integer</td>
      <td>Số lượng sản phẩm mua (số nguyên &gt; 0)</td>
      <td><strong>0.0%</strong></td>
      <td><span class="badge-code">INTEGER</span></td>
    </tr>
    <tr>
      <td><span class="badge-code">thanh_tien</span></td>
      <td>Integer</td>
      <td>Thành tiền dòng chi tiết (= số lượng * đơn giá)</td>
      <td><strong>0.0%</strong></td>
      <td><span class="badge-code">BIGINT</span></td>
    </tr>
  </tbody>
</table>

<h2>6.6. Quy tắc chất lượng dữ liệu có ngưỡng đo lường và câu truy vấn kiểm chứng (CL1 – CL5)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 10%;">Mã CL</th>
      <th style="width: 20%;">Chiều chất lượng</th>
      <th style="width: 32%;">Quy tắc nghiệp vụ và NGƯỠNG ĐO ĐƯỢC</th>
      <th style="width: 38%;">Câu lệnh SQL kiểm chứng (Validation Query)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CL1</strong></td>
      <td><strong>Tính đầy đủ</strong><br><em>(Completeness)</em></td>
      <td>Sau khi làm sạch, tỷ lệ khuyết thiếu (NULL) của các cột cốt lõi <span class="badge-code">date_key</span> và <span class="badge-code">line_total</span> trong <span class="badge-code">fact_sales</span> phải <strong>bằng đúng 0%</strong>.</td>
      <td>
        <pre>SELECT COUNT(*) FROM fact_sales 
WHERE date_key IS NULL 
   OR line_total IS NULL;
-- Kết quả kỳ vọng: 0 dòng vi phạm</pre>
      </td>
    </tr>
    <tr>
      <td><strong>CL2</strong></td>
      <td><strong>Tính hợp lệ</strong><br><em>(Validity)</em></td>
      <td><strong>100%</strong> giá trị ngày giao dịch nạp vào kho phải quy đổi thành công về chuẩn ISO-8601 (<span class="badge-code">YYYY-MM-DD</span>).</td>
      <td>
        <pre>SELECT COUNT(*) FROM fact_sales 
WHERE TRY_STRPTIME(CAST(date_key AS VARCHAR), 
                   '%Y%m%d') IS NULL;
-- Kết quả kỳ vọng: 0 dòng lỗi</pre>
      </td>
    </tr>
    <tr>
      <td><strong>CL3</strong></td>
      <td><strong>Tính duy nhất</strong><br><em>(Uniqueness)</em></td>
      <td>Khóa nghiệp vụ kết hợp <span class="badge-code">(store_id, order_id)</span> phải là duy nhất <strong>100%</strong> trong bảng đơn hàng sạch.</td>
      <td>
        <pre>SELECT store_id || '_' || order_id, 
       COUNT(*) FROM stg_orders 
GROUP BY 1 HAVING COUNT(*) > 1;
-- Kết quả kỳ vọng: Không có dòng trùng</pre>
      </td>
    </tr>
    <tr>
      <td><strong>CL4</strong></td>
      <td><strong>Tính nhất quán</strong><br><em>(Consistency)</em></td>
      <td>Quy tắc: <span class="badge-code">|thanh_tien - (so_luong * don_gia)| &le; 1 VNĐ</span> phải đạt tỷ lệ thỏa mãn <strong>&ge; 99.5%</strong> trên toàn bộ dòng chi tiết.</td>
      <td>
        <pre>SELECT (COUNT(CASE WHEN ABS(thanh_tien - 
       so_luong*don_gia) <= 1 THEN 1 END)*100.0 
       / COUNT(*)) FROM stg_order_items;
-- Kết quả kỳ vọng: >= 99.5%</pre>
      </td>
    </tr>
    <tr>
      <td><strong>CL5</strong></td>
      <td><strong>Toàn vẹn tham chiếu</strong><br><em>(Referential Integrity)</em></td>
      <td><strong>100%</strong> mã cửa hàng trong bảng Fact phải tham chiếu thành công vào danh mục 24 cửa hàng chuẩn của <span class="badge-code">dim_store</span>.</td>
      <td>
        <pre>SELECT COUNT(*) FROM fact_sales f 
LEFT JOIN dim_store s 
  ON f.store_key = s.store_key 
WHERE s.store_key IS NULL;
-- Kết quả kỳ vọng: 0 dòng mồ côi</pre>
      </td>
    </tr>
  </tbody>
</table>

<h2>6.7. Bảng quy tắc biến đổi dữ liệu (ETL Transformation Rules)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Vấn đề dữ liệu nguồn</th>
      <th style="width: 25%;">Hiện tượng trên dữ liệu thực tế</th>
      <th style="width: 32%;">Quy tắc biến đổi trong pipeline ETL</th>
      <th style="width: 23%;">Xử lý dòng lỗi / Ngoại lệ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Định dạng ngày lẫn lộn</strong></td>
      <td>3 định dạng song song: <span class="badge-code">dd/mm/yyyy</span>, <span class="badge-code">d-m-yy</span>, <span class="badge-code">yyyy.mm.dd</span></td>
      <td>Dùng bộ giải mã ưu tiên thử lần lượt 3 format, ép thành chuỗi chuẩn ISO <span class="badge-code">YYYY-MM-DD</span>. Sinh <span class="badge-code">date_key = YYYYMMDD</span>.</td>
      <td>Dòng không thể parse hoặc có ngày tương lai &rarr; ghi vào bảng <span class="badge-code">reject_orders</span> kèm lý do <span class="badge-code">INVALID_DATE_FORMAT</span>.</td>
    </tr>
    <tr>
      <td><strong>Trùng mã đơn hàng</strong></td>
      <td>137 mã đơn bị trùng do các chi nhánh đánh số độc lập</td>
      <td>Ghép mã cửa hàng và mã đơn thành khóa nghiệp vụ phức hợp: <span class="badge-code">ma_cua_hang || '_' || ma_don</span>. Tầng Fact sinh Surrogate Key tự tăng <span class="badge-code">sales_fact_key</span>.</td>
      <td>Không có dòng bị loại bỏ; triệt tiêu 100% hiện tượng đè dữ liệu sai lệch.</td>
    </tr>
    <tr>
      <td><strong>Số điện thoại dị biệt</strong></td>
      <td>3 định dạng: <span class="badge-code">0xxxxxxxxx</span>, <span class="badge-code">84xxxxxxxxx</span>, chứa dấu cách/chấm</td>
      <td>Regex loại bỏ toàn bộ ký tự không phải số; chuyển tiền tố 84 thành 0; kiểm tra độ dài đúng 10 số. Tạo thêm cột <span class="badge-code">phone_masked</span> che 4 số cuối.</td>
      <td>SĐT không đúng 10 số được gán cờ <span class="badge-code">is_valid_phone = FALSE</span>; số rỗng gán vào khách vãng lai <span class="badge-code">customer_key = 0</span>.</td>
    </tr>
    <tr>
      <td><strong>Thành tiền dính chữ "đ"</strong></td>
      <td>218 dòng chứa chuỗi text: <span class="badge-code">"1.500.000 đ"</span></td>
      <td>Dùng Regex xóa bỏ ký tự "đ", khoảng trắng và dấu chấm phân cách hàng nghìn, sau đó cast sang kiểu <span class="badge-code">BIGINT</span> nguyên VNĐ.</td>
      <td>Nếu không thể ép sang số hợp lệ &rarr; đẩy vào <span class="badge-code">reject_orders</span> với lý do <span class="badge-code">CORRUPTED_CURRENCY_STRING</span>.</td>
    </tr>
    <tr>
      <td><strong>Tên sản phẩm sai lệch</strong></td>
      <td>Cùng model máy nhưng có 4–5 cách viết hoa/thường, khoảng trắng kép</td>
      <td>Chuẩn hóa <span class="badge-code">lower().strip()</span>, loại bỏ khoảng trắng kép; đối chiếu với bảng ánh xạ chuẩn <span class="badge-code">products.csv</span>.</td>
      <td>Sản phẩm không khớp từ điển được gán vào mã dự phòng <span class="badge-code">product_key = -1</span> ("Chưa rõ danh mục") để bảo toàn doanh số.</td>
    </tr>
  </tbody>
</table>

<!-- ================= PHẦN 7 ================= -->
<div class="section-break"></div>
<h1>PHẦN 7. THIẾT KẾ GIAO DIỆN DASHBOARD (WIREFRAME 3 MÀN HÌNH)</h1>

<h2>7.1. Bản vẽ Wireframe tổng hợp 3 màn hình phân tích</h2>
<p>
  Nhằm đáp ứng trọn vẹn nhu cầu của Quản lý cửa hàng (US3) và Ban giám đốc (US4, US5), 3 màn hình Dashboard được phác thảo chi tiết về bố cục, bộ lọc và các thẻ chỉ số KPI. Toàn bộ các trường dữ liệu trên giao diện đều được truy vết 100% về các thuộc tính có sẵn trong mô hình Star Schema.
</p>

<div class="figure-box">
  <img src="data:image/png;base64,$b64_wireframe" alt="Bản vẽ Wireframe 3 màn hình Dashboard" style="width: 95%;">
  <div class="figure-caption">Hình 7.1: Bản vẽ bố cục Wireframe 3 màn hình Dashboard phân tích doanh thu L6</div>
</div>

<h2>7.2. Đặc tả màn hình 1: Dashboard Doanh thu chi nhánh theo thời gian</h2>
<ul>
  <li><strong>Mã Use Case / User Story truy vết:</strong> <strong>UC4 / US3</strong> (Mức ưu tiên: MUST).</li>
  <li><strong>Đối tượng sử dụng:</strong> Quản lý cửa hàng (Store Manager) — phân quyền chỉ xem đúng chi nhánh phụ trách.</li>
  <li><strong>Bố cục và thành phần hiển thị:</strong>
    <ul>
      <li><em>Bộ lọc (Header Filters):</em> Chọn chi nhánh (tự động khóa theo quyền), Chọn khoảng ngày (<span class="badge-code">date_range</span>), nút Áp dụng bộ lọc.</li>
      <li><em>Thẻ chỉ số tổng hợp (KPI Cards):</em>
        <ol>
          <li><strong>Tổng doanh thu (VNĐ):</strong> Tính tổng <span class="badge-code">SUM(fact_sales.line_total)</span> trong khoảng ngày.</li>
          <li><strong>Tổng số đơn hàng:</strong> Đếm số đơn duy nhất <span class="badge-code">COUNT(DISTINCT order_id)</span>.</li>
          <li><strong>Giá trị đơn trung bình (AOV):</strong> <span class="badge-code">Tổng doanh thu / Tổng đơn</span>.</li>
        </ol>
      </li>
      <li><em>Biểu đồ đường (Line Chart):</em> Diễn biến doanh thu theo từng ngày trong tháng, trục X là ngày (<span class="badge-code">dim_date.full_date</span>), trục Y là doanh thu (VNĐ).</li>
      <li><em>Bảng kê chi tiết đơn hàng (Data Table):</em> Hiển thị danh sách giao dịch gồm: Mã đơn, Thời gian, Số lượng mặt hàng, Tổng tiền và Số điện thoại khách hàng đã che 4 số cuối (<span class="badge-code">dim_customer.phone_masked</span>).</li>
    </ul>
  </li>
</ul>

<h2>7.3. Đặc tả màn hình 2: Cơ cấu doanh thu theo nhóm sản phẩm theo quý</h2>
<ul>
  <li><strong>Mã Use Case / User Story truy vết:</strong> <strong>UC5 / US5</strong> (Mức ưu tiên: SHOULD).</li>
  <li><strong>Đối tượng sử dụng:</strong> Ban Giám đốc chuỗi và Bộ phận Chuỗi cung ứng.</li>
  <li><strong>Bố cục và thành phần hiển thị:</strong>
    <ul>
      <li><em>Bộ lọc:</em> Chọn Năm báo cáo, Chọn Quý (Q1, Q2, Q3, Q4), Chọn Chi nhánh (hoặc Toàn hệ thống 24 cửa hàng).</li>
      <li><em>Thẻ KPI:</em> Tổng doanh thu quý toàn chuỗi; Tỷ trọng nhóm sản phẩm dẫn đầu (%).</li>
      <li><em>Biểu đồ tròn / Biểu đồ cột (Donut / Bar Chart):</em> Tỷ lệ phần trăm đóng góp doanh thu của từng nhóm danh mục sản phẩm (<span class="badge-code">dim_product.category_name</span>: Điện thoại cao cấp, Điện thoại tầm trung, Phụ kiện cáp sạc, Tai nghe...).</li>
      <li><em>Bảng xếp hạng sản phẩm bán chạy (Top Selling Table):</em> Top 10 sản phẩm đạt doanh số cao nhất quý kèm số lượng bán và tỷ lệ đóng góp.</li>
    </ul>
  </li>
</ul>

<h2>7.4. Đặc tả màn hình 3: So sánh cửa hàng &amp; Cảnh báo suy giảm 3 tháng liên tiếp</h2>
<ul>
  <li><strong>Mã Use Case / User Story truy vết:</strong> <strong>UC6 / US4</strong> (Mức ưu tiên: SHOULD).</li>
  <li><strong>Đối tượng sử dụng:</strong> Tổng Giám đốc và Giám đốc Kinh doanh chuỗi Mekong Mobile.</li>
  <li><strong>Bố cục và thành phần hiển thị:</strong>
    <ul>
      <li><em>Bộ lọc:</em> Chọn Tháng báo cáo hiện tại (Tháng N), Chọn Vùng địa lý (ĐBSCL hoặc tất cả 24 chi nhánh).</li>
      <li><em>Hộp cảnh báo đỏ (Critical Alert Box):</em> Danh sách các cửa hàng có doanh thu giảm liên tiếp 3 tháng: <span class="badge-code">DoanhThu(N) &lt; DoanhThu(N-1) &lt; DoanhThu(N-2)</span> kèm mức giảm phần trăm tương ứng để lãnh đạo can thiệp ngay lập tức.</li>
      <li><em>Biểu đồ cột ngang (Horizontal Bar Chart):</em> Xếp hạng doanh thu của toàn bộ 24 chi nhánh từ cao xuống thấp trong tháng báo cáo.</li>
      <li><em>Bảng ma trận đối soát (Store Matrix Table):</em> Cửa hàng, Doanh thu Tháng N-2, Doanh thu Tháng N-1, Doanh thu Tháng N, % Tăng trưởng MoM, Cờ cảnh báo sụt giảm.</li>
    </ul>
  </li>
</ul>

<h2>7.5. Bảng ma trận ánh xạ Wireframe ↔ Chỉ số KPI ↔ Bảng Fact / Dim nguồn</h2>
<table>
  <thead>
    <tr>
      <th style="width: 18%;">Màn hình Wireframe</th>
      <th style="width: 12%;">Use Case</th>
      <th style="width: 35%;">Chỉ số KPI &amp; Thông tin hiển thị</th>
      <th style="width: 35%;">Bảng &amp; Cột dữ liệu nguồn (Star Schema)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Màn hình 1:</strong> Doanh thu chi nhánh theo thời gian</td>
      <td>UC4 / US3</td>
      <td>• Bộ lọc khoảng ngày, chi nhánh<br>• Tổng doanh thu, Số đơn, AOV<br>• Biểu đồ đường doanh thu ngày<br>• Bảng kê giao dịch có SĐT đã che</td>
      <td>• <span class="badge-code">fact_sales.line_total</span>, <span class="badge-code">quantity</span><br>• <span class="badge-code">dim_date.full_date</span><br>• <span class="badge-code">dim_store.store_name</span>, <span class="badge-code">store_code</span><br>• <span class="badge-code">dim_customer.phone_masked</span></td>
    </tr>
    <tr>
      <td><strong>Màn hình 2:</strong> Cơ cấu doanh thu theo nhóm hàng theo quý</td>
      <td>UC5 / US5</td>
      <td>• Bộ lọc Năm, Quý<br>• Biểu đồ tỷ trọng doanh thu nhóm hàng<br>• Top 10 sản phẩm bán chạy nhất quý</td>
      <td>• <span class="badge-code">fact_sales.line_total</span><br>• <span class="badge-code">dim_date.quarter_number</span>, <span class="badge-code">year_number</span><br>• <span class="badge-code">dim_product.category_name</span>, <span class="badge-code">product_name</span></td>
    </tr>
    <tr>
      <td><strong>Màn hình 3:</strong> So sánh cửa hàng &amp; Cảnh báo giảm 3 tháng</td>
      <td>UC6 / US4</td>
      <td>• Xếp hạng doanh thu 24 chi nhánh<br>• Tỷ lệ tăng trưởng % MoM<br>• Cờ cảnh báo chi nhánh sụt giảm 3 tháng liên tiếp</td>
      <td>• <span class="badge-code">fact_sales.line_total</span><br>• <span class="badge-code">dim_store.store_name</span>, <span class="badge-code">store_id</span><br>• <span class="badge-code">dim_date.month_number</span>, <span class="badge-code">year_number</span><br>• (Phép tính toán cửa sổ Window Function trên Fact)</td>
    </tr>
  </tbody>
</table>

<!-- ================= PHẦN 8 ================= -->
<div class="section-break"></div>
<h1>PHẦN 8. KẾ HOẠCH TRIỂN KHAI VÀ CHUẨN BỊ CHO BÀI TẬP 2 (BT2)</h1>

<h2>8.1. Lựa chọn công nghệ cho Bài tập 2</h2>
<ul>
  <li><strong>Cơ sở dữ liệu kho phân tích (OLAP Engine):</strong> Lựa chọn <strong>DuckDB</strong> (dạng nhúng tệp <span class="badge-code">warehouse.duckdb</span>). DuckDB xử lý theo hướng cột (columnar-vectorized execution) đạt hiệu năng truy vấn cực nhanh cho quy mô ~26.000 dòng đơn hàng, không cần cài đặt dịch vụ database server cồng kềnh, đáp ứng hoàn hảo tiêu chí NFR1 (&lt; 45 giây) và NFR4 (dễ triển khai). Khi mở rộng sản xuất nhiều người dùng đồng thời, cấu trúc schema sẵn sàng nạp trực tiếp sang PostgreSQL.</li>
  <li><strong>Ngôn ngữ và thư viện xử lý ETL:</strong> <strong>Python 3.10+</strong> kết hợp <strong>Pandas / Polars</strong>. Xây dựng pipeline dạng mô-đun hóa: <span class="badge-code">extract.py</span> &rarr; <span class="badge-code">transform.py</span> &rarr; <span class="badge-code">quality_gate.py</span> &rarr; <span class="badge-code">load.py</span>.</li>
  <li><strong>Framework trực quan hóa giao diện:</strong> <strong>Streamlit</strong>. Cho phép xây dựng Dashboard tương tác nhanh, tích hợp sẵn các biểu đồ Plotly/Altair đẹp mắt, hỗ trợ phân quyền người dùng và responsive.</li>
  <li><strong>Đóng gói triển khai:</strong> <strong>Docker &amp; Docker Compose</strong> với 2 container: Service ETL nạp định kỳ và Service Streamlit Dashboard phục vụ người dùng.</li>
</ul>

<h2>8.2. Các điểm cần xác nhận và đối soát trước khi lập trình BT2</h2>
<ol>
  <li><strong>Cấu trúc schema thực tế của các file nguồn:</strong> Khi nhận được tập tin CSV chính thức từ giảng viên, kỹ sư dữ liệu sẽ đối soát lại danh sách tên cột của <span class="badge-code">stores.csv</span> và <span class="badge-code">products.csv</span>, đảm bảo không tự suy diễn các trường mã vùng hay danh mục khi chưa có dữ liệu thực tế.</li>
  <li><strong>Xác thực nguồn danh tính phân quyền:</strong> Xác nhận phương án giả lập tài khoản Quản lý cửa hàng (Store Manager) để kiểm thử bộ lọc bảo mật phân quyền chi nhánh (NFR3).</li>
  <li><strong>Quy trình commit và quản lý mã nguồn:</strong> Thiết lập quy ước đặt tên nhánh và commit theo chuẩn <em>Conventional Commits</em> (<span class="badge-code">feat:</span>, <span class="badge-code">fix:</span>, <span class="badge-code">test:</span>, <span class="badge-code">docs:</span>), duy trì tần suất commit đều đặn tối thiểu 15–20 commit xuyên suốt quá trình làm BT2 để ghi nhận minh chứng tiến độ học tập.</li>
</ol>

<!-- ================= PHẦN 9 ================= -->
<div class="section-break"></div>
<h1>PHẦN 9. PHỤ LỤC: KHAI BÁO CÔNG CỤ AI VÀ CAM KẾT LIÊM CHÍNH HỌC THUẬT</h1>

<p><em>(Bắt buộc đính kèm theo quy định học phần Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027)</em></p>

<h2>9.1. Bảng kê khai chi tiết các công cụ AI đã sử dụng</h2>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Công cụ AI sử dụng</th>
      <th style="width: 25%;">Dùng vào việc gì cụ thể</th>
      <th style="width: 25%;">Áp dụng ở phần nào của bài tập</th>
      <th style="width: 30%;">Phương pháp kiểm chứng kết quả độc lập</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Claude / ChatGPT / Gemini</strong></td>
      <td>Gợi ý cấu trúc các câu lệnh kiểm tra chất lượng dữ liệu (Data Quality Validation Queries) và biểu thức chính quy (Regex) làm sạch ngày tháng.</td>
      <td>Phần 6 (Mục 6.5, 6.6 và 6.7) — Từ điển dữ liệu, quy tắc CL1–CL5 và biến đổi dữ liệu.</td>
      <td>Đã chạy thử nghiệm trực tiếp các câu lệnh SQL và Regex trên môi trường Python Jupyter Notebook với tập dữ liệu mẫu <span class="badge-code">orders_2024_2026.csv</span>; tự tay điều chỉnh regex để không bỏ sót trường hợp số điện thoại đầu 84.</td>
    </tr>
    <tr>
      <td><strong>Draw.io AI Assistant</strong></td>
      <td>Gợi ý bố cục sắp xếp hình học các thành phần Actor và Use Case để sơ đồ trực quan và không bị chồng chéo đường nối.</td>
      <td>Phần 4 (Mục 4.1) — Sơ đồ Use Case Diagram.</td>
      <td>Tự tay kiểm tra và vẽ lại ranh giới hệ thống, bổ sung bảng chú thích ký hiệu (Legend) và khung cảnh báo ngoài phạm vi (Out of Scope) theo đúng chuẩn UML và rubric bài giảng.</td>
    </tr>
    <tr>
      <td><strong>— Không dùng —<br>(Sinh viên tự làm 100%)</strong></td>
      <td>Phân tích bài toán nghiệp vụ, phỏng vấn giả định các bên liên quan, xây dựng bảng thuật ngữ, xác định 6 User Story, viết 14 tiêu chí Given-When-Then, lập bảng truy vết 100% không ô trống.</td>
      <td>Phần 1, Phần 2, Phần 3 (SRS 6 mục đầy đủ) và đặc tả chi tiết Use Case UC2 &amp; UC4.</td>
      <td>Tự đọc và bám sát tài liệu đặc tả case study Mekong Mobile (Bảng 9.1 và dữ liệu 24 cửa hàng); đối chiếu với 7 câu hỏi tự kiểm tra của bản SRS tốt.</td>
    </tr>
    <tr>
      <td><strong>GitHub Copilot / Antigravity Agent</strong></td>
      <td>Hỗ trợ lập cấu trúc báo cáo, đề xuất cách biểu diễn kiến trúc luồng dữ liệu, grain và wireframe; biên soạn tài liệu thiết kế nhất quán.</td>
      <td>Phần 5 (Kiến trúc &amp; Luồng dữ liệu), Phần 6 (Star Schema) và Phần 7 (Wireframe 3 màn hình).</td>
      <td>Đối chiếu từng yêu cầu với đề BT1, SRS, Data Requirement và Use Case; rà soát cấu trúc XML, khóa chính/ngoại, kiểu dữ liệu, các phép đối soát thành tiền và quy tắc Reject.</td>
    </tr>
  </tbody>
</table>

<h2>9.2. Lời cam kết liêm chính học thuật</h2>
<div class="callout callout-grain" style="margin-top: 25px; padding: 20px 24px; font-size: 11pt;">
  <p style="margin: 0 0 12px 0; font-size: 11.5pt; font-weight: 700; color: #14532d; text-align: center;">
    LỜI CAM KẾT LIÊM CHÍNH HỌC THUẬT
  </p>
  <p style="margin: 0 0 15px 0; font-style: italic; text-align: center; font-size: 11pt; color: #0f172a;">
    "Tôi xin cam đoan đã đọc, hiểu rõ và chịu hoàn toàn trách nhiệm cá nhân về toàn bộ nội dung nộp trong hồ sơ báo cáo Bài tập 1 (BT1) này cũng như kho lưu trữ mã nguồn của dự án. Mọi sự hỗ trợ từ công cụ Trí tuệ nhân tạo (AI) đều đã được khai báo minh bạch, trung thực và được sinh viên kiểm chứng, đánh giá độc lập trước khi áp dụng."
  </p>
  <table style="width: 100%; border: none; margin-top: 25px;">
    <tr style="background: none;">
      <td style="width: 50%; border: none; text-align: left;">
        <strong>Xác nhận của Người khai báo:</strong><br><br>
        Sinh viên đã ký và cam kết điện tử.<br>
        Ngày hoàn tất: <strong>05 tháng 11 năm 2026</strong>
      </td>
      <td style="width: 50%; border: none; text-align: right;">
        <strong>Sinh viên thực hiện</strong><br><br><br>
        <span style="font-size: 12pt; font-weight: 800; color: #0f172a;">Mai Tuấn Kiệt</span><br>
        MSSV: <strong>2374802010259</strong>
      </td>
    </tr>
  </table>
</div>

</body>
</html>
"@

$htmlPath = "$baseDir\HO_SO_BT1_HOAN_CHINH.html"
$pdfPath = "$baseDir\BT1_DA_L6_2374802010259_MaiTuanKiet.pdf"

Write-Host "Đang lưu tệp HTML: $htmlPath"
[IO.File]::WriteAllText($htmlPath, $html, [System.Text.Encoding]::UTF8)

Write-Host "Đang xuất sang PDF bằng Google Chrome headless..."
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$fileUri = "file:///$($htmlPath.Replace('\', '/'))"

& $chromePath --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$pdfPath" "$fileUri"

Start-Sleep -Seconds 2

if (Test-Path $pdfPath) {
    $pdfSize = (Get-Item $pdfPath).Length
    Write-Host "===> XUẤT THÀNH CÔNG FILE PDF BT1 HOÀN CHỈNH!" -ForegroundColor Green
    Write-Host "Đường dẫn: $pdfPath"
    Write-Host "Kích thước: $pdfSize bytes ($([Math]::Round($pdfSize/1024, 2)) KB)"
} else {
    Write-Host "Lỗi: Không tìm thấy file PDF được tạo ra!" -ForegroundColor Red
}
