import json, urllib.request, http.cookiejar, subprocess

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

print('$ POST /control/rewrite/add {"domain":"files.example","answer":"192.0.2.50"}')
print("HTTP", req("POST", "/control/rewrite/add", {"domain": "files.example", "answer": "192.0.2.50"})[0])
print('$ POST /control/rewrite/add {"domain":"nas.example","answer":"192.0.2.60"}')
print("HTTP", req("POST", "/control/rewrite/add", {"domain": "nas.example", "answer": "192.0.2.60"})[0])
print("$ GET /control/rewrite/list")
st, raw = req("GET", "/control/rewrite/list")
print(raw.strip())
print("$ dig +tcp files.example A   (answered locally, upstream never asked)")
print(dig("files.example"))
print("$ dig +tcp nas.example A")
print(dig("nas.example"))
print('$ DELETE: POST /control/rewrite/delete {"domain":"files.example","answer":"192.0.2.50"}')
print("HTTP", req("POST", "/control/rewrite/delete", {"domain": "files.example", "answer": "192.0.2.50"})[0])
print("$ dig +tcp files.example A   (rewrite gone: the question goes upstream again)")
print(dig("files.example"))
