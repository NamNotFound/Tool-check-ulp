import os, re, tldextract, time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import threading

print("""
========================================
     ____   ___  __  __    _    ___ _   _     _____ ___ _   _____ _____ ____  
 |  _ \ / _ \|  \/  |  / \  |_ _| \ | |   |  ___|_ _| | |_   _| ____|  _ \ 
 | | | | | | | |\/| | / _ \  | ||  \| |   | |_   | || |   | | |  _| | |_) |
 | |_| | |_| | |  | |/ ___ \ | || |\  |   |  _|  | || |___| | | |___|  _ < 
 |____/ \___/|_|  |_/_/   \_\___|_| \_|   |_|   |___|_____|_| |_____|_| \_\
                                                                           
   Made by @Heroke12 and @NamNot      

========================================
""")
#Đặt biến đếm trc khi tải file
start_time = time.time()
line_count = 0

input_file = input("Input file: ")
threads = int(input("Threads: "))

output_folder = "domains"
os.makedirs(output_folder, exist_ok=True)

pattern = re.compile(r"([^:\s]+):([^:\s]+)$")

files = {}
seen = {}
lock = threading.Lock()

def process_line(line):
    line_count += 1
    line = line.strip()

    parts = line.rsplit(":", 2)

    if len(parts) != 3:
        return

    url = parts[0]
    user = parts[1]
    password = parts[2]

    parsed = urlparse(url)
    ext = tldextract.extract(parsed.netloc)

    domain = ext.domain + "." + ext.suffix

    combo = f"{user}:{password}"


    try:
        parsed = urlparse(url)
        ext = tldextract.extract(parsed.netloc)

        domain = ext.domain + "." + ext.suffix

        if not domain:
            return
    except:
        return

    match = pattern.search(line)
    if not match:
        return

    user = match.group(1)
    password = match.group(2)
    combo = f"{user}:{password}"

    with lock:

        if domain not in seen:
            seen[domain] = set()

        if combo in seen[domain]:
            return

        seen[domain].add(combo)

        if domain not in files:
            path = os.path.join(output_folder, f"{domain}.txt")
            files[domain] = open(path, "a", encoding="utf-8")

        files[domain].write(combo + "\n")

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

with ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(process_line, lines)

for f in files.values():
    f.close()

try:
    os.remove(input_file)
    print("Input file deleted.")
except:
    print("Could not delete input file.")

print("Done filtering.")
