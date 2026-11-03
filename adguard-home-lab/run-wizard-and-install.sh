#!/bin/bash
set -u
BIN=$HOME/workspace/adguard-home-labwork/agh/AdGuardHome/AdGuardHome
LAB=$HOME/workspace/adguard-home-labwork/lab
TR=$HOME/workspace/adguard-home-for-mere-mortals/adguard-home-lab/transcripts
rm -rf "$LAB"; mkdir -p "$LAB"
{
echo '$ AdGuardHome -w $LAB --web-addr 127.0.0.1:18080 --no-check-update   (fresh, empty work dir)'
"$BIN" -w "$LAB" --web-addr 127.0.0.1:18080 --no-check-update --pidfile "$LAB/agh.pid" > "$LAB/server.log" 2>&1 &
sleep 2
echo '$ curl -s -i http://127.0.0.1:18080/'
curl -s -i http://127.0.0.1:18080/
echo
echo '$ curl -s http://127.0.0.1:18080/control/install/get_addresses'
curl -s http://127.0.0.1:18080/control/install/get_addresses; echo
echo '$ curl -s -X POST -d <install choices> /control/install/check_config'
curl -s -X POST -H 'Content-Type: application/json' -d '{"web":{"ip":"127.0.0.1","port":18080},"dns":{"ip":"127.0.0.1","port":53},"username":"admin","password":"lab-password-123"}' http://127.0.0.1:18080/control/install/check_config; echo
echo '$ grep -E "first time|can bind|redirecting|serving" server.log'
grep -E "first time|can bind|redirecting|serving url" "$LAB/server.log"
} > "$TR/t01-first-run-wizard.txt" 2>&1
{
echo '$ curl -s -X POST -d <install choices> /control/install/configure'
curl -s -X POST -H 'Content-Type: application/json' -d '{"web":{"ip":"127.0.0.1","port":18080},"dns":{"ip":"127.0.0.1","port":53},"username":"admin","password":"lab-password-123"}' -w '\nHTTP %{http_code}\n' http://127.0.0.1:18080/control/install/configure
sleep 2
echo '$ curl -s http://127.0.0.1:18080/control/status   (no login cookie yet)'
curl -s -w '\nHTTP %{http_code}\n' http://127.0.0.1:18080/control/status
echo '$ curl -s -c cookies.txt -X POST -d {"name":"admin","password":"lab-password-123"} /control/login'
curl -s -c "$LAB/cookies.txt" -H 'Content-Type: application/json' -d '{"name":"admin","password":"lab-password-123"}' -w '\nHTTP %{http_code}\n' http://127.0.0.1:18080/control/login
echo '$ curl -s -b cookies.txt http://127.0.0.1:18080/control/status'
curl -s -b "$LAB/cookies.txt" http://127.0.0.1:18080/control/status; echo
echo '$ find lab work dir -type f'
find "$LAB" -type f | sort
echo '$ AdGuardHome -c lab/AdGuardHome.yaml --check-config'
"$BIN" -c "$LAB/AdGuardHome.yaml" --check-config; echo "exit:$?"
echo '$ grep key lines of AdGuardHome.yaml (password hash deliberately not shown)'
grep -E 'address: 127|^- name|port: 53|dns10.quad9|name: AdGuard' "$LAB/AdGuardHome.yaml"
} > "$TR/t02-install-and-login.txt" 2>&1
echo done
