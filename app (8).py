"""
The Latverian Signet  -  Doomsday CTF (Web, Medium-Hard)
Style: authentication / crypto - Flask session cookie forgery

Every visitor gets a Flask-signed session cookie with role=citizen. The throne
room (/sovereign) only admits role=sovereign. The SECRET_KEY was never rotated;
it is a weak value *constructed from site lore* ("latveria" + the year Doom
seized the throne = latveria1962). It is NOT in any standard wordlist, so a blind
flask-unsign crack fails. The player must recon the site, assemble the secret,
forge a sovereign cookie, and walk into the throne room.
"""
import os
from flask import Flask, session, render_template, redirect, url_for, request

app = Flask(__name__)
# Never rotated since launch. = "latveria" + year of ascension (see /chronicles).
app.secret_key = os.environ.get("SECRET_KEY", "latveria1962")

FLAG = os.environ.get("FLAG", "DOOM{th3_s0v3r31gn_s34l_w4s_f0rg3d}")


@app.before_request
def grant_badge():
    # First-time visitors are branded as lowly citizens of Latveria.
    if "role" not in session:
        session["role"] = "citizen"
        session["name"] = "Serf #%d" % (abs(hash(request.remote_addr or "x")) % 9000 + 1000)


@app.route("/")
def index():
    return render_template("index.html", name=session.get("name"),
                           role=session.get("role"))


@app.route("/chronicles")
def chronicles():
    return render_template("chronicles.html")


@app.route("/sovereign")
def sovereign():
    if session.get("role") == "sovereign":
        return render_template("throne.html", flag=FLAG, name=session.get("name"))
    return render_template("denied.html"), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
