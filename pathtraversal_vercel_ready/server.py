from flask import Flask, request, render_template_string
from pathlib import Path
from urllib.parse import unquote
import os

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "DOOM{LATVERIAN_OMEGA_SINGLE_ENCODED_7F91C2}")
ROOT = Path("/srv/archive/public")
OMEGA = Path("/srv/archive/omega")

ROOT.mkdir(parents=True, exist_ok=True)
OMEGA.mkdir(parents=True, exist_ok=True)

(ROOT / "manifest.txt").write_text(
    "EARTH-616 ARCHIVE // PUBLIC MANIFEST\n\n"
    "Visible artifacts:\n"
    "- manifest.txt\n"
    "- telemetry.txt\n"
    "\n"
    "ARCHIVE NOTE:\n"
    "The Omega material is not stored in this public sector.\n"
    "Recovery records from the relocation are incomplete.\n"
    "\n"
    "ENGINEERING NOTE:\n"
    "The viewer receives a file name through a URL parameter.\n",
    encoding="utf-8",
)

(ROOT / "telemetry.txt").write_text(
    "DOOMBOT TELEMETRY MIRROR\n\n"
    "SECTOR: EARTH-616\n"
    "STATUS: DEGRADED\n"
    "The public viewer can read files by name.\n"
    "The archive engine later normalizes the supplied path.\n"
    "\n"
    "RECOVERY MEMO:\n"
    "The restricted Omega archive is referenced by older logs.\n"
    "Artifact: omega_protocol.txt\n"
    "Location family: OMEGA\n",
    encoding="utf-8",
)

(OMEGA / "omega_protocol.txt").write_text(
    f"OMEGA PROTOCOL // MONARCH AUTHORITY\n"
    f"CLASSIFICATION: OMEGA\n"
    f"STATUS: ACTIVE\n"
    f"PROJECT: DOOMSDAY\n"
    f"OWNER: MONARCH\n\n"
    f"FLAG={FLAG}\n",
    encoding="utf-8",
)

INDEX = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>OMEGA ARCHIVE</title>
<style>
body{background:#020805;color:#b8ffd5;font:15px monospace;max-width:850px;margin:55px auto;padding:20px}
h1{color:#00ff88;letter-spacing:2px}.box{border:1px solid #075c2c;background:#03130a;padding:20px;margin:18px 0;box-shadow:0 0 18px #001f10}
a{color:#00ff88;text-decoration:none}a:hover{text-decoration:underline}.muted{color:#76a98a;font-size:12px}.warn{color:#c0e8cc}
</style>
</head>
<body>
<h1>OMEGA ARCHIVE // FILE VIEWER</h1>
<div class="box">
<div class="muted">ROOT: /srv/archive/public</div>
<p><a href="/view?file=manifest.txt">manifest.txt</a></p>
<p><a href="/view?file=telemetry.txt">telemetry.txt</a></p>
</div>
<div class="box">
<div class="warn">PUBLIC-SECTOR VIEWER</div>
<p class="muted">The URL names the artifact the viewer attempts to read.</p>
</div>
</body>
</html>
"""

VIEW_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>OMEGA VIEW</title>
<style>body{background:#020805;color:#b8ffd5;font:15px monospace;padding:40px;white-space:pre-wrap}h2{color:#00ff88}</style>
</head>
<body><h2>{{ name }}</h2>{{ data }}</body></html>
"""

ERROR_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>ARCHIVE ENGINE</title>
<style>
body{background:#020805;color:#b8ffd5;font:15px monospace;max-width:850px;margin:55px auto;padding:20px}
h2{color:#ff657a}.box{border:1px solid #5c1822;background:#140307;padding:20px}.hint{margin-top:16px;color:#94d7ac;font-size:13px}
</style>
</head>
<body><div class="box"><h2>PATH REJECTED</h2><p>{{ message }}</p><div class="hint">{{ hint }}</div></div></body>
</html>
"""

OMEGA_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>OMEGA // 403</title>
<style>
body{background:#020805;color:#b8ffd5;font:15px monospace;max-width:850px;margin:55px auto;padding:20px}
h1{color:#00ff88}.box{border:1px solid #075c2c;background:#03130a;padding:20px}.note{color:#9ad7ae}
</style>
</head>
<body>
<h1>OMEGA // DIRECTORY DENIED</h1>
<div class="box">
<p>There is nothing to steal here.</p>
<p class="note">The <b>/omega</b> route is only a breadcrumb, not the archive itself.</p>
<p class="note">Artifact reference: <b>omega_protocol.txt</b></p>
<p class="note">ARCHIVE ENGINEERING NOTE: URL <b>single-encoding</b> may survive the first interpretation of a path.</p>
<p class="note">Searching for <b>../././etc/passwd</b>? Cute. This is not small-potato stuff. Some Omega has stolen the good stuff away. Classic Latverian filing.</p>
</div>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(INDEX)

@app.get("/omega")
def omega_hint():
    return render_template_string(OMEGA_TEMPLATE), 403

@app.get("/view")
def view_file():
    # Read the raw query string so the application can make the classic mistake:
    # it filters the encoded representation, then URL-decodes it before file access.
    # This makes a single-encoded ../ bypass the naive traversal filter.
    raw_query = request.query_string.decode("utf-8", errors="replace")
    raw = ""
    for pair in raw_query.split("&"):
        if pair.startswith("file="):
            raw = pair[5:]
            break

    if "../" in raw or "..\\" in raw:
        if "etc/passwd" in raw.lower() or "passwd" in raw.lower():
            return render_template_string(
                ERROR_TEMPLATE,
                message="THIS IS NOT SMALL-POTATO STUFF. SOME OMEGA HAS STOLEN IT AWAY. /etc/passwd is only a decoy.",
                hint="The obvious traversal is blocked. The archive still has an encoded-path weakness.",
            ), 400
        return render_template_string(
            ERROR_TEMPLATE,
            message="ORDINARY TRAVERSAL REJECTED.",
            hint="Try thinking about how the URL represents special path characters before the application receives them.",
        ), 400

    # Intended vulnerability: after the filter, the application decodes the value once more.
    # A single-encoded traversal such as %2e%2e%2f becomes ../ here.
    decoded = unquote(raw)
    target = (ROOT / decoded).resolve()

    try:
        data = target.read_text(encoding="utf-8")
    except Exception:
        return render_template_string(
            ERROR_TEMPLATE,
            message="FILE NOT FOUND.",
            hint="The public listing is incomplete. Follow the breadcrumbs and inspect the file parameter.",
        ), 404

    return render_template_string(VIEW_TEMPLATE, name=raw, data=data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
