# Blocking — Lists and Your Own Rules

**Outcome: a name on a list — or on a
rule you wrote — gets the empty answer,
a name on neither gets through, and
you can prove both in one sitting.**

This is the chapter the tool is famous
for. It is also where guides often
assert instead of showing, so this one
shows everything, using names taken
from the evidence itself.

## The lists

Out of the wizard, the config carries
two blocklists:

- **AdGuard DNS filter** — enabled.
- **AdAway Default Blocklist** —
  present, disabled.

A **refresh** downloads the enabled
lists to the `data/filters/` folder
and loads them. The lab's refresh
reported the AdGuard list at
**188,107 rules** (transcript
`t06-blocking.txt`). A rule in these
lists is usually one line per name:

```text
||taboola-display.com^
```

Read it as: *the name
`taboola-display.com`, and anything
under it, starting here, ending there*
— AdGuard's rule syntax, shared with
its browser products, of which a home
user needs perhaps four patterns
(below).

## Proof, from the list itself

Rather than trusting a famous name,
the lab took a name out of the
downloaded file and asked for it:

```text
$ grep -m1 taboola lab/data/filters/1.txt
||taboola-display.com^

$ dig +tcp @127.0.0.1 taboola-display.com A
taboola-display.com.	10	IN	A	0.0.0.0
```

`0.0.0.0` — the blocking answer, with a
10-second TTL (the config's
`blocked_response_ttl`) instead of a
real answer's longer life, so a name
wrongly listed recovers quickly once
the list is fixed. The query log
(chapter 9) records *why*: reason
`FilteredBlackList`, with the rule
attached.

Lists update themselves on an
interval (24 hours in the config), and
the refresh the lab ran by hand is the
same call the dashboard's *Update*
button makes. More lists can be added
by URL in the same settings — chapter
11 has a recipe and a caution about
list enthusiasm.

## Your own rules

**Custom rules** live in the filtering
settings (`user_rules`), in the same
syntax. The lab added one line:

```text
||ads.example.com^
```

and then proved the three claims such
a rule makes (t06):

```text
ads.example.com      -> 0.0.0.0    (the name itself)
www.ads.example.com  -> 0.0.0.0    (|| covers subdomains)
example.com          -> answered  (the rule reaches no further)
```

The patterns worth learning:

- `||name^` — block this name and its
  subdomains. The everyday rule.
- `@@||name^` — an **exception**: allow
  this name even if a list blocks it.
  How you carve one hole, deliberately.
- `|name` / `name|` — anchor to the
  start / end, for surgical cases.
- `/regex/` — a regular expression,
  for the rare day the above will not
  do. Reach for it last: it is the only
  pattern that can surprise you at
  scale.

One trap the lab met and now warns
about: the rule was set through the
API and the *status* showed it at
once, but the first question asked in
the same second was still answered —
the engine was mid-reload from the
list refresh. Asked again moments
later, the name blocked and stayed
blocked. If a new rule seems ignored,
wait a few seconds and ask again
before doubting the syntax (chapter 14
keeps this).

Two neighbouring features share this
engine and are set in the same place:
the **blocked services** list (whole
services — games, messengers, social
networks — refused at the name level)
and the optional **safe browsing** and
**parental** checks, which consult
AdGuard's hashed-prefix services for
known-bad and adult names. The lab's
statistics show their counters (all
zero — nothing asked matched), and
this guide describes them from the
documentation rather than claiming a
live catch.

## The protection switch

All of it — lists, rules, checks — is
under one switch: **protection**. The
lab turned it off and on through the
API (transcript
`t10-protection-and-failures.txt`):

```text
protection off -> taboola-display.com answered normally
protection on  -> the next list name asked is refused again
```

It is the pause button for the day a
site breaks and you need to know
whether your own server is the reason:
one click narrows the fault to *with
protection* or *without*. It can also
be switched off *for a duration*, after
which it returns by itself — kinder
than a setting forgotten.
