#!/bin/bash
set -u
BIN=$HOME/workspace/adguard-home-labwork/agh/AdGuardHome/AdGuardHome
LAB=$HOME/workspace/adguard-home-labwork/lab
CK=$LAB/cookies.txt
echo '$ dig +tcp taboola-display.com A   (baseline: blocked by the list)'
dig +tcp @127.0.0.1 taboola-display.com A +noall +answer +stats
echo '$ curl -s -b cookies.txt -X POST -d {"enabled":false,"duration":0} /control/protection'
curl -s -b "$CK" -H 'Content-Type: application/json' -d '{"enabled":false,"duration":0}' -w '\nHTTP %{http_code}\n' http://127.0.0.1:18080/control/protection
sleep 1
echo '$ curl -s -b cookies.txt /control/status'
curl -s -b "$CK" http://127.0.0.1:18080/control/status; echo
echo '$ dig +tcp taboola-display.com A   (protection off: the list no longer applies)'
dig +tcp @127.0.0.1 taboola-display.com A +noall +answer +stats
echo '$ curl -s -b cookies.txt -X POST -d {"enabled":true} /control/protection'
curl -s -b "$CK" -H 'Content-Type: application/json' -d '{"enabled":true}' -w '\nHTTP %{http_code}\n' http://127.0.0.1:18080/control/protection
sleep 1
echo '$ dig +tcp cursosmarketing.info A   (a second list domain: blocked again)'
dig +tcp @127.0.0.1 cursosmarketing.info A +noall +answer +stats
echo
echo '$ curl -s -i -X POST -d {"name":"admin","password":"wrong-password"} /control/login   (bad password)'
curl -s -i -H 'Content-Type: application/json' -d '{"name":"admin","password":"wrong-password"}' http://127.0.0.1:18080/control/login | head -8
echo
echo '$ dig +tcp @127.0.0.1 example.com ANY +noall +comments   (refuse_any)'
dig +tcp @127.0.0.1 example.com ANY +noall +comments
echo '$ printf "http:\n  address: [unclosed\n" > bad.yaml; AdGuardHome -c bad.yaml --check-config'
printf 'http:\n  address: [unclosed\n' > "$LAB/bad.yaml"
"$BIN" -c "$LAB/bad.yaml" --check-config; echo "exit:$?"
