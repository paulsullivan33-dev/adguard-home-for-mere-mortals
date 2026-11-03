# Your First Lookups

**Outcome: real DNS questions asked of
your server and answered, with times —
and one honest wall, met head-on and
named.**

The tool for asking DNS questions by
hand is **dig**, the standard lookup
client. Point it at your server with
`@127.0.0.1`; everything after the
address is the question.

## The wall (read this first)

The lab's first attempts looked like
this (transcript `t03-dns-queries.txt`):

```bash
dig @127.0.0.1 example.com A
# ;; communications error to 127.0.0.1#53: timed out
```

Repeatedly — no answer at all, while
the server was demonstrably running and
its log showed it *listening* on UDP
port 53. The log also showed the
reason, and it is the sandbox, not the
product (transcript
`t11-sandbox-udp-evidence.txt`): every
attempt to **send a UDP answer** failed
with `sendmsg: operation not
permitted`. The sandbox lets the
process receive UDP questions but not
send UDP answers. On any ordinary
machine this restriction does not
exist; inside this lab it is absolute.

DNS has a second, fully standard way
to travel: **TCP**, on the same port.
Nothing about the questions changes —
only the envelope. So the lab asked
over TCP for the rest of the guide:

```bash
dig +tcp @127.0.0.1 example.com A
```

Everything from here on is real: real
questions, really forwarded, really
answered, really timed. Where the
distinction could matter to a claim,
the guide says *over TCP* out loud.

## First answers

At first the server still could not
answer completely: its default upstream
is encrypted DNS at Quad9, and reaching
it requires a one-time **bootstrap**
lookup over plain UDP to the
internet — also walled off in this
sandbox, and recorded failing in the
same log (`no addresses` for the
upstream's name). Chapter 6 tells that
story and makes the change the lab
made: the upstream became the sandbox
gateway's resolver, the lab equivalent
of a home router's resolver. With that
one change, questions flowed
(transcript `t05-dns-over-tcp.txt`):

```text
$ dig +tcp @127.0.0.1 example.com A +noall +answer +stats
example.com.		15	IN	A	198.18.131.110
;; Query time: 40 msec

$ dig +tcp @127.0.0.1 example.com A        (again)
example.com.		15	IN	A	198.18.131.110
;; Query time: 0 msec
```

(The `198.18…` address is the sandbox
gateway's own synthetic answer — in a
home the same line would carry the
real public address your upstream
returned. The shape and the timing are
the lesson, and they are genuine.)

Three things to read in that output:

- **An answer, with a TTL.** `15` is
  the answer's *time to live* in
  seconds: how long anyone may remember
  it. Your server honours it.
- **40 ms, then 0 ms.** The first ask
  travelled to the upstream and back.
  The second was served from your
  server's **cache** — the single most
  common thing AdGuard Home will ever
  do for you, measured.
- **The same question, a different
  road.** Over UDP at home these take
  the same few milliseconds; nothing in
  the rest of this guide depends on
  which envelope carried the question.

## Two more shapes of answer

An **AAAA** question (the IPv6 form of
an address) for a name whose upstream
answer has none returns a successful,
empty answer — *no error, no address*
— which is DNS for "that form does not
exist" (t05). And an **ANY** question,
which asks for everything at once and
is a favourite of abuse, is refused
with `NOTIMP` by default: the
`refuse_any` setting doing its quiet
job (t10).
