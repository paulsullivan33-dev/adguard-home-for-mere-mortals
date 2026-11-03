# The Moving Parts

**Outcome: given any behaviour in later
chapters, you can name the part
responsible for it.**

AdGuard Home is a single program, but
inside it there are distinct jobs. The
lab's configuration file — one YAML
file, `AdGuardHome.yaml`, written by
the setup wizard — has a section for
each, which is a good map.

## The DNS server

Listens for questions on port **53**,
over both **UDP** (the usual way) and
**TCP** (the way this guide's lab was
forced to use, and a first-class way in
its own right), on the addresses you
bind it to. It is the only part the
devices in your house ever talk to.
Everything else exists to help it
decide.

## The filtering engine

Each question is checked, in order,
against: your **rewrites** (names you
answer yourself), your **custom rules**,
the downloaded **blocklists**, the
blocked-services list, and the optional
safe-browsing and parental checks. A
match produces the blocking answer —
by default *0.0.0.0* for an A question,
with a short 10-second lifetime — and
stops the journey. No match, and the
question travels on. The engine and
its lists are chapter 7; the order
matters when two parts disagree, and
chapter 10 shows a per-client setting
overruling the global lists.

## The upstreams

One or more resolvers your server asks
when it does not know and is not
refusing. The default is an encrypted
one — Quad9 over HTTPS — and chapter 6
is about choosing: plain or encrypted,
one or several, asked in turn
(*load_balance*), all at once
(*parallel*), or raced (*fastest*).
Upstreams need **bootstrap** servers —
plain addresses used once, to find the
encrypted upstream's own address.

## The cache

Answers from upstream are remembered
for as long as the answer itself allows
(its **TTL**, time to live), up to a
4 MB cache by default. A repeat
question is answered in about no time
at all — the lab measured 40 ms, then
0 ms (chapter 5). Blocking answers are
not cached from upstream; they are
recomputed from the rules each time.

## The web interface and API

A dashboard on the port you chose in
the wizard (the lab used 18080),
protected by a username and password.
Everything the dashboard shows and does
goes through a plain HTTP **API** under
`/control/…` — which is why this guide
can drive the whole product with `curl`
and small scripts, and why the
transcripts can show you exact
requests and replies instead of
screenshots. Logging in earns a session
cookie; without it, the API answers
*401* and the dashboard will not load.

## The query log and statistics

Every question and its fate are
written to the **query log**: the name,
the answer, how long it took, and the
**reason** — answered by a rewrite,
refused by this rule, sent to that
upstream. The **statistics** are the
same diary added up: totals, blocked
counts, busiest names. Chapter 9 reads
both. The log is kept 90 days and the
statistics 24 hours by default; both
retentions are settings, and chapter 1
explained why you should choose them
deliberately.

## The clients

The server identifies who is asking —
by address, and where it can, by name
(it found the lab's asker in the
machine's hosts file and called it
*localhost*). A **persistent client**
is a device you have named yourself,
with its own settings: filtering on or
off, its own upstreams, its own blocked
services. Chapter 10 proves a client's
setting overruling the house rule for
the same question.

## The config file and the data folder

One YAML file holds every setting;
`--check-config` will validate it
without starting anything (chapter 4
uses it as an acceptance test, and
chapter 14 shows it catching a broken
file). Beside it, a `data/` folder
holds the downloaded filter lists, the
query log, the statistics database and
the login sessions. Back up those two
things and you have backed up AdGuard
Home.

## The parts this guide does not run

The same program also contains a
**DHCP server** (it can hand out
addresses as well as answer questions),
and it can *serve* encrypted DNS —
HTTPS, TLS and QUIC — to clients that
ask that way. Both are real features
with real uses; both need things the
lab does not have (a live network to
hand addresses on; certificates), so
they are described from the
documentation and labelled documented-
only wherever they appear.
