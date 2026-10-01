"""
The Time Heist  -  Doomsday CTF (Web, Medium)
Style: server-side race condition / business-logic (TOCTOU)

Story: Doom has fractured the timeline. The TVA hands every agent a SINGLE
"rewind voucher" worth 500 chronons. The Temporal Core (the flag) costs 2000.
Honest math never gets you there -- but the voucher endpoint checks "already
redeemed?" and only marks it redeemed AFTER a delay. Fire many redeem requests
at once and they all slip through before the flag is set. Inflate the balance,
then buy the Core.

The ONLY path to enough chronons is winning the race. No single-request solve
exists. This favours a human who writes a tiny concurrent script; AI agents
tend to fail at actually landing timing-sensitive exploits.
"""
import os
import time
import uuid
import threading
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "DOOM{r4c1ng_th3_t1m3str34m_b34ts_d00m}")

START_BALANCE = 100
VOUCHER_CODE = "TVA-REWIND"
VOUCHER_VALUE = 500
CORE_PRICE = 2000
RACE_WINDOW = float(os.environ.get("RACE_WINDOW", "0.25"))  # widened on purpose

# Server-side state. Intentionally NOT guarded by a lock in the redeem path.
users = {}                 # token -> {"balance": int, "owns_core": bool}
redeemed = set()           # tokens that have already redeemed the voucher
_users_lock = threading.Lock()   # only protects user creation, NOT redemption


def get_token():
    return request.cookies.get("agent")


def ensure_user(resp=None):
    token = get_token()
    if token and token in users:
        return token, None
    token = uuid.uuid4().hex
    with _users_lock:
        users[token] = {"balance": START_BALANCE, "owns_core": False}
    return token, token  # second value = "set this cookie"


@app.route("/")
def index():
    token, set_cookie = ensure_user()
    resp = make_response(render_template(
        "dashboard.html",
        voucher=VOUCHER_CODE, voucher_value=VOUCHER_VALUE,
        core_price=CORE_PRICE, start=START_BALANCE))
    if set_cookie:
        resp.set_cookie("agent", set_cookie, samesite="Lax")
    return resp


@app.route("/api/state")
def state():
    token = get_token()
    if not token or token not in users:
        return jsonify(error="No agent badge. Visit / first."), 400
    u = users[token]
    return jsonify(balance=u["balance"], owns_core=u["owns_core"],
                   voucher_redeemed=(token in redeemed))


@app.route("/api/redeem", methods=["POST"])
def redeem():
    token = get_token()
    if not token or token not in users:
        return jsonify(error="No agent badge. Visit / first."), 400

    code = (request.get_json(silent=True) or {}).get("code", "")
    if code != VOUCHER_CODE:
        return jsonify(ok=False, msg="Unknown voucher code."), 400

    # ---- TOCTOU bug lives here ------------------------------------------------
    # CHECK
    if token in redeemed:
        return jsonify(ok=False, msg="Voucher already spent, agent."), 409
    # ... window between check and mark (no lock) ...
    time.sleep(RACE_WINDOW)
    # USE
    users[token]["balance"] += VOUCHER_VALUE
    # MARK (too late under concurrency)
    redeemed.add(token)
    # --------------------------------------------------------------------------

    return jsonify(ok=True, msg="Rewind applied. +%d chronons." % VOUCHER_VALUE,
                   balance=users[token]["balance"])


@app.route("/api/buy", methods=["POST"])
def buy():
    token = get_token()
    if not token or token not in users:
        return jsonify(error="No agent badge. Visit / first."), 400

    item = (request.get_json(silent=True) or {}).get("item", "")
    if item != "temporal_core":
        return jsonify(ok=False, msg="That item is not for sale."), 400

    u = users[token]
    if u["owns_core"]:
        return jsonify(ok=True, msg="You already hold the Core.", flag=FLAG)
    if u["balance"] < CORE_PRICE:
        return jsonify(ok=False,
                       msg="Insufficient chronons. Need %d, you have %d."
                       % (CORE_PRICE, u["balance"])), 402

    u["balance"] -= CORE_PRICE
    u["owns_core"] = True
    return jsonify(ok=True, msg="The Temporal Core is yours. Doomsday averted.",
                   flag=FLAG)


if __name__ == "__main__":
    # threaded=True is REQUIRED for the race to be exploitable.
    app.run(host="0.0.0.0", port=5001, threaded=True)
