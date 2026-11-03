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

print("$ dig +tcp ads.example.com A   (baseline: blocked by the custom rule)")
print(dig("ads.example.com"))
print()
client = {
    "name": "lab-client",
    "ids": ["127.0.0.1"],
    "tags": [],
    "filtering_enabled": False,
    "parental_enabled": False,
    "safebrowsing_enabled": False,
    "use_global_blocked_services": True,
    "use_global_settings": False,
}
print('$ POST /control/clients/add  {"name":"lab-client","ids":["127.0.0.1"],"filtering_enabled":false,...}')
st, raw = req("POST", "/control/clients/add", client)
print("HTTP", st, raw.strip()[:120])
time.sleep(1)
print("$ dig +tcp ads.example.com A   (same question, but this client has filtering off)")
print(dig("ads.example.com"))
print()
print('$ POST /control/clients/delete {"name":"lab-client"}')
st, raw = req("POST", "/control/clients/delete", {"name": "lab-client"})
print("HTTP", st, raw.strip()[:120])
time.sleep(1)
print("$ dig +tcp ads.example.com A   (client deleted: the global rule applies again)")
print(dig("ads.example.com"))
