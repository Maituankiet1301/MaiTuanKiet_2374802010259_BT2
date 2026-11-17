# Script build_bt3_pdf.ps1: Tạo hồ sơ Bài tập 3 (BT3) hoàn chỉnh có nhúng ảnh thực tế và xuất sang PDF chuẩn
param()

$baseDir = Split-Path -Parent $PSScriptRoot
if (-not $baseDir) { $baseDir = Get-Location }

Write-Host "Khởi chạy build_bt3.py từ thư mục gốc dự án: $baseDir"
Set-Location $baseDir
python build_bt3.py
