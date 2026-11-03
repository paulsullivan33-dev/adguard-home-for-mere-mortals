# Limits

**Outcome: you can name what this
tool cannot do before it surprises
you — the honest edges, collected.**

**DNS-level blocking is name-level
blocking.** An advertisement served
from the same name as the content —
the arrangement several large video
and social services use — cannot be
refused without refusing the content.
No list fixes this; it is the method's
edge, not the product's failure.
Browser-level tools (chapter 12) see
more and can cut finer, on one device
at a time.

**Devices can walk around it.** Any
app or browser that uses its own
encrypted DNS goes straight to its
chosen resolver and your server never
sees the question. Modern browsers
ship this, sometimes on. Your server
governs the devices that ask it;
chapter 11's first recipe makes that
most of a house, not all of it, and
the query log's silences are data, not
proof of virtue.

**It is a single point of failure.**
When your server is down, a house
pointed only at it has no DNS, which
reads as *the internet is broken* for
every device at once. Mitigations are
real but partial: a second resolver
in the router's settings helps only
if clients use it as fallback rather
than as an equal (many treat the list
as a menu and leak questions to the
unfiltered entry on good days too).
Choose consciously: purity, or a
safety net with holes.

**Port 53 is contested ground.** On
many systems something already listens
there — Ubuntu's stub resolver is the
usual tenant — and AdGuard Home
cannot bind until it is moved or
disabled. The wizard's port check
catches it (chapter 14), and a server
meant for a whole house should bind
its real address deliberately, not
inherit a loopback habit from a lab.

**Identification is soft.** Per-client
rules key on IP or MAC addresses
(chapter 10). Addresses change
(without reservations), MAC addresses
randomise (phones do this by design),
and a determined teenager with a VPN
app is not a DNS problem at all. The
rules are good manners enforcement
for a household, not access control
against an adversary.

**The diary is a liability as well as
a tool.** The query log knows when
the house wakes, works, and streams.
Ninety days of it, the default
retention, is a long memory; set it
shorter if your troubleshooting does
not need it (chapters 1 and 9).

**Scale and shape.** It is built for a
home or small network: one config
file, one admin model (named users
with one password each — not roles
and permissions), lists counted in
the hundreds of thousands of rules
comfortably and not in the tens of
millions. And its own extras have
edges: the DHCP server is a
stand-in, not a router's equal; the
safe-browsing and parental verdicts
are AdGuard's services speaking, with
their own false positives; rule
syntax can express more than a
household should attempt.

**And the lab's own ceiling,** stated
once more where limits live: in this
guide's sandbox, UDP answers could
not be sent and the public encrypted
upstream could not be reached, so the
live proof ran over TCP against a
local upstream. The product's UDP
serving and public DoH upstream are
its most ordinary paths in the world —
documented here, configured and read
in the lab's real config — but they
were not the paths the lab could
walk, and the guide does not pretend
otherwise. `criteria.md` is the
ledger.
