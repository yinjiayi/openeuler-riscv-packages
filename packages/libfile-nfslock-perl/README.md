# File::NFSLock 1.29

The pinned upstream archive matches authorized MetaCPAN metadata, the verified PAUSE checksum entry, and the Debian orig archive byte-for-byte. The archive README and module carry the author grant for GNU GPL or the Perl Artistic License; Debian identifies GPL-1-or-later or Artistic for the same archive. The RPM installs the original README notice and both full Perl license texts.

The recipe runs the complete upstream default suite unchanged. On the host, 21 files and 214 assertions passed; tests exercise forks, signals, timeouts and local file-lock lifecycle. The staged smoke uses a private temporary file and verifies lock creation and release. Neither is a native NFS interoperability test or a RISC-V result. Actual RISC-V build, install and smoke remain CI-only.
