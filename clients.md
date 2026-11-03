# Clients and Per-Device Rules

**Outcome: the same question, asked by
two different devices, getting two
different answers — on purpose.**

A house is not one user. The games
console, the children's tablet, the
laptop that pays the bills and the
phone that tests things have different
needs, and AdGuard Home's answer is
the **client**: a named device (or
group) with its own settings, sitting
on top of the global ones.

## Who the server thinks is asking

Even before you define anything, the
server keeps track of askers. The
lab's list (`GET /control/clients`)
showed **auto clients** it had
identified from the machine's hosts
file and neighbourhood — the lab's own
asker as `localhost`, and the sandbox
gateway wearing a hosts-file name.
On a home network this is where your
devices appear, by address, gathering
names where the server can learn them
(DHCP, reverse lookups, hosts files).

A **persistent client** is one you
define yourself: a name, one or more
**IDs** it is recognised by (an IP
address, a MAC address, or a ClientID
for encrypted DNS), and its settings —
filtering, parental controls, safe
browsing, safe search, blocked
services, even its own upstreams.
`use_global_settings` decides whether
the house rules apply under the
client's own.

## The proof: one device, exempted

The lab defined a persistent client
for its own asking address with
filtering **off**, leaving everything
else global (transcript
`t09-clients.txt`):

```text
before:   dig ads.example.com  -> 0.0.0.0        (custom rule blocks it)
add client  lab-client, ids=[127.0.0.1], filtering_enabled=false
after:    dig ads.example.com  -> 198.18.131.112 (answered, upstream)
delete the client
again:    dig ads.example.com  -> 0.0.0.0        (house rule returns)
```

Same server, same rule, same question:
the client's setting overruled the
house's, and removing the client
restored the house's answer. That is
the whole chapter in one exchange —
per-device policy is real, immediate,
and (note well) only as strong as the
identification: a client recognised by
IP address is recognised *as whoever
holds that address*, which is why
chapter 11 pairs this with fixed
addresses for the devices whose rules
matter.

What the lab did not exercise: MAC
and ClientID identification, client-
specific upstreams, and the blocked-
services per client — all present in
the same API object the lab used, and
described here from the documentation.
The mechanism they ride on — client
settings overruling global ones — is
the part that was proven.
