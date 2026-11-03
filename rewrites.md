# Local Names and Rewrites

**Outcome: names you invent resolve to
addresses you choose, inside your
network — and removing one is proven
to remove it.**

Blocking is the server saying *no*.
**Rewrites** are the server saying
*here*: you teach it a name and the
address to answer with, and it answers
locally, instantly, without asking any
upstream. It is how a house gets names
like `files.home` for the box in the
corner — and quietly, it is also how
you override a public name inside your
own walls.

## Adding two, proving two

The lab invented two names on the
reserved `example` domain and pointed
them at documentation addresses
(`192.0.2.0/24` is the range set aside
for examples, so no real machine can
be meant), through the same API the
dashboard's *DNS rewrites* page uses
(transcript `t07-rewrites.txt`):

```text
POST /control/rewrite/add  {"domain":"files.example","answer":"192.0.2.50"}
POST /control/rewrite/add  {"domain":"nas.example","answer":"192.0.2.60"}
GET  /control/rewrite/list
[{"domain":"files.example","answer":"192.0.2.50","enabled":true},
 {"domain":"nas.example","answer":"192.0.2.60","enabled":true}]
```

```text
$ dig +tcp @127.0.0.1 files.example A
files.example.		10	IN	A	192.0.2.50
;; Query time: 1 msec

$ dig +tcp @127.0.0.1 nas.example A
nas.example.		10	IN	A	192.0.2.60
;; Query time: 0 msec
```

No upstream was consulted — the query
log entry for these reads reason
`Rewrite`, upstream empty (chapter 9).
Rewrites outrank everything: they are
checked before blocklists and before
upstream, which is why they are also
the sharp tool — a rewrite for a
public name silently redirects that
name for the whole network. The lab's
rule for itself is worth adopting:
rewrites for names you *own* (your
house's names, your test names), never
as a prank on names you don't.

## Deleting, proven

```text
POST /control/rewrite/delete  {"domain":"files.example","answer":"192.0.2.50"}

$ dig +tcp @127.0.0.1 files.example A
files.example.		15	IN	A	198.18.131.114
;; Query time: 28 msec
```

The address is different, the time is
an upstream journey's time, and the
query log shows the question going
upstream again. (At home, a name like
this would likely come back *no such
name* — the correct fate of a deleted
invention; the lab's gateway invents
answers of its own, which is a sandbox
trait, not your server's.) A rewrite
can also be *disabled* without being
deleted — the `enabled` flag in the
list — for the name you need only
sometimes.

## Which names to use at home

Pick a suffix that is yours to use:
a domain you own, or `home.arpa` — the
suffix reserved for exactly this,
home naming — rather than an invented
top-level like `.lan` that could one
day exist publicly and collide. One
rewrite per name is the norm; a name
can carry several answers (including
IPv6 forms) when a machine genuinely
has them.
