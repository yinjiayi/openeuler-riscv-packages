<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-digest-md5-file

This directory packages upstream `https://metacpan.org/dist/Digest-MD5-File` version `0.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The upstream README and module POD give the same terms as Perl itself and retain
Daniel Muey's copyright. The original README is installed as license material.
The complete upstream `make test` runs unchanged; the installed smoke uses
only local scratch files. MD5 is a compatibility feature, not a security
recommendation.

`0001-open-literal-filenames.patch` is a local fix for 0.08. The existence
checks preceding the two-argument Perl `open` did not prevent mode or command
interpretation of a real filename. Three-argument read-only open preserves
literal paths and existing binmode handling. The installed smoke covers both
an ordinary file and a real filename ending in a pipe. This is not an
architecture-specific change; remove it only when the verified upstream source
opens caller paths literally and passes the same regression.
