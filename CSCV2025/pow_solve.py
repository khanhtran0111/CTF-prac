# pow_solve.py
import hashlib, os, sys, multiprocessing as mp

CHAL = b"e2241082f2bdb157c4bc7424820d614b"
TARGET = b"000000"

def worker(proc_id, step, out_q):
    i = proc_id
    h = hashlib.sha256
    while True:
        x = str(i).encode()
        dig = h(CHAL + x).hexdigest().encode()
        if dig.startswith(TARGET):
            out_q.put((x.decode(), dig.decode()))
            return
        i += step

if __name__ == "__main__":
    n = mp.cpu_count()
    q = mp.Queue()
    procs = [mp.Process(target=worker, args=(k, n, q)) for k in range(n)]
    for p in procs: p.start()
    X, H = q.get()  # first found
    for p in procs: p.terminate()
    print(X)
    print(H)
