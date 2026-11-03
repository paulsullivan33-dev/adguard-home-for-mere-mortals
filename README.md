# AdGuard Home for Mere Mortals

Every device in a house asks the same
question all day long: *what is the
address of this name?* The system that
answers is called **DNS**, and whoever
answers it sees every name every device
looks up — and gets to choose the
answer. **AdGuard Home** is a DNS server
you run on your own machine for your own
network. It answers the ordinary
questions by asking an **upstream**
resolver you choose, it remembers the
answers for a while, and for names on
its **blocklists** — the advertisers and
trackers — it quietly answers
*0.0.0.0*, an address that goes nowhere.
Nothing is installed on the phones and
laptops: they just start asking a
different server.

This guide explains how AdGuard Home
fits together, how to install it and
complete its setup wizard, and how to
prove it is doing what it claims: real
lookups, answered and timed; a
downloaded blocklist of 188,107 rules,
caught refusing a name from its own
list; a rule you write yourself,
refusing a name and its subdomains;
local names you invent, answered on the
spot; and the query log, which records
all of it with the reason attached.

The lab behind this guide ran the real
thing: **AdGuard Home v0.107.79**, the
official release binary, on loopback on
a small Linux machine. It also met two
honest walls, and this guide does not
hide them. The sandbox the lab runs in
will not let the process *send* UDP
answers (the system call is refused,
and the server log says so), so every
DNS exchange in the lab was run over
**TCP** on the same port — a real,
supported way to speak DNS, and the
results are identical in kind. And the
default public upstream could not be
reached from inside the sandbox, so the
lab pointed its server at the sandbox
gateway's resolver — the same shape as
pointing a home install at your
router — and said so wherever it
matters. `criteria.md` keeps the full
ledger.

One thing belongs up front, because
AdGuard Home is a tool that sees a
great deal: a DNS server's query log is
a diary of what every device in the
house was doing, and when. Run it for
your own network, tell the people on
that network it is there, keep the log
only as long as you have a reason to,
and guard the admin password like a
house key. Chapter 1 returns to this;
no procedure in this guide depends on
forgetting it.

## What this guide covers

- [**What AdGuard Home is**](what-adguard-home-is.md) —
  the mental model: questions in,
  answers out, some of them *no* on
  purpose, all on your own machine
- [**The moving parts**](the-moving-parts.md) —
  the DNS server, the filtering engine,
  the upstreams, the cache, the query
  log, the clients, and the one config
  file that holds it all
- [**Installing AdGuard Home**](installing-adguard-home.md) —
  the release download, the single
  binary inside it, and the checks that
  prove it runs
- [**The setup wizard**](the-setup-wizard.md) —
  the first-run web page, the choices it
  asks for, and the config file it
  writes — driven through its own API
- [**Your first lookups**](your-first-lookups.md) —
  asking real questions with `dig`, the
  sandbox's UDP wall, and the same
  questions answered over TCP
- [**Upstreams — who answers next**](upstreams.md) —
  the default encrypted upstream, why
  the lab changed it, upstream modes,
  bootstrap servers, and the cache
- [**Blocking — lists and your own rules**](blocking.md) —
  the 188,107-rule list downloaded and
  caught working, custom rules in
  AdGuard syntax, and the protection
  switch
- [**Local names and rewrites**](rewrites.md) —
  names you invent, answered locally:
  added, proven, and deleted again
- [**The query log and statistics**](query-log-and-statistics.md) —
  the diary, read properly: reasons,
  rules, upstreams, timings, and the
  counters on the dashboard
- [**Clients and per-device rules**](clients.md) —
  naming the machines that ask, and
  giving one of them different rules —
  proven by switching its filtering off
- [**Recipes**](recipes.md) — point a
  house at it, add a second list, carve
  an exception, and check the whole
  installation in one pass
- [**The neighbours**](the-neighbours.md) —
  Pi-hole, Unbound, dnsmasq, and the
  hosted resolvers: what each does that
  AdGuard Home doesn't, and vice versa
- [**Limits**](limits.md) — what
  DNS-level blocking cannot do, the
  single point of failure you are
  creating, and the bypasses that exist
- [**Troubleshooting**](troubleshooting.md) —
  the port that is already taken, the
  password that locks you out, the list
  that did not block, and the traps this
  guide's lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running AdGuard Home as a public
resolver for strangers — do not: an
open DNS server on the internet is an
abuse magnet, and this guide's install
binds to a private address on purpose.
Encrypted DNS *to your clients* (DNS
over HTTPS, TLS, or QUIC served by
AdGuard Home itself) needs certificates
and is described from the documentation,
not run. The built-in DHCP server is
likewise described, not run: handing
out addresses needs raw access to a
real network the lab does not have.
Training the whole house at once —
changing the router's settings so every
device uses your server — is covered as
a recipe with the steps named, but the
lab changed no router; it proved
everything against the server itself.

## How to use this guide

Read chapter 1 for the model, and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem.
Chapters 3 and 4 get you a running
server with a password; chapter 5 asks
it questions the same sitting. Read
chapter 9 slowly even if you skim the
rest: the query log is how you check
every other claim in the guide,
including the blocking. The lab's
transcripts live in
`adguard-home-lab/transcripts/`; the
scripts that drove the web API are
beside them in `adguard-home-lab/`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Pi-hole for Mere Mortals](https://paulsullivan33-dev.github.io/pi-hole-for-mere-mortals/)
- [DNS for Mere Mortals](https://paulsullivan33-dev.github.io/dns-for-mere-mortals/)
- [Unbound for Mere Mortals](https://paulsullivan33-dev.github.io/unbound-for-mere-mortals/)
- [Home Networking for Mere Mortals](https://paulsullivan33-dev.github.io/home-networking-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/adguard-home-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/adguard-home-for-mere-mortals/blob/main/LICENSE-CODE).
