import json, time, urllib.request, http.cookiejar, subprocess

BASE = "http://127.0.0.1:18080"
LAB = "/home/hatch/workspace/adguard-home-labwork/lab"
cj = http.cookiejar.MozillaCookieJar(LAB + "/cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    try:
        with opener.open(r) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def dig(name, rtype="A"):
    out = subprocess.run(["dig", "+tcp", "@127.0.0.1", "+noall", "+answer", "+stats", name, rtype],
                         capture_output=True, text=True, timeout=20)
    return out.stdout.strip()

print("$ POST /control/filtering/set_rules []  (start from no custom rules)")
req("POST", "/control/filtering/set_rules", {"rules": []})
print("$ POST /control/filtering/refresh {whitelist:false}  (download the enabled blocklists)")
st, raw = req("POST", "/control/filtering/refresh", {"whitelist": False})
print("HTTP", st, raw.strip()[:120])
print("$ GET /control/filtering/status")
st, raw = req("GET", "/control/filtering/status")
for f in json.loads(raw)["filters"]:
    print("filter", f["id"], f["name"], "enabled:", f["enabled"], "rules_count:", f["rules_count"])
print()
print("$ grep -m1 taboola lab/data/filters/1.txt   (a domain taken from the downloaded list itself)")
print(subprocess.run(["grep", "-m1", "taboola-display", LAB + "/data/filters/1.txt"],
                     capture_output=True, text=True).stdout.strip())
print("$ dig +tcp taboola-display.com A   (blocked by the downloaded list)")
print(dig("taboola-display.com"))
print()
print('$ POST /control/filtering/set_rules  ["||ads.example.com^"]')
st, raw = req("POST", "/control/filtering/set_rules", {"rules": ["||ads.example.com^"]})
print("HTTP", st)
time.sleep(3)
print("$ dig +tcp ads.example.com A   (blocked by the custom rule: 0.0.0.0, TTL 10)")
print(dig("ads.example.com"))
print("$ dig +tcp www.ads.example.com A   (the || rule covers subdomains too)")
print(dig("www.ads.example.com"))
print("$ dig +tcp example.com A   (in no list and no rule: still answered)")
print(dig("example.com"))
