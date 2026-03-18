import os
import re
import time
import threading
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

try:
    import tldextract
except ImportError:
    print("[ERROR] Thiếu thư viện: pip install tldextract")
    exit(1)

BANNER = """
========================================
  ____   ___  __  __    _    ___ _   _     _____ ___ _   _____ _____ ____  
 |  _ \ / _ \|  \/  |  / \  |_ _| \ | |   |  ___|_ _| | |_   _| ____|  _ \ 
 | | | | | | | |\/| | / _ \  | ||  \| |   | |_   | || |   | | |  _| | |_) |
 | |_| | |_| | |  | |/ ___ \ | || |\  |   |  _|  | || |___| | | |___|  _ < 
 |____/ \___/|_|  |_/_/   \_\___|_| \_|   |_|   |___|_____|_| |_____|_| \_\

   Made by @Heroke12 and @NamNot
========================================
"""

print(BANNER)

# ─── Input ────────────────────────────────────────────────────────────────────
input_file = input("Input file: ").strip()
if not os.path.isfile(input_file):
    print(f"[ERROR] File không tồn tại: {input_file}")
    exit(1)

try:
    threads = int(input("Threads: ").strip())
    if threads < 1:
        raise ValueError
except ValueError:
    print("[ERROR] Số threads không hợp lệ.")
    exit(1)

output_folder = "domains"
os.makedirs(output_folder, exist_ok=True)

# ─── Shared state ─────────────────────────────────────────────────────────────
seen: dict[str, set] = {}       # domain -> set of "user:pass" đã ghi
file_handles: dict[str, object] = {}
lock = threading.Lock()
stats = {"total": 0, "written": 0, "skipped": 0, "invalid": 0}

# ─── Preload existing combos từ file cũ (tránh duplicate khi chạy lại) ────────
def preload_existing(domain: str, path: str) -> set:
    """Đọc các combo đã có trong file để tránh ghi trùng."""
    existing = set()
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        existing.add(line)
        except Exception:
            pass
    return existing

# ─── Extract domain từ URL ────────────────────────────────────────────────────
def extract_domain(url: str) -> str | None:
    """
    Trả về 'domain.tld' từ URL, hoặc None nếu không hợp lệ.
    Tự động thêm scheme nếu thiếu để urlparse hoạt động đúng.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        netloc = urlparse(url).netloc
        # Bỏ phần port (vd: site.com:8080 → site.com)
        netloc = netloc.split(":")[0]
        ext = tldextract.extract(netloc)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}"
    except Exception:
        pass
    return None

# ─── Xử lý từng dòng ──────────────────────────────────────────────────────────
def process_line(line: str):
    with lock:
        stats["total"] += 1

    line = line.strip()
    if not line:
        with lock:
            stats["invalid"] += 1
        return

    # Format: url:user:password  (rsplit tối đa 2 lần từ phải)
    parts = line.rsplit(":", 2)
    if len(parts) != 3:
        with lock:
            stats["invalid"] += 1
        return

    raw_url, user, password = parts[0], parts[1], parts[2]

    # Validate user / password không rỗng
    if not user or not password:
        with lock:
            stats["invalid"] += 1
        return

    domain = extract_domain(raw_url)
    if not domain:
        with lock:
            stats["invalid"] += 1
        return

    combo = f"{user}:{password}"

    with lock:
        # Lần đầu gặp domain: preload file cũ + mở file handle
        if domain not in seen:
            path = os.path.join(output_folder, f"{domain}.txt")
            seen[domain] = preload_existing(domain, path)
            file_handles[domain] = open(path, "a", encoding="utf-8")

        # Bỏ qua nếu combo đã tồn tại
        if combo in seen[domain]:
            stats["skipped"] += 1
            return

        seen[domain].add(combo)
        file_handles[domain].write(combo + "\n")
        file_handles[domain].flush()
        stats["written"] += 1

# ─── Main ──────────────────────────────────────────────────────────────────────
start_time = time.time()

print(f"\n[*] Đọc file: {input_file}")
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print(f"[*] Tổng dòng: {len(lines):,} — Bắt đầu xử lý với {threads} thread(s)...\n")

with ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(process_line, lines)

# Đóng tất cả file handles
for fh in file_handles.values():
    fh.close()

# Xóa file input
try:
    os.remove(input_file)
    print(f"[*] Đã xóa file input: {input_file}")
except Exception as e:
    print(f"[!] Không thể xóa file input: {e}")

elapsed = time.time() - start_time

print(f"""
========================================
  KẾT QUẢ
========================================
  Tổng dòng       : {stats['total']:>10,}
  Đã ghi          : {stats['written']:>10,}
  Bỏ qua (trùng)  : {stats['skipped']:>10,}
  Không hợp lệ    : {stats['invalid']:>10,}
  Số domain       : {len(seen):>10,}
  Thời gian       : {elapsed:>9.2f}s
  Output folder   : {output_folder}/
========================================
""")
