# RPM repository server

This directory is the reproducible server-side definition for the supplemental
openEuler RISC-V repository at `http://2.27.148.101:38080`.

A **repository generation** is an immutable snapshot of both binary and source
repository metadata plus the RPM files visible when one accepted batch was
published. `state.json` identifies the latest generation; CI resolves that file
once and then uses only the generation-specific URL, so a later upload cannot
change dependencies midway through a build.

The `reposync` SSH account is not a general shell account. Its sole authorized
key is forced through `rrsync -wo -no-del -no-overwrite` into the non-public
`incoming/` directory. An upload becomes eligible only after a separately
transferred `.ready` manifest binds every RPM to its SHA-256, package, commit,
run, and attempt. The root publisher rejects symlinks, special files, manifest
mismatches, invalid RPMs, and architectures other than `riscv64`, `noarch`,
`src`, or `nosrc` before invoking `createrepo_c`.

The public repository is intentionally served over HTTP because that is the
operator-provided endpoint. The project repository is supplemental and carries
unsigned project RPMs, so its generated DNF configuration uses `gpgcheck=0`.
Trust instead comes from the pinned SSH host key, restricted deploy key,
ready-manifest SHA-256 values, immutable generation URL, and verified
`repomd.xml` digest. The official openEuler repository remains HTTPS and
GPG-checked; this endpoint does not replace it.

Deploy or reconcile the server as root:

```bash
ops/rpm-repo-server/install.sh
```

The installer is idempotent. It creates the empty bootstrap generation, enables
the path watcher and two-minute retry timer, tests Nginx configuration, and
starts the service. Runtime content lives below
`/opt/openeuler-riscv-rpm-repo`; uploads and rejected batches are outside the
Nginx document root.
