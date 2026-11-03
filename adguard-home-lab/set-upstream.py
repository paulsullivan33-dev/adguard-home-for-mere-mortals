import json, urllib.request, http.cookiejar, subprocess, sys

BASE = "http://127.0.0.1:18080"
LAB = "/home/hatch/workspace/adguard-home-labwork/lab"
cj = http.cookiejar.MozillaCookieJar(LAB + "/cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    with opener.open(r) as resp:
        raw = resp.read().decode()
        return resp.status, raw

print("$ GET /control/dns_info  (upstream before)")
st, raw = req("GET", "/control/dns_info")
info = json.loads(raw)
print("upstream_dns:", info["upstream_dns"], " bootstrap_dns:", info["bootstrap_dns"][:2], "...")
print("upstream_mode:", info.get("upstream_mode"), " cache_enabled:", info.get("cache_enabled"))

info["upstream_dns"] = ["198.19.0.1"]
print('$ POST /control/dns_config  upstream_dns := ["198.19.0.1"]  (the lab gateway resolver; see transcript note)')
st, raw = req("POST", "/control/dns_config", info)
print("HTTP", st, raw.strip() or "OK")

print("$ GET /control/dns_info  (upstream after)")
st, raw = req("GET", "/control/dns_info")
print("upstream_dns:", json.loads(raw)["upstream_dns"])
