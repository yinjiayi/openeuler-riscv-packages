# Libterminput

Official libterminput 1.1.2 parses common terminal input sequences without
terminfo. Its complete ISC copyright and permission notice is retained in the
source archive and every explicit binary subpackage.

Upstream `make all` remains unchanged, including compilation of the interactive
demo. The original `make check` executes the complete unfiltered `test.c`.
That default driver uses ordinary pipes and blocking/nonblocking reads to test
key/modifier sequences, mouse protocols, Unicode boundaries, bracketed paste,
input/state serialization and error/EOF cases. Its five-second alarm guards
remain intact. The interactive demo is not a default test and is not executed;
this does not claim physical terminal compatibility or native timing coverage.

The tests subpackage retains the whole checksum-bound upstream archive.
Staged and ordinarily installed shared/static replays compile the unchanged
original driver and compare the installed public header byte-for-byte. Four
internal manual-page symlinks are retained; their archive targets were checked
to stay inside the same upstream tree. Only staged `/usr/lib` is relocated to
openEuler's `/usr/lib64`. No source patch or disabled feature is introduced.

Repository validation is not target acceptance. No local source, RPM or QEMU
build is run; exact-head target CI, normal installation and physical RPM/SRPM
verification remain mandatory before merging.
