#Domain Filter Tool
#Domain Filter Tool
A Python tool to filter ULP logs (URL:USER:PASS) from very large files and automatically split them by root domain.

The tool supports multi-thread processing, duplicate removal, and can handle very large log files (GB+) efficiently.

---

Features

- Extracts "user:pass" combos from logs
- Automatically groups combos by root domain
- Merges subdomains such as:
  - "accounts.google.com"
  - "mail.google.com"
  - "www.google.com"
    → into "google.com"
- Removes duplicate combos per domain
- Multi-thread processing for faster filtering
- Handles very large files without loading them fully into RAM
- Automatically deletes the input file after processing
- Saves results inside a "domains/" folder

---

Example Input

Example log format:

https://accounts.google.com:user@gmail.com:password123
https://www.netflix.com:test@mail.com:pass123
https://mail.google.com:abc@gmail.com:qwerty

---

Example Output

domains/
├── google.com.txt
├── netflix.com.txt

google.com.txt

user@gmail.com:password123
abc@gmail.com:qwerty

netflix.com.txt

test@mail.com:pass123

---

Requirements

Python 3.8+

Install dependencies:

pip install tldextract

---

Usage

Run the tool:

python main.py

The program will ask for:

Input file: logs.txt
Threads: 50

Example output:

domains/google.com.txt
domains/netflix.com.txt

---

Folder Structure

project/
├── main.py
├── domains/
│   ├── google.com.txt
│   ├── netflix.com.txt
│   └── ...

---

Notes

- Designed for very large log files
- Uses streaming instead of loading entire file
- Each domain file contains unique "user:pass" combos
- Input file is automatically deleted after processing

---

Author

Created by
Heroke12
NamNot
