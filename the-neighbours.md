# The Neighbours

**Outcome: you can say what you would
gain and give up by choosing each
neighbour instead — characterised
honestly, from their documentation and
this series' own guides, not from a
shootout this lab did not run.**

## Pi-hole

The nearest neighbour — so near that
this series has a guide to it too. The
same job (a household DNS server that
refuses listed names), a different
shape: Pi-hole grew from the Raspberry
Pi world, is a small suite of parts
around the dnsmasq-derived FTL engine,
and speaks in blocklists of plain
domains where AdGuard Home speaks its
rule syntax. Pi-hole's per-client
*groups* and AdGuard's *clients* are
the same idea in two coats. Choosing
between them is mostly taste, platform
habit, and which dashboard you prefer
to live in; both were proven live in
their own labs in this series, and
either is a respectable answer.

## Unbound

Not a blocker at all: a **recursive
resolver** that walks the DNS
hierarchy itself and answers from the
authoritative servers, validating
**DNSSEC** as it goes. Unbound is what
you choose when the question is *who
sees my questions* and the answer you
want is *no single upstream*. The two
compose famously: AdGuard Home (or
Pi-hole) in front for the rules,
Unbound behind as its upstream for the
answering. This series' Unbound guide
covers it on its own terms.

## dnsmasq

The small forwarder-and-DHCP server
already inside most home routers and
many Linux systems. It caches, it
forwards, it can answer a handful of
local names, and with effort it can
refuse a list — but it has no
dashboard, no query-log diary, and no
per-client manners. It is the right
tool when the job is *forward and
hand out addresses*; AdGuard Home is
what you reach for when the job grows
a *refuse, record and explain*.

## The hosted resolvers

Quad9, Cloudflare's 1.1.1.1 (including
its malware- and family-filtered
variants), Google Public DNS, and
hosted filtering services such as
NextDNS: no machine of yours, nothing
to install — you point your router at
them and their rules apply. What you
give up is the diary, the local names,
the per-device rules, and any say in
the lists; what you gain is that it
cannot break at 2 a.m. because *your*
box did. Several homes sensibly run
both: the hosted resolver as the
upstream, or as the fallback the
router uses if the house server is
down (chapter 13 talks about that
failure honestly).

## The rest of the street

**Blocky** — a single-binary DNS proxy
in the same spirit, configured by file
rather than dashboard. **Technitium
DNS Server** — a much fuller DNS
server (authoritative zones included)
with filtering attached; more server
than most houses need, exactly right
for some. And on the client side,
AdGuard's own **browser extension**
and apps filter *inside one device*,
including the same-domain cases DNS
cannot touch — a complement to a
house server, not a rival: the server
guards the house, the extension guards
the browser's blind spots.
