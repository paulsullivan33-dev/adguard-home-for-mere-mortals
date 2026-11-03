# Troubleshooting

**Outcome: the failures this guide
actually met — and the common ones it
can diagnose from the evidence — each
with the check that names it.**

Failures here are ordered roughly by
how a new install meets them. Every
check is one you have already seen
work in an earlier chapter.

## The wizard writes no config (500 on configure)

**Seen in the lab.** Installing with a
*relative* `--work-dir` produced
`Couldn't write config: … work2/work2/
.AdGuardHome.yaml: no such file or
directory` — the program resolved the
path twice. **Check:** the error names
the doubled path. **Fix:** stop it,
start again with an **absolute**
`--work-dir` path, and the same
choices install cleanly (chapter 4).

## Questions time out, though the server is up

**Seen in the lab.** `dig` over UDP
timed out while the log showed the
server listening — and, one level
down, `responding request … sendmsg:
operation not permitted` on every
answer. The sandbox forbade the
process sending UDP at all.
**Check in general:** the server log's
*responding* errors separate "never
heard the question" from "answered
and it vanished" — two different
faults wearing one symptom. Try
`dig +tcp`: if TCP answers, the server
and its config are fine and the fault
is in the UDP path (firewall, sandbox,
or something else holding port 53).

## The upstream never answers ("no addresses")

**Seen in the lab.** With the default
encrypted upstream, exchanges failed
with `no addresses`: the upstream's
own name could not be resolved because
the bootstrap path (plain UDP, to the
internet) was blocked. **Check:** read
the failing name in the log — a
failing *upstream name* is a bootstrap
problem; a failing *question* is an
upstream problem. **Fixes:** working
bootstrap addresses, an upstream given
by address rather than name, or a
local upstream — the lab took the
third (chapter 6).

## A blocked name is answered anyway

Work through, in this order:

1. **Protection on?** `/control/status`
   says `protection_enabled` — the lab
   proved what *off* does to a blocked
   name (chapter 7).
2. **The client exempt?** A persistent
   client with filtering off answers
   everything (chapter 10) — check the
   log entry's client against your
   client list before blaming the rule.
3. **Just changed the rule?** The
   engine reloads after list/rule
   changes; the lab's first question in
   the same second slipped through, the
   next was refused. Wait, ask again.
4. **Cached?** An answer fetched
   before the rule existed lives out
   its TTL. Blocking answers carry a
   short TTL; real ones may not.
5. **Is the name really the name?**
   Read the query log: the entry names
   the rule when a rule fired, and
   silence in the log means the device
   never asked *you* — it is using
   another resolver entirely (chapter
   13's bypass, met in the wild).

## A wanted site broke after a new list

The query log is the diagnosis: find
the device, find the refused name,
read the rule. Then the exception is
one `@@||` line (chapter 11), not a
disabled list. If the refused name is
a CDN or an API the site needs, the
same recipe applies — carve the one
name, write the dated comment.

## Locked out of the dashboard

A wrong password gets `403 invalid
username or password` — and the
config's guard (`auth_attempts: 5`,
`block_auth_min: 15`) waits out
repeated guessing, including yours.
Forgotten entirely: stop the server,
and edit the `users:` section of
`AdGuardHome.yaml` to replace the
stored hash with a new one generated
by the program's documented procedure
(the project's help pages carry it),
then `--check-config` before starting.
The hash in the file is a bcrypt of
your password; the file's permissions
are why the program fussed about them
in chapter 3.

## The config will not start

`--check-config` is the check, and it
earns its keep: the lab fed it a file
with an unclosed bracket and got the
parser's exact complaint — line and
column — with **exit 1**, instead of a
server that fails mysteriously at
boot. Run it after every hand edit;
keep the wizard's original file backed
up before the first one.

## Port 53 is already taken

The wizard's check step reports the
DNS port unusable, and on Ubuntu the
tenant is usually the stub resolver.
The fix is system configuration —
move or disable the stub listener, or
bind AdGuard Home where it does not
stand — and it is deliberately a
*system* change, made knowingly, not
something the installer does behind
your back. Chapter 13 names the wider
point: bind the address you mean.
