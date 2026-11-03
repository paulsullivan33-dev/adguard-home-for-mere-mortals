# Recipes

**Outcome: four jobs from real life,
each built only from moves the earlier
chapters proved — with the one step
the lab could not do labelled where it
sits.**

## 1. Point a house at your server

The server is only useful once devices
ask *it*. The order matters:

1. Give the server machine a **fixed
   address** on your network (a DHCP
   reservation on the router, or a
   static address). Every recipe below
   assumes it never moves.
2. On **one device first** — a laptop —
   set its DNS server to your machine's
   address by hand. Use it for a day.
   Read its entries in the query log
   (chapter 9): you should see its
   questions, its blocked names, and no
   surprises.
3. Then change the **router's** DHCP
   settings to hand out your server's
   address as the DNS server. Devices
   pick it up as their leases renew.
   Keep the router's own address
   written down; reverting is changing
   one field back.

Step 3 is the step the lab did not
perform (it changed no router) and it
is described from the product's
documentation and the shape of home
routers generally; steps 1–2 are the
parts that catch every mistake cheaply,
including the classic: a second DHCP
server. AdGuard Home's own DHCP stays
**off** unless you deliberately retire
the router's — two DHCP servers on one
network is a fault, not a redundancy.

## 2. Add a second list

In *Filters → DNS blocklists*, add a
list by URL (several curated
collections exist; the Hostlists
Registry the defaults came from is the
sane shelf to browse). Refresh, note
the rule count before and after, then
spot-check one name *from the new
file* the way chapter 7 did — a name
out of the downloaded list, blocked,
is proof; a name you merely believe is
in it is not. The caution: every list
is someone else's judgement, applied
to your whole house. Add lists one at
a time, days apart, so when something
breaks you know whose arrival to
suspect.

## 3. Carve an exception

A needed site breaks; the query log
(chapter 9) shows the blocked name
and the rule that caught it. Add one
exception to your custom rules:

```text
@@||the-exact-name.example^
```

`@@` is the allow marker; the rest of
the pattern names exactly the one
name. Ask again — the lab's rule
tests in chapter 7 are the model for
proving the exception works and that
its neighbours still block. Resist
the broad exception (`@@||*.example^`
and kin): carve the hole the size of
the name, never the size of the
domain family, and write a `#` comment
above it saying why it exists, dated.
Future you, reading the rules at
midnight, is a reader too.

## 4. The one-pass health check

Everything the guide proved, as a
standing checklist for your install:

```text
1. --check-config on your config file      -> "configuration file is ok"
2. /control/status, logged in              -> running: true, protection_enabled: true
3. dig a name you rewrote                  -> your address, ~0 ms, log says Rewrite
4. dig a name from your biggest list       -> 0.0.0.0, log names the rule
5. dig an ordinary name, twice             -> answered; second time ~0 ms (cache)
6. query log, newest entries               -> reasons you recognise, clients you know
```

Five minutes, six checks, and every
moving part from chapter 2 has been
touched. When one fails, chapter 14 is
ordered to meet it.
