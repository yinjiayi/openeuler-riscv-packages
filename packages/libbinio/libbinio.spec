# SPDX-License-Identifier: Apache-2.0
Name:           libbinio
Version:        1.5
Release:        1%{?dist}
Summary:        Platform-independent C++ binary stream input and output library
License:        LGPL-2.1-or-later AND LicenseRef-Ken-Turkowski AND GFDL-1.1-or-later
URL:            https://github.com/adplug/libbinio
Source0:        libbinio-1.5.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  texinfo
BuildRequires:  gettext
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
%description
Binary I/O stream classes for portable integer, floating-point, memory,
file and standard C++ iostream access. Original default feature selection,
shared and static libraries, and Texinfo documentation are retained.

%package devel
Summary:        Development headers and static library for libbinio
Requires:       %{name} = %{version}-%{release}
Requires:       gcc-c++
Requires:       pkgconf

%description devel
Original public headers, pkg-config metadata and static library. The
packaging-owned verification source exercises the installed shared library;
these are downstream checks, not an upstream unit-test suite.

%prep
%autosetup -n libbinio-020a4c2b7612863600428e0e9f2491b923e54ac2 -p1
# Preserve the complete original permission and warranty notice verbatim.
sed -n '451,470p' src/binio.cpp > COPYING-KEN-TURKOWSKI
cat > verify-binio.cpp <<'CPP'
// SPDX-License-Identifier: Apache-2.0
// Packaging-owned semantic checks; never presented as upstream tests.
#include <binio.h>
#include <binstr.h>
#include <binfile.h>
#include <binwrap.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <string>
static unsigned checks = 0;
static void check(bool ok, const char *name) {
  ++checks;
  if (!ok) { std::fprintf(stderr, "FAIL: %%s\n", name); std::exit(1); }
  std::printf("PASS: %%s\n", name);
}
int main() {
  check(BINIO_ENABLE_STRING == 1, "default-string-feature");
  check(BINIO_ENABLE_IOSTREAM == 1, "default-iostream-feature");
  check(BINIO_ISO_STDLIB == 1, "default-iso-stdlib");
  check(BINIO_WITH_MATH == 1, "default-math-feature");
  unsigned char bytes[32] = {};
  binsstream memory(bytes, sizeof bytes);
  memory.setFlag(binio::BigEndian, false);
  memory.writeInt(0x12345678, 4);
  check(memory.pos() == 4, "integer-write-position");
  check(bytes[0] == 0x78 && bytes[1] == 0x56 && bytes[2] == 0x34 && bytes[3] == 0x12, "little-endian-bytes");
  memory.seek(0);
  check(memory.readInt(4) == 0x12345678, "little-endian-roundtrip");
  memory.seek(0);
  check(memory.peekInt(4) == 0x12345678, "integer-peek");
  check(memory.pos() == 0, "peek-keeps-position");
  memory.setFlag(binio::BigEndian);
  check(memory.getFlag(binio::BigEndian), "big-endian-flag");
  memory.writeInt(0x12345678, 4);
  check(bytes[0] == 0x12 && bytes[1] == 0x34 && bytes[2] == 0x56 && bytes[3] == 0x78, "big-endian-bytes");
  memory.seek(0);
  check(memory.readInt(4) == 0x12345678, "big-endian-roundtrip");
  memory.seek(0); memory.setFlag(binio::BigEndian, false); memory.setFlag(binio::FloatIEEE);
  memory.writeFloat(1.0, binio::Single);
  check(bytes[0] == 0 && bytes[1] == 0 && bytes[2] == 0x80 && bytes[3] == 0x3f, "ieee-single-bytes");
  memory.seek(0);
  check(memory.readFloat(binio::Single) == 1.0, "ieee-single-roundtrip");
  check(memory.error() == binio::NoError, "memory-no-error");
  memory.seek(0);
  check(memory.writeString(std::string("abc|")) == 4, "std-string-write-size");
  memory.seek(0);
  check(memory.readString('|') == "abc", "std-string-delimited-read");
  memory.seek(0); char text[5] = {};
  check(memory.readString(text, 4, '|') == 3, "c-string-delimited-size");
  check(std::strcmp(text, "abc") == 0, "c-string-delimited-value");
  binisstream bounded(bytes, 4); bounded.seek(4);
  check(bounded.pos() == 4 && !bounded.eof(), "exact-end-position");
  bounded.readInt(1);
  check(bounded.eof() && bounded.pos() == 4, "bounded-read-no-overrun");
  check(bounded.error() == binio::Eof, "eof-error-code");
  check(!bounded.eof() && bounded.error() == binio::NoError, "error-read-clears-state");
  bounded.seek(8);
  check(bounded.pos() == 4 && bounded.error() == binio::Eof, "seek-beyond-logical-bound");
  std::ostringstream out; binowstream writer(&out); writer.setFlag(binio::BigEndian);
  writer.writeInt(0x3456, 2);
  check(out.str().size() == 2 && static_cast<unsigned char>(out.str()[0]) == 0x34 && static_cast<unsigned char>(out.str()[1]) == 0x56, "ostream-wire-bytes");
  std::istringstream in(out.str()); biniwstream reader(&in); reader.setFlag(binio::BigEndian);
  check(reader.readInt(2) == 0x3456, "istream-wrapper-read");
  check(reader.error() == binio::NoError && writer.error() == binio::NoError, "iostream-no-error");
  { binofstream file(std::string("binio-fixture.dat")); file.setFlag(binio::BigEndian); file.writeInt(0x10203040, 4); file.close();
    check(file.error() == binio::NoError, "file-write-close"); }
  { binifstream file(std::string("binio-fixture.dat")); file.setFlag(binio::BigEndian);
    check(file.readInt(4) == 0x10203040, "file-read-roundtrip");
    check(file.ateof() && file.pos() == 4, "file-peek-eof-position");
    check(file.error() == binio::NoError, "file-peek-keeps-error-state"); }
  check(std::remove("binio-fixture.dat") == 0, "fixture-removal");
  binifstream missing("binio-file-must-not-exist.dat");
  check(missing.error() == binio::NotFound, "missing-file-error");
  memory.seek(0);
  check(memory.readInt(64) == 0, "unsupported-size-value");
  check(memory.error() == binio::Unsupported, "unsupported-size-error");
  std::printf("{\"suite\":\"downstream-binio-semantics\",\"checks\":%%u,\"skips\":0,\"status\":\"passed\"}\n", checks);
  return 0;
}
CPP

%build
# Bootstrap the fixed official Git release; execute only in target CI.
autoreconf --force --install
%configure --enable-maintainer-mode
%make_build

%install
%make_install
# libtool's .la and the generated global Info directory index are not payloads.
rm -f %{buildroot}%{_libdir}/libbinio.la %{buildroot}%{_infodir}/dir
install -Dm644 verify-binio.cpp %{buildroot}%{_datadir}/libbinio/verify-binio.cpp

%check
# Original default target is preserved; upstream defines no TESTS.
make check
mkdir downstream-source downstream-staged
g++ %{optflags} -Isrc verify-binio.cpp -Lsrc/.libs -lbinio -lm -o downstream-source/verify
(cd downstream-source && env LD_LIBRARY_PATH="$OLDPWD/src/.libs" ./verify)
g++ %{optflags} -I%{buildroot}%{_includedir}/binio verify-binio.cpp -L%{buildroot}%{_libdir} -lbinio -lm -o downstream-staged/verify
(cd downstream-staged && env LD_LIBRARY_PATH="%{buildroot}%{_libdir}" ./verify)

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING AUTHORS COPYING-KEN-TURKOWSKI doc/fdl.texi
%doc README NEWS doc/libbinio.texi doc/fdl.texi doc/version.texi
%{_libdir}/libbinio.so.1*
%{_infodir}/libbinio.info*

%files devel
%{_includedir}/binio/
%{_libdir}/libbinio.so
%{_libdir}/libbinio.a
%{_libdir}/pkgconfig/libbinio.pc
%{_datadir}/libbinio/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Preserve original defaults, documentation and literal borrowed notices.
- Add separately labeled source, staged and RPM-installed semantic checks.
