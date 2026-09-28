# libslz 1.3.1

The frozen inventory's exact `libslz` key maps to Willy Tarreau's
[official GitHub repository](https://github.com/wtarreau/libslz). The latest
upstream tag `v1.3.1` resolves to immutable commit
`046706451ccc90908fd63dd2509ece96f1c18e94`; the release README names
version 1.3.1. Its HTTPS commit archive is pinned at SHA-256
`db0f0d9a26333534d3891663d40bab3b90cdc2b7dcf56122a60f1675f440cc78`.
All 26 archive entries were inspected: there are no absolute paths, parent
traversal, links, or device entries. Source files and the license are MIT.

Upstream does not register a `check` or `test` target. It ships three input
fixtures and its compressor/decompressor tools. Rather than mislabel those as
an upstream test suite, `%check` runs a downstream 180-case matrix: three
fixtures, ten compression levels, three formats (gzip, zlib and raw Deflate),
and direct/buffered input. Each stream must round-trip through SLZ's decoder
and independently decode through Python's zlib implementation. Installed
smoke compiles a public-API client and round-trips via the installed tools.

Upstream's `install-tools` target accidentally copies `zdecode` into the
`zdec` path and strips `zenc` before RPM debug extraction. The SPEC installs
the same three built tools directly, preserving their distinct behavior and
debug data. Both shared and static libraries are packaged.

Target: openEuler 24.03 LTS SP3, `riscv64`, RVA23. CI may retrieve only the
SHA-256-pinned source over HTTPS. A successful PR build would show target
build and test evidence, not public RPM/SRPM publication; repository URLs need
a separate verified publication result.
