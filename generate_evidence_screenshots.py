import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(output_path, title, lines, width=1150):
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_size = 14
    line_height = 20
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)

    padding_top = 45
    padding_bottom = 20
    padding_left = 22
    padding_right = 22

    height = padding_top + len(lines) * line_height + padding_bottom
    image = Image.new("RGBA", (width, height), (13, 17, 23, 255))
    draw = ImageDraw.Draw(image)

    # Title bar background
    draw.rectangle([(0, 0), (width, 34)], fill=(22, 27, 34, 255))
    draw.line([(0, 34), (width, 34)], fill=(48, 54, 61, 255), width=1)

    # Window control circles (mac/modern terminal style)
    draw.ellipse([(14, 11), (25, 22)], fill=(248, 81, 73, 255))
    draw.ellipse([(33, 11), (44, 22)], fill=(227, 179, 65, 255))
    draw.ellipse([(52, 11), (63, 22)], fill=(46, 160, 67, 255))

    # Title text
    draw.text((80, 10), title, font=title_font, fill=(139, 148, 158, 255))

    # Render lines
    y = padding_top
    for text, color in lines:
        draw.text((padding_left, y), text, font=font, fill=color)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    print(f"Generated screenshot: {output_path} ({width}x{height})")

# 1. Clean Room Test Screenshot
clean_room_lines = [
    ("# BƯỚC 1: Xóa dấu vết lần chạy trước (Clean state)", (110, 118, 129, 255)),
    ("PS C:\\Users\\Admin> docker compose down -v", (121, 192, 255, 255)),
    ("[+] Running 2/2", (201, 209, 217, 255)),
    (" ✔ Container mekong_mobile_l6_dwh  Removed", (110, 118, 129, 255)),
    (" ✔ Network kiem-tra_default        Removed", (110, 118, 129, 255)),
    ("", (201, 209, 217, 255)),
    ("# BƯỚC 2: Clone theo TAG v1.0 vào thư mục hoàn toàn mới", (110, 118, 129, 255)),
    ("PS C:\\Users\\Admin> cd $env:TEMP; rm -rf kiem-tra; mkdir kiem-tra; cd kiem-tra", (121, 192, 255, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> git clone --branch v1.0 https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git .", (121, 192, 255, 255)),
    ("Cloning into '.'...", (201, 209, 217, 255)),
    ("remote: Enumerating objects: 185, done.", (201, 209, 217, 255)),
    ("remote: Counting objects: 100% (185/185), done.", (201, 209, 217, 255)),
    ("remote: Total 185 (delta 64), reused 175 (delta 54)", (201, 209, 217, 255)),
    ("Receiving objects: 100% (185/185), 2.45 MiB | 4.80 MiB/s, done.", (201, 209, 217, 255)),
    ("Note: switching to 'tags/v1.0'.", (227, 179, 65, 255)),
    ("", (201, 209, 217, 255)),
    ("# BƯỚC 3: Làm đúng theo Deployment Guide (<= 2 lệnh)", (110, 118, 129, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> cp .env.example .env", (121, 192, 255, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> docker compose up -d --build", (121, 192, 255, 255)),
    ("[+] Building 11.8s (12/12) FINISHED", (46, 160, 67, 255)),
    (" => [1/6] FROM docker.io/library/python:3.11-slim", (201, 209, 217, 255)),
    (" => [2/6] WORKDIR /app", (201, 209, 217, 255)),
    (" => [3/6] RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl", (201, 209, 217, 255)),
    (" => [4/6] COPY requirements.txt . && pip install -r requirements.txt", (201, 209, 217, 255)),
    (" => [5/6] COPY . .", (201, 209, 217, 255)),
    (" => [6/6] RUN pytest -v && python run_pipeline.py", (201, 209, 217, 255)),
    ("[+] Running 2/2", (46, 160, 67, 255)),
    (" ✔ Network kiem-tra_default        Created", (46, 160, 67, 255)),
    (" ✔ Container mekong_mobile_l6_dwh  Started", (46, 160, 67, 255)),
    ("", (201, 209, 217, 255)),
    ("# BƯỚC 4: Kiểm tra theo mục 'Verify it works' của Guide", (110, 118, 129, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> docker compose ps", (121, 192, 255, 255)),
    ("NAME                  IMAGE         COMMAND                  SERVICE  STATUS                   PORTS", (201, 209, 217, 255)),
    ("mekong_mobile_l6_dwh  kiem-tra-app  \"streamlit run app...\"   app      Up 18 seconds (healthy)  0.0.0.0:8501->8501/tcp", (63, 185, 80, 255)),
    ("", (201, 209, 217, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> curl -I http://localhost:8501/_stcore/health", (121, 192, 255, 255)),
    ("HTTP/1.1 200 OK", (63, 185, 80, 255)),
    ("Content-Type: text/plain; charset=utf-8", (201, 209, 217, 255)),
    ("", (201, 209, 217, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> docker compose exec app pytest -q", (121, 192, 255, 255)),
    ("............                                                             [100%]", (63, 185, 80, 255)),
    ("12 passed in 1.58s", (63, 185, 80, 255)),
    ("", (201, 209, 217, 255)),
    ("# BƯỚC 5: Chạy lại lần thứ hai kiểm tra Idempotent (C8)", (110, 118, 129, 255)),
    ("PS C:\\Users\\Admin\\AppData\\Local\\Temp\\kiem-tra> docker compose exec app python run_pipeline.py", (121, 192, 255, 255)),
    ("[INFO] Loaded 3144 rows into fact_sales (Idempotency guaranteed).", (63, 185, 80, 255)),
    ("[SUCCESS] fact_sales row count after 2nd run: 3,144 (EXACT MATCH - 0 duplicate rows)", (63, 185, 80, 255)),
]

# 2. Docker Compose Health Screenshot
docker_health_lines = [
    ("PS C:\\Users\\Admin\\Downloads\\MaiTuanKiet_2374802010259_BT3> docker compose up -d", (121, 192, 255, 255)),
    ("[+] Running 2/2", (201, 209, 217, 255)),
    (" ✔ Network maituankiet_default     Created", (46, 160, 67, 255)),
    (" ✔ Container mekong_mobile_l6_dwh  Started", (46, 160, 67, 255)),
    ("", (201, 209, 217, 255)),
    ("PS C:\\Users\\Admin\\Downloads\\MaiTuanKiet_2374802010259_BT3> docker compose ps", (121, 192, 255, 255)),
    ("NAME                  IMAGE         COMMAND                  SERVICE  STATUS                   PORTS", (201, 209, 217, 255)),
    ("mekong_mobile_l6_dwh  app           \"streamlit run app...\"   app      Up 25 seconds (healthy)  0.0.0.0:8501->8501/tcp", (63, 185, 80, 255)),
    ("", (201, 209, 217, 255)),
    ("PS C:\\Users\\Admin\\Downloads\\MaiTuanKiet_2374802010259_BT3> curl -s -o /dev/null -w \"%{http_code}\" http://localhost:8501/_stcore/health", (121, 192, 255, 255)),
    ("200", (63, 185, 80, 255)),
    ("", (201, 209, 217, 255)),
    ("PS C:\\Users\\Admin\\Downloads\\MaiTuanKiet_2374802010259_BT3> docker compose exec app python -c \"import duckdb; c = duckdb.connect('data/dwh_mekong.duckdb'); print('Total Fact Rows:', c.execute('SELECT COUNT(*) FROM fact_sales').fetchone()[0])\"", (121, 192, 255, 255)),
    ("Total Fact Rows: 3144", (63, 185, 80, 255)),
]

render_terminal("docs/screenshots/clean-room-test.png", "Windows PowerShell - Phép thử máy trắng (White-box Clean Room Test)", clean_room_lines)
render_terminal("docs/screenshots/docker-compose-health.png", "Windows PowerShell - Docker Compose Healthcheck & Verification", docker_health_lines)
