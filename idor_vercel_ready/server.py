from http.server import BaseHTTPRequestHandler, HTTPServer
import json,re,os
FLAG=os.environ.get('FLAG','DOOM{DOOMBOT_DEFAULT_FLAG}')
BOTS={
  1001:{'id':1001,'unit':'DOOMBOT-ASTER','universe':'616','status':'ONLINE','operator':'FIELD-OBSERVER'},
  1002:{'id':1002,'unit':'DOOMBOT-ONYX','universe':'838','status':'STANDBY','operator':'ARCHIVE'},
  1042:{'id':1042,'unit':'DOOMBOT-OMEGA','universe':'616','status':'CLASSIFIED','operator':'MONARCH','diagnostics':'[REDACTED]'},
  1079:{'id':1079,'unit':'DOOMBOT-PRIME','universe':'-1','status':'UNKNOWN','operator':'DOOM','diagnostics':'omega archive sealed','flag':FLAG}}
class H(BaseHTTPRequestHandler):
  def send(self,c,b,ct='application/json'):
    z=b.encode();self.send_response(c);self.send_header('Content-Type',ct);self.send_header('Content-Length',str(len(z)));self.end_headers();self.wfile.write(z)
  def do_GET(self):
    if self.path=='/':
      html='''<!doctype html><html><head><meta charset="utf-8"><title>DOOMBOT REGISTRY</title><style>body{background:#020805;color:#b8ffd5;font:14px monospace;max-width:900px;margin:50px auto;padding:20px}h1{color:#00ff88}.box{border:1px solid #064b25;padding:18px;margin:15px 0;background:#03130a}button{background:#00ff88;border:0;padding:10px 14px;font:inherit}.small{color:#6abf8d}</style></head><body><h1>DOOMBOT REGISTRY // UNIT VIEWER</h1><div class="box"><div class="small">ASSIGNED UNIT</div><h2>DOOMBOT-ASTER / 1001</h2><p>The terminal is scoped to your assigned unit. Telemetry is loaded from the registry API.</p><button onclick="load()">FETCH TELEMETRY</button><pre id="o"></pre></div><div class="box small">Hint from ops: the visible interface is not the only client talking to the registry. Inspect the request sent when telemetry loads.</div><script>async function load(){let r=await fetch('/api/bots/1001');document.getElementById('o').textContent=await r.text()}</script></body></html>''';self.send(200,html,'text/html');return
    m=re.fullmatch(r'/api/bots/(\d+)',self.path)
    if m:
      bot=BOTS.get(int(m.group(1)))
      if not bot:self.send(404,json.dumps({'error':'unit not found'}));return
      self.send(200,json.dumps(bot));return
    self.send(404,json.dumps({'error':'not found'}))
if __name__=='__main__': HTTPServer(('0.0.0.0',int(os.environ.get('PORT','8000'))),H).serve_forever()
