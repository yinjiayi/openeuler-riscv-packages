# RPM repository server

This directory is the reproducible server-side definition for the supplemental
openEuler RISC-V repository at `http://2.27.148.101:38080`.

A **repository generation** is an immutable snapshot of both binary and source
repository metadata plus the RPM files visible when one accepted batch was
published. `state.json` identifies the latest generation; CI resolves that file
once and then uses only the generation-specific URL, so a later upload cannot
change dependencies midway through a build.

**Generation response caching** means that only HTTP 200 (complete content),
206 (partial content), and 304 (not modified) under `/generations/` receive
the year-long `immutable` cache policy. Every other generation response uses
`no-store`: a missing generation's 404 is not an immutable artifact and may
become available after publication. The server-level `no-store` fallback also
covers hidden-file denial without weakening that denial or `nosniff`.
The mutable `/state.json` remains `no-store`; other ordinary paths retain
their `no-cache` policy. The status map belongs in the HTTP include context
used by the installer, outside the `server` block. It must be `volatile`:
an unsatisfiable byte range can first pass the header filter as 200, then
re-enter it as 416. Caching the map result would append the initial immutable
value again instead of adding `no-store` for the error.

**Late range-error limitation:** an isolated Nginx 1.31.8 test found that even
with `volatile`, a 416 response can retain the first immutable Cache-Control
field alongside the second `no-store` field. The latter prohibits storage,
but this is not a single-field/no-immutable-on-error result. A named 416 error
page did not remove the first field either. Do not claim that stronger
acceptance criterion has passed, or deploy this change on that assumption.
Resolve and re-test header cleanup against the deployed Nginx before merge
and deployment; do not disable valid range responses to hide this failure.

The Python regression tests check this configuration contract, not a running
Nginx instance. Before deploying, run `nginx -t` and verify actual 200, range
206, conditional 304, redirect, hidden-file 403, missing 404 and unsupported
method and unsatisfiable-range 416 responses in an isolated server. Inspect
every Cache-Control field, not a dictionary that hides duplicates. In
particular, a missing generation
must return `no-store`, then serve newly created content with `immutable`.
This policy does not repair a missing generation or invalidate an error
already stored by an intermediary; publisher diagnostics and public RPM/SRPM
checksum verification remain separate acceptance gates.

Directive semantics: [Nginx status maps](https://nginx.org/en/docs/http/ngx_http_map_module.html)
and [response headers](https://nginx.org/en/docs/http/ngx_http_headers_module.html).

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
