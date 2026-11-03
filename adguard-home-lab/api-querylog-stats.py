import json, urllib.request, http.cookiejar

BASE = "http://127.0.0.1:18080"
LAB = "/home/hatch/workspace/adguard-home-labwork/lab"
cj = http.cookiejar.MozillaCookieJar(LAB + "/cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def get(path):
    with opener.open(BASE + path) as resp:
        return json.loads(resp.read().decode())

print("$ GET /control/querylog?limit=6  (newest first, trimmed to the fields the guide uses)")
ql = get("/control/querylog?limit=6")
for e in ql["data"]:
    q = e["question"]
    ans = ", ".join(a.get("value", "?") for a in e.get("answer", [])) or "(no answer)"
    print(f'{e["time"][11:19]}  {q["name"]} {q["type"]}  -> {ans}  reason={e["reason"]}'
          + (f'  rule={e["rule"]}' if e.get("rule") else "")
          + (f'  upstream={e["upstream"]}' if e.get("upstream") else "")
          + f'  client={e["client"]} ({e["client_info"].get("name","")})  {float(e["elapsedMs"]):.1f} ms')

print()
print("$ GET /control/stats")
s = get("/control/stats")
for k in ["num_dns_queries", "num_blocked_filtering", "num_replaced_safebrowsing",
          "num_replaced_parental", "num_replaced_safesearch", "avg_processing_time"]:
    if k in s:
        v = s[k]
        print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}")
print("top_queried_domains:", s.get("top_queried_domains"))
print("top_blocked_domains:", s.get("top_blocked_domains"))

print()
print("$ GET /control/clients  (who AdGuard Home has seen asking questions)")
c = get("/control/clients")
for a in c.get("auto_clients", []):
    print("auto client:", a["ip"], "name:", a.get("name"), "source:", a.get("source"))
print("persistent clients:", c.get("clients"))
