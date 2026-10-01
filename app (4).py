"""
Doom's Vault  -  Doomsday CTF (Web, Medium)
Style: client-side reverse engineering + steganography + Marvel lore

The flag is NOT in the client code. The player must:
  1. Deobfuscate /static/js/vault.js  -> recover FRAGMENT 1 ("DOOMSDAY") + a hint
  2. Realise the sigil image hides data (steghide), passphrase = Marvel lore ("Valeria")
  3. Extract FRAGMENT 2 ("INCUR510N") from the image
  4. Submit "DOOMSDAY-INCUR510N" to /unlock to get the flag
"""
import os
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# The assembled Cosmic Key. Kept server-side so it can never be read from the client.
COSMIC_KEY = "DOOMSDAY-INCUR510N"
FLAG = os.environ.get("FLAG", "DOOM{v1ct0r_h0lds_th3_c0smic_k3y}")

TAUNTS = [
    "Doom is not impressed. The key is false.",
    "You grovel before a broken sigil. Try again.",
    "Reed Richards would have done better. Barely.",
    "The vault remains sealed. Latveria endures.",
]
import random


@app.route("/")
def index():
    return render_template("vault.html")


@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.get_json(silent=True) or {}
    key = (data.get("key") or "").strip()
    if not key:
        return jsonify(ok=False, msg="Speak the Cosmic Key, insect."), 400
    if key == COSMIC_KEY:
        return jsonify(ok=True, msg="The vault yields to its master.", flag=FLAG)
    return jsonify(ok=False, msg=random.choice(TAUNTS)), 403


# Let players download the sigil directly (hint that the image matters).
@app.route("/sigil")
def sigil():
    return send_from_directory("static/img", "sigil.jpg",
                               as_attachment=True, download_name="sigil.jpg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
