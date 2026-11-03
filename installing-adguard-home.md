# Installing AdGuard Home

**Outcome: an `AdGuardHome` program on
your machine that states its version —
before any network enters the picture.**

AdGuard Home is one self-contained
program. There is no installer to run
and no database to set up first: you
download one archive from the project's
own releases, unpack it, and the binary
inside is the whole product — web
interface, DNS server and all.

## The release download

The lab installed **v0.107.79** from
the official GitHub releases
(`github.com/AdguardTeam/AdGuardHome`).
There is one archive per platform —
`AdGuardHome_linux_amd64.tar.gz` for
ordinary 64-bit Linux PCs, with builds
for ARM boards (Raspberry Pi included),
macOS and Windows beside it. The lab's
download was 12 MB, SHA-256
`c48f4a43000665484c5ec28177de11a004759b620dae8f77b2aabefc9ef3687f`
— your version's hash will differ, and
checking it against the release page is
the habit, not the number.

Unpacked, the archive is small and
complete:

```text
AdGuardHome/
  AdGuardHome        the program (35 MB, statically linked)
  AdGuardHome.sig    its signature file
  CHANGELOG.md
  LICENSE.txt
  README.md          the project's own notes
```

Nothing is written into your system:
no package manager, and deleting the
folder removes it. The lab ran it
straight from the unpacked folder, with
its working data in a separate
directory it was told about — which is
also how you should think of it in
production: the *program* is
replaceable, the *work directory*
(config, lists, logs) is the part you
keep.

## The check

```bash
./AdGuardHome --version
```

```text
AdGuard Home, version v0.107.79
```

That is this chapter's acceptance test
(transcript `t00-download-and-version.txt`
keeps the download, the hash and this
output). `--help` lists the options;
the ones this guide uses are:

```text
-c, --config VALUE        Path to the config file.
-w, --work-dir VALUE      Path to the working directory.
    --web-addr VALUE      Address to serve the web UI on, in the host:port format.
-s, --service VALUE       Service control action: status, install, uninstall, start, stop, restart, reload.
    --check-config        Check configuration and exit.
    --no-check-update     Don't check for updates.
-v, --verbose             Enable verbose output.
    --version             Show the version and exit.
```

Two warnings from the lab's own
experience, both cheap to learn here
instead of there. First, give
`--work-dir` an **absolute path**: with
a relative one, the install step later
tried to write its config under the
path twice and failed (chapter 14 tells
that story). Second, the program cares
about the work directory's permissions
and says so in its log (`permcheck`
warning) — it keeps a password hash and
a diary in there, so the fussiness is
justified; `0700` is what it wants.

## The other ways in

On a real machine you will usually also
register it as a service —
`./AdGuardHome -s install` sets that up
on systems with a service manager, so
it starts at boot and restarts if it
falls. The lab had no service manager
and ran the binary directly throughout;
the service form is documented-only in
this guide. The project also publishes
container images and packages for
several systems; the release binary is
the path this guide verifies, and the
others put the same binary in a
different wrapper.
