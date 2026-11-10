<!-- SPDX-License-Identifier: Apache-2.0 -->
# File::Tee

This directory packages upstream `https://metacpan.org/dist/File-Tee` version `0.07` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed upstream 0.07 archive matches authorized MetaCPAN metadata, signed
PAUSE CHECKSUMS and the byte-identical Debian source archive. The original
README and module grant redistribution under the same terms as Perl; both
complete Perl license texts are included in the RPM. No distribution recipe or
patch is imported.

The package runs upstream's unchanged default tests. The functional suite has
50 assertions covering fork/signal handling and replicated bytes; the POD test
retains upstream's author-only self-skip. The installed smoke uses a private
directory and an explicit literal target path; it does not execute a shell
command or depend on sleep timing. Upstream's documented stream and pipe
options are unchanged. The application must not pass untrusted input as a tee
target specification.
