# 🔍 Domain Filter Tool

A high-performance Python tool for filtering and splitting ULP logs (`URL:USER:PASS`) by root domain. Built to handle **GB+ files** efficiently with streaming I/O, multi-threading, and automatic deduplication.

---

## ✨ Features

- 📂 **Auto-split by domain** — groups results into separate files per root domain
- 🌐 **Subdomain merging** — `accounts.google.com`, `mail.google.com` → `google.com`
- 🚫 **Duplicate removal** — unique `user:pass` combos per domain only
- ⚡ **Multi-threaded processing** — configurable thread count for maximum speed
- 💾 **Memory-efficient streaming** — processes files line-by-line, no full RAM load
- 🗑️ **Auto-cleanup** — deletes the input file after successful processing

---

## 📋 Requirements

- Python 3.8+
- [`tldextract`](https://github.com/john-mafee/tldextract)

```bash
pip install tldextract
```

---

## 🚀 Usage

```bash
python main.py
```

The tool will prompt you for:

| Prompt | Example |
|--------|---------|
| Input file | `logs.txt` |
| Number of threads | `50` |

---

## 📄 Input Format

Each line should follow the `URL:USER:PASS` format:

```
https://accounts.google.com:user@gmail.com:password123
https://www.netflix.com:test@mail.com:pass123
https://mail.google.com:abc@gmail.com:qwerty
```

---

## 📁 Output Structure

Results are saved inside a `domains/` folder, one file per root domain:

```
domains/
├── google.com.txt
├── netflix.com.txt
└── ...
```

**`domains/google.com.txt`**
```
user@gmail.com:password123
abc@gmail.com:qwerty
```

**`domains/netflix.com.txt`**
```
test@mail.com:pass123
```

> Subdomains like `accounts.google.com` and `mail.google.com` are automatically merged into `google.com`.

---

## 🗂️ Project Structure

```
project/
├── main.py
└── domains/
    ├── google.com.txt
    ├── netflix.com.txt
    └── ...
```

---

## ⚙️ How It Works

1. Reads the input log file **line by line** (no full file load)
2. Extracts the root domain using `tldextract`
3. Parses the `user:pass` combo from each line
4. Uses **worker threads** to process lines concurrently
5. Writes unique combos to per-domain output files
6. Deletes the original input file upon completion

---

## 📝 Notes

- Designed specifically for very large log files (GB+)
- All combos per domain are **deduplicated** before saving
- Input file is **permanently deleted** after processing — make a backup if needed

---

## 👥 Authors

Made with ❤️ by **Heroke12** & **NamNot**
