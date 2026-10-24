# SPDX-License-Identifier: Apache-2.0
Name:           csvprintf
Version:        1.3.4
Release:        1%{?dist}
Summary:        Simple CSV file parser for the UNIX command line
License:        Apache-2.0
URL:            https://github.com/archiecobbs/csvprintf
Source0:        csvprintf-1.3.4-edbe73d.tar.gz

BuildRequires:  autoconf >= 2.69
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  libxslt
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  util-linux

# coreutils supplies the external printf configured into the executable.
# libxslt supplies xsltproc for the default installed xml2csv command.
# The remaining tools replay the complete upstream installed test payload.
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       findutils
Requires:       grep
Requires:       libxslt
Requires:       sed
Requires:       util-linux

%description
csvprintf parses CSV input into printf-formatted records, XML, JSON text
sequences, or Bash assignments. The xml2csv companion performs the original
XSLT-based conversion from its XML representation back to CSV.

%prep
%autosetup -n archiecobbs-csvprintf-edbe73d -p1

%build
# The immutable Git archive lacks generated Autotools files and gitrev.c.
# Bootstrap first because upstream cleanup deliberately removes gitrev.c.
bash ./autogen.sh
# At the exact annotated tag 1.3.4, upstream git describe yields 1.3.4.
# Materialize that generated release object without consulting any .git tree.
printf 'const char *const csvprintf_version = "1.3.4";\n' > gitrev.c
%configure
%make_build

%install
%make_install
# Keep all upstream default binaries, both man aliases, XSL and default docs.
# Preserve the entire original test set for installed-RPM verification.
install -d %{buildroot}%{_libexecdir}/csvprintf/upstream-tests
cp -pr tests %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/tests
install -m 0644 csv.xsl %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/csv.xsl
find %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/tests -type d -exec chmod 0755 {} +
find %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/tests -type f -exec chmod 0644 {} +
chmod 0755 %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/tests/run.sh \
    %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/tests/run2.sh
test "$(find tests -type f | wc -l)" -eq 85
# Bind the original bytes, not only the staged copies. No fixture rewriting.
(find tests -type f -print0; printf 'csv.xsl\0') | LC_ALL=C sort -z | \
    xargs -0 sha256sum > %{buildroot}%{_libexecdir}/csvprintf/upstream-tests/SHA256SUMS
(cd %{buildroot}%{_libexecdir}/csvprintf/upstream-tests && sha256sum -c SHA256SUMS)

%check
export LC_ALL=C
# Fail closed rather than silently replacing the original make tests target.
# run.sh's unmodified /bin/sh shebang needs pipefail on the target shell.
/bin/sh -c 'set -o pipefail'
test "$(find tests -type f | wc -l)" -eq 85
%make_build tests
./csvprintf -v > version.stdout 2> version.stderr
test ! -s version.stdout
grep -Fx 'csvprintf version 1.3.4 (1.3.4)' version.stderr

%files
%license COPYING
%{_bindir}/csvprintf
%{_bindir}/xml2csv
%{_mandir}/man1/csvprintf.1*
%{_mandir}/man1/xml2csv.1*
%dir %{_datadir}/csvprintf
%{_datadir}/csvprintf/csv.xsl
%dir %{_datadir}/doc/packages/csvprintf
%doc %{_datadir}/doc/packages/csvprintf/CHANGES
%doc %{_datadir}/doc/packages/csvprintf/COPYING
%doc %{_datadir}/doc/packages/csvprintf/README
%{_libexecdir}/csvprintf

%changelog
* Fri Oct 23 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.4-1
- Package fixed official release with deterministic release-version object.
- Preserve upstream defaults, original full tests, and installed test replay.
