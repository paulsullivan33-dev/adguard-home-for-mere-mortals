# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's names are reserved example domains and its
   addresses are documentation ranges or loopback.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: name-level blocking that cannot separate ads
   served from the content's own name, devices and apps that
   bypass it with their own encrypted DNS, the single point of
   failure it creates for a network, port 53 contention,
   IP/MAC identification too soft for access control, the
   query log's sensitivity, household scale, and the lab's
   own ceiling — UDP answers unsendable and the public
   encrypted upstream unreachable inside its sandbox, so the
   live proof ran over TCP against a local upstream.
8. **The ethics rule is in the text, early.** A DNS server
   sees every name every device on the network looks up, and
   its query log is a diary of the household. Chapter 1 and
   the README state the line before any procedure depends on
   it: run it only on a network you are responsible for, tell
   the people on that network, keep the log only as long as
   it serves a purpose, guard the single admin password like
   a house key, and never expose the DNS port or admin page
   to the internet, where an open resolver is abused and the
   log-keeper becomes the leak.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran. AdGuard Home
**v0.107.79** was installed from the official release archive
`AdGuardHome_linux_amd64.tar.gz` (12 MB, SHA-256
`c48f4a43000665484c5ec28177de11a004759b620dae8f77b2aabefc9ef3687f`)
from the project's GitHub releases and run unmodified, bound
to loopback: web interface on port 18080, DNS on port 53.
All transcripts live in `adguard-home-lab/transcripts/`; the
scripts that drove the web API are in `adguard-home-lab/`.

Two sandbox ceilings shaped the lab and are stated wherever
they touch a claim. **First, UDP:** the process could bind
UDP port 53 and receive questions, but every attempt to send
a UDP answer failed with `sendmsg: operation not permitted`
in the server log (t11), so `dig` over UDP timed out (t03).
All live DNS exchanges were therefore run over **TCP** on
the same port — a standard, supported transport — and every
result quoted is from those exchanges. **Second, the
upstream:** the default upstream (Quad9 DNS over HTTPS)
needs a bootstrap lookup over plain UDP to the internet,
which the sandbox also blocks; the log records the exchange
failing with "no addresses" (t11). The lab therefore set the
upstream, through the product's own API, to the sandbox
gateway's resolver at 198.19.0.1 (the resolver in the lab
machine's own `/etc/resolv.conf`; verified answering a
direct dig in 5 ms, t04) — the same configuration shape as a
home install pointed at a router's resolver. The gateway
returns synthetic addresses in a benchmarking range, which
is why answer addresses in the transcripts look unusual;
the guide says so where they appear. AdGuard Home's UDP
serving and its public encrypted upstream are its ordinary
paths in the world; here they are configuration-verified
and documented, not walked, and the text never claims
otherwise.

Run for real, with transcripts as evidence:

- Download, hash, unpack, `--version` (v0.107.79) and the
  full `--help` option list (t00).
- First run on an empty work directory: redirect to the
  install wizard, the address list the wizard offers, and
  its check step passing for web 127.0.0.1:18080 and DNS
  127.0.0.1:53 (t01).
- Install through the wizard's own API: config written
  (`AdGuardHome.yaml`, schema version 34), unauthenticated
  status refused with 401, login with the lab password,
  authenticated status showing the running server (t02);
  `--check-config` accepting the generated file (t02) and
  rejecting a deliberately broken one with the parser's
  message and exit 1 (t10).
- DNS over TCP with the local upstream: `example.com` A
  answered in 40 ms and again in 0 ms from the cache;
  an AAAA question answered empty; an ANY question refused
  with NOTIMP under the default `refuse_any` (t05, t10).
- Blocking: the enabled AdGuard DNS filter refreshed to
  188,107 rules; a name taken from the downloaded file
  (`taboola-display.com`) refused with 0.0.0.0 at TTL 10;
  a custom rule `||ads.example.com^` refusing the name and
  its subdomain while the parent domain still answered
  (t06).
- Rewrites: two invented names added, listed, answered
  locally at their documentation addresses, one deleted
  and the same name then answered from upstream (t07).
- The query log read back with reasons (`Rewrite`,
  `FilteredBlackList` with the rule named,
  `NotFilteredNotFound` with the upstream named), clients
  and timings; the statistics totals (23 queries, 4
  blocked) and top-domain tables; the auto-client list
  (t08).
- Clients: a persistent client for the lab's own address
  with filtering off, the same blocked name then answered,
  and the client deleted with blocking restored (t09).
- Protection off and on through the API, with a listed
  name answered while off and a second listed name
  refused again when back on; a wrong password refused
  with 403 and its exact message (t10).

Documented only — described from the project's
documentation and the generated config, not run, and the
text does not claim otherwise:

- DNS serving over UDP, and any use of the public
  encrypted upstreams (DoH/DoT/DoQ), per the ceilings
  above. Upstream modes beyond the single-upstream lab
  (load_balance was the mode in force and is named in the
  log; parallel and fastest are described, not run).
- AdGuard Home serving encrypted DNS to clients (its own
  DoH/DoT/DoQ with certificates), and the built-in DHCP
  server handing out addresses on a real network.
- Safe browsing, parental control and safe search
  verdicts (their counters appear in the real statistics,
  all zero; no live catch is claimed), blocked-services
  lists, per-client upstreams, and MAC/ClientID client
  identification (the client mechanism itself was proven
  by IP, t09).
- Registering the program as a system service
  (`-s install`), the container and package installs,
  changing a real router's DHCP/DNS settings (recipe
  chapter 11, step 3), and the neighbour tools of
  chapter 12, characterised from their documentation and
  this series' own guides (Pi-hole and Unbound were run
  live in *their* labs, not this one).

Fixtures are this guide's own and deliberately generic:
reserved `example` domains for questions and rules, a
blocklist name taken from the downloaded list itself as
the blocking specimen, documentation-range addresses
(192.0.2.50, 192.0.2.60) for rewrites, and one throwaway
lab password. The admin password's bcrypt hash appears in
no transcript. Nothing was exposed beyond loopback, and
every server the lab started was stopped when the lab
finished.
