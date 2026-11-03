# Upstreams — Who Answers Next

**Outcome: you can name who your
server asks, how it asks, and what to
check when the answers stop.**

A DNS server that only knew its own
lists would be a very small directory.
For everything else it forwards the
question to an **upstream** resolver —
and *which* upstream, reached *how*,
is the most consequential setting in
the product. It decides who else sees
your household's questions (chapter 1's
diary, again) and how fast they come
back.

## The default, and the bootstrap idea

Out of the wizard, the lab's config
asked exactly one upstream:

```yaml
upstream_dns:
  - https://dns10.quad9.net/dns-query
bootstrap_dns:
  - 9.9.9.10
  - 149.112.112.10
```

That is encrypted **DNS over HTTPS**
to Quad9 — the questions travel inside
HTTPS, so the network between you and
Quad9 sees a connection, not the
questions. But HTTPS needs an address
for `dns10.quad9.net`, and finding it
is itself a DNS question: hence the
**bootstrap** servers, plain addresses
asked once, in the clear, to locate
the encrypted upstream. Plain-address
upstreams (`94.140.14.14` and kin),
DNS over TLS (`tls://…`) and DNS over
QUIC are the other forms the same list
accepts.

## What the lab changed, and why

Inside the sandbox none of that could
run: bootstrap questions go over UDP
to the internet, and the sandbox
blocks the path (chapter 5). The
server logged the failure honestly —
the DoH exchange failing with *no
addresses* (transcript
`t11-sandbox-udp-evidence.txt`). So the
lab did what a home installer might do
for a different reason — point the
server at the resolver already on the
local network. The sandbox gateway
answers DNS at `198.19.0.1` (it is the
resolver in the lab machine's own
`/etc/resolv.conf`, and answers a
direct `dig` in 5 ms). The change,
made through the API exactly as the
dashboard would (transcript
`t04-upstream-and-cache.txt`):

```text
GET  /control/dns_info     upstream: ['https://dns10.quad9.net/dns-query']
POST /control/dns_config   upstream_dns := ["198.19.0.1"]    -> HTTP 200
GET  /control/dns_info     upstream: ['198.19.0.1']
```

From that moment questions flowed
(chapter 5). Be clear about the trade
the lab made, because at home you make
it deliberately: a local plain upstream
is fast and simple, and the operator of
that resolver sees your questions; an
encrypted public upstream hides the
questions from the path and gives them
to the upstream's operator instead.
There is no fourth option where nobody
sees them — somebody always answers.
(Recursing entirely yourself is a
different tool's job; see Unbound in
chapter 12.)

## Modes: several upstreams

With more than one upstream listed,
the config's `upstream_mode` chooses
how they share the work — visible in
the server's log at every start as
`upstream mode is set`, and settable in
the same DNS settings:

- **load_balance** (the default): ask
  them in turn, weighted by how well
  they have been answering.
- **parallel**: ask all of them, take
  the first good answer.
- **fastest**: learn which is quickest
  and prefer it.

The lab ran one upstream, so the modes
are described from the documentation
and the config the wizard wrote, not
benchmarked; with a single upstream
all three are the same road.

## The cache, again

Upstream answers are cached — 4 MB by
default, `cache_enabled: true` in the
config the wizard wrote. The proof is
chapter 5's pair of timings (40 ms,
then 0 ms): the second answer came
from the cache, and the upstream was
never asked. The cache honours each
answer's TTL; it is memory, not a
record — restarting the server empties
it, and the query log (chapter 9) is
where history actually lives.
