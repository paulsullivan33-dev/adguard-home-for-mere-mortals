# What AdGuard Home Is

**Outcome: you can say what happens to
a name when a device in your house asks
for it — and who decides.**

Before anything is a web page or an
app, it is a name: a shop, a mail
server, a video service. Computers
cannot use names directly; they need
numbered addresses. **DNS** — the
Domain Name System — is the worldwide
directory that turns names into
addresses, and every device you own is
constantly asking it questions. Each
question is small, plain, and revealing:
to fetch anything at all, a device must
first announce what it is about to
fetch.

By default those questions go to a
resolver run by someone else — your
internet provider's, usually, chosen by
your router. It answers faithfully, and
it sees everything.

**AdGuard Home is a DNS server you run
yourself, for your own network, that
answers those questions under your
rules.** It is one program, free and
open source, from the AdGuard team. A
device asks it *what is the address of
this name?* and one of four things
happens:

1. **It remembers.** It answered the
   same question recently, so it answers
   from its **cache** at once.
2. **It knows locally.** You taught it
   the name yourself (a **rewrite**, for
   machines in your own house), so it
   answers from your list.
3. **It refuses.** The name is on a
   **blocklist** — an advertiser, a
   tracker, a known malware host — so it
   answers *0.0.0.0*, the address that
   goes nowhere, and the device gives
   up quietly.
4. **It asks upstream.** It forwards the
   question to a resolver **you** chose,
   remembers the answer for next time,
   and passes it back.

That is the whole machine. Everything
else in this guide — the web dashboard,
the statistics, the per-device rules —
is bookkeeping around those four
answers.

## A first taste

With the server running (chapters 3 and
4), asking it a question is one line,
using the standard DNS tool `dig`:

```bash
dig +tcp @127.0.0.1 example.com A
```

```text
example.com.		15	IN	A	198.18.131.110
;; Query time: 40 msec
```

An address came back, in 40
milliseconds, from *your* server — which
had asked its upstream, and will answer
the same question from cache in 0
milliseconds if you ask again (chapter
6 shows both). Ask for a name on the
blocklist and the answer changes
character:

```text
taboola-display.com.	10	IN	A	0.0.0.0
```

No error, no scolding — just an address
that leads nowhere, so the advertisement
never loads. Chapter 7 catches that
answer being produced by a downloaded
list of 188,107 rules, and by a rule
written in the lab in one line.

## The privacy line, stated early

A DNS server is a witness. Its **query
log** records which device asked for
which name at what time — reading it,
you can watch a household wake up, work,
and stream in the evening. AdGuard Home
keeping that log *on your machine*
instead of a provider keeping it on
theirs is the tool's main privacy
argument, and it is a real one. It cuts
both ways: the diary now exists in your
house, under your control, and it is
your responsibility. This guide's line,
stated before any procedure depends on
it:

- Run it for a network you are
  responsible for, and tell the people
  on that network it is running.
- Keep the query log for as long as it
  helps you (the default retention is 90
  days) and no longer.
- The admin interface is protected by
  one password. Treat it like a house
  key: the person holding it can read
  the diary and change the rules.
- Never expose the DNS port or the
  admin page to the internet. A public
  resolver is abused within hours, and
  the admin page is not built to be a
  public website.

## What it is not

AdGuard Home is not a filter *inside*
any app: it cannot remove an
advertisement that is served from the
same name as the content — the famous
case is video-site ads — because at the
DNS level the two are indistinguishable
(chapter 13 is plain about this). It is
not a firewall and not a VPN: it judges
*names*, not traffic. It is not
invisible armour for a device that
ignores it: a phone app or browser that
uses its own encrypted DNS bypasses
your server completely, and chapter 13
names that bypass rather than pretending
it away. And it is not a public good to
offer strangers: it is a household
tool, sized and licensed for a home or
small network.

## Who it is for

The person who wants the trackers in
their house refused at one point
instead of chased app by app. The home
network tinkerer who wants names for
their own machines that work everywhere
in the house. The parent who wants a
per-device switch, not a lecture. The
common thread is one network, one small
machine that is always on, and someone
willing to be its librarian.
