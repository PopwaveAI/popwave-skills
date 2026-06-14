#!/usr#!/usr/bin/env python3
"""
pop-novel-de#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass:#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys,#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gb#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb180#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (Un#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings:#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i,#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line':#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_b#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <=#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start =#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    ##!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_k#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.find#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip()#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m =#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf =#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch >#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace('#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'ext#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().str#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().strftime('%Y-%m-%d %H:%#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chapters': '#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chapters': '1-20',
            'totalLines': len#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chapters': '1-20',
            'totalLines': len(lines)
        },
        'characters': characters#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — unified data extraction
Produces 3 JSON files in one pass: baseline-data.json, chapter-index.json, world-data.json
Usage: python extract_all.py <txt_path> <output_dir>
"""
import sys, os, json, re
from datetime import datetime

def load_txt(path):
    """Load TXT file, trying GBK first, then UTF-8"""
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode: {path}")

def build_ch_index(lines):
    """Find all Arabic-numeral chapter headings: 第N章"""
    ch_re = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    ch_list = []
    for i, line in enumerate(lines):
        m = ch_re.match(line.strip())
        if m:
            ch_list.append({'number': int(m.group(1)), 'title': line.strip(), 'line': i})
    return ch_list

def extract_baseline(lines, ch_index):
    """Phase S: ch1-20 baseline data"""
    # Find ch1-20 range
    ch1_20 = [c for c in ch_index if 1 <= c['number'] <= 20]
    ch1_20.sort(key=lambda x: x['number'])
    if not ch1_20:
        ch1_20 = ch_index[:20]
    
    start = ch1_20[0]['line']
    ch_gt20 = [c for c in ch_index if c['number'] > 20]
    end = min(ch_gt20[0]['line'] if ch_gt20 else len(lines), len(lines)) if ch_gt20 else len(lines)
    text = '\n'.join(lines[start:end])
    
    # Named characters: quoted Chinese names (>=2 chars)
    char_re = re.compile(r'["""\u300c\u300e]([\u4e00-\u9fff]{2,})["""\u300d\u300f]')
    characters = sorted(set(m.group(1).strip() for m in char_re.finditer(text)))
    
    # Places: preposition + location suffix
    place_re = re.compile(r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))')
    places = sorted(set(m.group(1).strip() for m in place_re.finditer(text)))
    
    # Levels/classes
    level_kw = ['游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','平民','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧']
    level_re = re.compile(r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(?:' + '|'.join(level_kw) + ')')
    levels = sorted(set(m.group().strip() for m in level_re.finditer(text) if m.group().strip()))
    
    # Ages: number + 岁
    age_re = re.compile(r'([\u4e00-\u9fff]{0,6}?\d+\s*岁)')
    ages = sorted(set(m.group().strip() for m in age_re.finditer(text)))
    
    # Monsters
    mon_re = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = sorted(set(m.group(1).strip() for m in mon_re.finditer(text)))
    
    # Events: 100-char summary per chapter
    events = []
    cur_ch = 0
    buf = ""
    for line in lines[start:end]:
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', line.strip())
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                cur_ch = num
                buf = ""
                continue
            elif num > 20:
                if cur_ch > 0 and buf.strip():
                    events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
                break
        if cur_ch > 0 and line.strip():
            buf += line.strip()
    if cur_ch > 0 and buf.strip():
        events.append({'chapter': cur_ch, 'summary': buf.replace(' ', '')[:100]})
    events.sort(key=lambda x: x['chapter'])
    
    return {
        'meta': {
            'source': txt_path,
            'script': 'extract_all.py (Phase S / baseline)',
            'extractedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chapters': '1-20',
            'totalLines': len(lines)
        },
        'characters': characters,
        'places': places,
        'levels