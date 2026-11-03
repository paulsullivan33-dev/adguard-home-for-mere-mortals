# Glossary

**Blocklist** — a downloaded list of
names to refuse, one rule per line.
The lab's AdGuard DNS filter held
188,107 rules.

**Blocking answer** — the reply given
for a refused name: by default
`0.0.0.0` for an A question, with a
short TTL — an address that goes
nowhere, so the request quietly dies.

**Bootstrap** — the plain-address
resolvers asked once, to find the
address of an encrypted upstream
whose name itself needs resolving.

**Cache** — answers remembered for
their TTL and served without asking
upstream again. The lab measured
40 ms, then 0 ms.

**Client** — a device the server
identifies as an asker. A
**persistent client** is one you
defined, with its own settings that
can overrule the house's.

**Custom rules** (`user_rules`) —
your own lines in AdGuard's rule
syntax, checked alongside the lists.

**dig** — the standard DNS lookup
tool: asks one question, shows the
answer and its timing. This guide's
measuring instrument.

**DNS** — the Domain Name System: the
directory that turns names into
addresses, one small question at a
time.

**DNS over HTTPS / TLS / QUIC
(DoH / DoT / DoQ)** — DNS questions
carried inside an encrypted
connection, so the path cannot read
them. AdGuard Home can *use* all
three upstream, and *serve* them to
clients with certificates.

**Port 53** — the standard DNS port,
for both UDP (usual) and TCP (the
path this guide's lab used).

**Protection** — the master switch
over lists, rules and checks. Off,
the server answers everything it can;
it can be timed to return by itself.

**Query log** — the per-question
diary: name, answer, reason, rule,
upstream, client, time taken. Where
every claim in this guide was
checked.

**Reason** — the log's verdict on a
question: `Rewrite`,
`FilteredBlackList`, and
`NotFilteredNotFound` (ordinary:
sent on and answered) are the three
this guide met.

**Rewrite** — a name you teach the
server to answer itself, with an
address you choose. Checked before
lists and upstream.

**Rule syntax** — AdGuard's pattern
language: `||name^` blocks a name and
its subdomains; `@@` in front makes
an exception; anchors and regular
expressions exist for rare surgery.

**TTL (time to live)** — the seconds
an answer may be remembered, set by
the answer itself. Blocking answers
carry a short one (10 s by default).

**Upstream** — the resolver your
server asks when it neither knows
nor refuses. Chosen by you; asked in
load-balance, parallel, or fastest
mode when there are several.
