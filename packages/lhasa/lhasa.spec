# SPDX-License-Identifier: Apache-2.0
Name:           lhasa
Version:        0.6.0
Release:        1%{?dist}
Summary:        Free LHA and LZH archive decompressor and library
License:        ISC
URL:            https://lhasa.soulsphere.org/
Source0:        lhasa-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
Lhasa is a free replacement for the Unix LHA tool. It extracts LZH/LHA and
LZS archives and provides liblhasa for applications that need the same
decompression support.

%package devel
Summary:        Development files for liblhasa
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with liblhasa.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/liblhasa.la

%check
# Run every compiled decoder test and every shipped archive/extraction corpus.
# Upstream deliberately clears CFLAGS for its unoptimized test objects. Keep
# the position-independent code property required by openEuler's PIE linker.
%make_build check CFLAGS="-fPIE"

%files
%license COPYING.md
%doc AUTHORS NEWS.md README.md SECURITY.md
%{_bindir}/lha
%{_libdir}/liblhasa.so.0*
%{_mandir}/man1/lha.1*

%files devel
%license COPYING.md
%{_includedir}/liblhasa-%{version}/
%{_libdir}/liblhasa.so
%{_libdir}/pkgconfig/liblhasa.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package with the complete archive regression suite.
- Compile the upstream test-only objects for openEuler's PIE link policy.
- Pass installed-smoke pkg-config flags as an explicit Bash array.
