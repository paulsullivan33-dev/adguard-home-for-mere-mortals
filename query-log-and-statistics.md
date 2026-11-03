# The Query Log and Statistics

**Outcome: for any question your
server was asked, you can find the
entry that records what happened and
why — and read the dashboard's
counters as the same diary, added
up.**

Every other chapter's claim in this
guide was checked here. The **query
log** is AdGuard Home's memory of
individual questions; the
**statistics** are its totals. Both
are in the dashboard — *Query Log* and
the top of the home page — and both
come from the same API the lab read
(transcript
`t08-querylog-and-stats.txt`).

## Reading a log entry

The lab's log, trimmed to the fields
that matter, after the blocking and
rewrite chapters had done their work:

```text
01:00:06  files.example A        -> 192.0.2.50     reason=Rewrite            client=127.0.0.1 (localhost)  0.1 ms
01:00:06  nas.example A          -> 192.0.2.60     reason=Rewrite            client=127.0.0.1 (localhost)  0.1 ms
00:59:54  www.ads.example.com A  -> 0.0.0.0        reason=FilteredBlackList  rule=||ads.example.com^       0.1 ms
00:59:54  ads.example.com A      -> 0.0.0.0        reason=FilteredBlackList  rule=||ads.example.com^       0.5 ms
00:59:54  example.com A          -> 198.18.131.110 reason=NotFilteredNotFound upstream=198.19.0.1:53        3.8 ms
01:00:06  files.example A        -> 198.18.131.114 reason=NotFilteredNotFound upstream=198.19.0.1:53       28.2 ms
```

Each entry answers the five questions
you actually bring to a log:

- **What was asked** — the name and
  type, exactly as the device asked.
- **What was answered** — the address,
  or `0.0.0.0` for a refusal, or
  nothing for an empty answer.
- **Why** — the `reason`. The lab met
  three, which between them cover most
  of life: `Rewrite` (a local name),
  `FilteredBlackList` (a list or a
  custom rule — and the entry names
  the **rule**), and
  `NotFilteredNotFound` — an
  unglamorous name for the ordinary
  case: not filtered, and the answer
  came from upstream (named in the
  entry) or cache.
- **Who asked** — the client address,
  with a name when the server knows
  one (it learned `localhost` from the
  machine's hosts file).
- **How long it took** — which is how
  cache hits (≈0 ms) and upstream
  journeys (milliseconds to tens of
  milliseconds) announce themselves.

When something in the house misbehaves
— an app that will not load, a site
half-broken — this is the first place
to look: filter the log to the device,
read the *why* column, and the culprit
rule, if there is one, is printed on
the entry. Chapter 11's "carve an
exception" recipe starts here.

## The totals

```text
num_dns_queries:           23
num_blocked_filtering:     4
avg_processing_time:       0.007
top_queried_domains:  example.com 10, example.org 4, files.example 2, …
top_blocked_domains:  ads.example.com 2, taboola-display.com 1, www.ads.example.com 1
```

Small numbers — a lab's afternoon, not
a household's week — but the shape is
the one your dashboard will show at
scale: total questions, how many were
refused by filtering, the busiest
names in each direction, and the
counters for the safe-browsing,
parental and safe-search replacements
(all zero in the lab: nothing asked
matched them). Two cautions of
interpretation. *Blocked* counts
questions, not advertisements — one
page can ask thirty questions. And a
name high in *top queried* is usually
just a chatty device or a service
polling, not a villain; the log, not
the league table, is where judgement
happens.

## Retention, deliberately

The wizard's defaults keep the query
log **90 days** and the statistics
**1 day** (both in the config, both
changeable, statistics commonly set
longer). Chapter 1's line applies in
concrete form here: the log is a
diary; keep the retention as short as
your troubleshooting habit allows, and
know that the dashboard offers both a
pause and a clear for the log when a
situation calls for it. The entries
are the household's, on the household's
machine — that is the improvement over
a provider's log, not a licence to
forget they are sensitive.
