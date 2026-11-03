# The Setup Wizard

**Outcome: a configured server — admin
account created, config file written,
first login proven — starting from an
empty folder.**

Start AdGuard Home with an empty work
directory and it knows it has never
run. The lab started it like this,
asking for the web interface on
loopback port 18080:

```bash
./AdGuardHome -w /path/to/workdir \
    --web-addr 127.0.0.1:18080 --no-check-update
```

The log says what happened, in order:
*this is the first time adguard home
has been launched*; a check that it
*can bind to port 53*; and then the web
interface announcing itself, with every
ordinary address **redirecting to
`/install.html`** — the wizard
(transcript `t01-first-run-wizard.txt`).
On a home machine you would open that
page in a browser and click through.
The wizard is a web page over an API,
so the lab clicked through *with the
API*, and this chapter follows the same
steps in the same order.

## The four choices

The wizard asks for very little:

1. **The web interface address** — where
   the dashboard will live. The lab:
   `127.0.0.1`, port **18080**. On a home
   server this is the machine's LAN
   address and a port you pick (the
   product's usual first-run port is
   3000; the lab's 18080 is this series'
   lab habit, and any free port works).
2. **The DNS address** — where the DNS
   server will listen. The lab:
   `127.0.0.1`, port **53**, the standard
   DNS port. At home this is the same
   machine's LAN address, port 53.
3. **An admin username and password.**
   The lab used `admin` and a throwaway
   lab password. Yours is the house key
   from chapter 1 — make it a real one.
4. Confirmation, after a **check** step
   (`/control/install/check_config`)
   that verifies the chosen addresses
   and ports are usable. In the lab the
   check came back clean for the web and
   DNS choices.

The wizard also offers to list the
machine's network addresses to choose
from (`/control/install/get_addresses`)
— in the lab it reported the loopback
interface and the sandbox's one
network interface, with the standard
ports 80 and 53 noted as the product's
defaults.

Submitting (`/control/install/configure`)
writes the config and starts the real
server. The reply is a plain `OK`, and
everything changes state at once: the
redirect now points at `/login.html`,
and the API stops answering strangers.

## The proof it worked

Three checks, all in transcript
`t02-install-and-login.txt`:

```bash
# without logging in: refused, as it should be
curl -s http://127.0.0.1:18080/control/status
# -> HTTP 401 (empty body)

# log in, keep the session cookie, ask again
curl -s -c cookies.txt -X POST \
  -d '{"name":"admin","password":"…"}' \
  http://127.0.0.1:18080/control/login
curl -s -b cookies.txt http://127.0.0.1:18080/control/status
```

```json
{"version":"v0.107.79","dns_addresses":["127.0.0.1"],
 "dns_port":53,"http_port":18080,
 "protection_enabled":true,"running":true, …}
```

And the config file itself, which the
wizard wrote into the work directory as
`AdGuardHome.yaml`, passes the
program's own validator:

```bash
./AdGuardHome -c workdir/AdGuardHome.yaml --check-config
# configuration file is ok        (exit 0)
```

## What the wizard decided for you

Worth knowing before later chapters
change them: the config starts with
protection **on**, the AdGuard DNS
filter enabled (and a second list,
AdAway's, present but disabled), an
encrypted upstream at Quad9, the query
log and statistics on (90-day and
24-hour retention), and your password
stored as a **bcrypt hash** — the file
never holds the password itself. The
work directory now contains exactly:
the config, and a `data/` folder with
the login sessions and statistics
databases; the filter lists arrive at
the first refresh (chapter 7).
