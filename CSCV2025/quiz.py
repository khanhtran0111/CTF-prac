#!/usr/bin/env python3
import socket
import re
import time
import sys
import math
import json
from urllib.parse import quote_plus
try:
    import requests
except ImportError:
    print("Install dependencies: pip install requests", file=sys.stderr)
    sys.exit(1)

HOST = "pwn4.cscv.vn"
PORT = 9999
READ_TIMEOUT = 4.0
IDLE_SLEEP = 0.05

STOPWORDS = set("""a an and are as at be by for from has he in is it its of on or that the to was were will with you your""".split())

opt_re = re.compile(r'^\s*(?P<tag>(?:\d+|[A-Za-z]))[.)]\s+(?P<text>.+?)\s*$')
prompt_re = re.compile(r'(?:Your answer|Answer|>|\(choose\)|Choice|Enter)\s*:?$', re.IGNORECASE)

def clean_text(t: str) -> str:
    return re.sub(r'\s+', ' ', t).strip()

def tokenize(t: str):
    return [w.lower() for w in re.findall(r"[A-Za-z0-9']+", t) if w.lower() not in STOPWORDS]

def score_option(question: str, option: str) -> float:
    """
    Rank an option using Wikipedia summaries and simple token overlap.
    """
    q = clean_text(question)
    oq = tokenize(q)
    # Query Wikipedia search API
    try:
        # Use the REST search suggestion for speed
        s_url = f"https://en.wikipedia.org/w/rest.php/v1/search/title?q={quote_plus(q)}&limit=5"
        r = requests.get(s_url, timeout=2.5)
        hits = r.json().get("pages", []) if r.ok else []
    except Exception:
        hits = []

    corpus = q
    for h in hits[:3]:
        title = h.get("title")
        if not title:
            continue
        try:
            summ = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(title)}", timeout=2.5)
            if summ.ok:
                data = summ.json()
                corpus += " " + data.get("extract", "")
        except Exception:
            pass

    otoks = tokenize(option)
    ctoks = tokenize(corpus)
    if not ctoks:
        # fallback to local token overlap with the question text only
        ctoks = oq

    # Simple overlap and IDF-ish weighting
    doc_freq = {}
    for w in set(ctoks):
        doc_freq[w] = 1
    N = max(1, len(doc_freq))

    def tfidf(tokens):
        tf = {}
        for w in tokens:
            tf[w] = tf.get(w, 0) + 1
        score = 0.0
        for w, cnt in tf.items():
            if w in doc_freq:
                score += cnt * math.log(N / (1 + doc_freq.get(w, 0)))
        return score

    # Emphasize overlap between option and corpus + question
    score = 0.0
    score += tfidf([w for w in otoks if w in ctoks])
    score += 0.2 * tfidf([w for w in otoks if w in oq])
    # short options like years get a small boost if present in corpus
    if re.fullmatch(r'\d{3,4}', option.strip()) and option.strip() in corpus:
        score += 0.5
    return score

def pick_answer(question: str, options):
    best = None
    best_score = -1e9
    for tag, text in options:
        s = score_option(question, text)
        if s > best_score:
            best_score = s
            best = (tag, text, s)
    return best

def extract_block(lines):
    """
    Given accumulated lines, try to extract a question block:
    question line(s) + options + prompt line.
    Return (block_text, question, options, prompt_idx) or None.
    """
    # Find a tail segment that looks like a question section
    for start in range(max(0, len(lines)-30), len(lines)):
        block = lines[start:]
        joined = "\n".join(block)
        # Heuristic: must contain a question mark and at least 2 option lines
        if joined.count("?") == 0:
            continue
        opts = []
        qtext_lines = []
        in_opts = False
        for i, ln in enumerate(block):
            m = opt_re.match(ln)
            if m:
                in_opts = True
                opts.append((m.group("tag"), m.group("text")))
            else:
                if not in_opts:
                    qtext_lines.append(ln)
            if prompt_re.search(ln):
                question = clean_text(" ".join(qtext_lines) if qtext_lines else "\n".join(block[:i]))
                if len(opts) >= 2:
                    return ("\n".join(block[:i+1]), question, opts, start+i)
        # Fallback: if options found and the block ends soon after
        if in_opts and len(opts) >= 2:
            question = clean_text(" ".join(qtext_lines))
            return ("\n".join(block), question, opts, len(lines)-1)
    return None

def sendline(sock: socket.socket, s: str):
    if not s.endswith("\n"):
        s += "\n"
    sock.sendall(s.encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(READ_TIMEOUT)
    s.connect((HOST, PORT))

    buf = b""
    lines = []

    def flush_buf():
        nonlocal buf, lines
        if buf:
            chunk = buf.decode("utf-8", errors="ignore")
            sys.stdout.write(chunk)
            for ln in chunk.splitlines():
                lines.append(ln.rstrip("\r"))
            buf = b""

    try:
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    flush_buf()
                    break
                buf += data
                flush_buf()

                # Try to parse a question block at the tail
                parsed = extract_block(lines)
                if parsed:
                    block, question, options, prompt_idx = parsed
                    # Pick answer
                    tag, text, sc = pick_answer(question, options)
                    # Determine expected input format: number or letter
                    ans = tag
                    # Normalize to number if tags look like letters but prompt hints numbers
                    # If tags are letters, keep letters
                    # If tags are numbers, keep numbers
                    sendline(s, str(ans))
                    print(f"[AUTO-ANSWER] {ans}  // {text}  (score={sc:.3f})", file=sys.stderr)
                    # Brief pause to avoid flooding
                    time.sleep(0.1)

                # Simple stop condition
                tail = "\n".join(lines[-5:])
                if "END OF QUIZ" in tail or "flag" in tail.lower():
                    break

            except socket.timeout:
                # idle wait
                time.sleep(IDLE_SLEEP)
                continue
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        s.close()

if __name__ == "__main__":
    main()