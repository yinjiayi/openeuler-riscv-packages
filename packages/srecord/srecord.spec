# SPDX-License-Identifier: Apache-2.0
Name:           srecord
Version:        1.65.0
Release:        1%{?dist}
Summary:        Manipulate EPROM load files
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
URL:            https://srecord.sourceforge.net/
Source0:        srecord-%{version}-Source.tar.gz

BuildRequires:  bash
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  doxygen
BuildRequires:  gawk
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ghostscript
BuildRequires:  graphviz
BuildRequires:  grep
BuildRequires:  groff
BuildRequires:  libgcrypt-devel
BuildRequires:  make
BuildRequires:  netpbm
BuildRequires:  psutils
BuildRequires:  sed
BuildRequires:  which

%description
SRecord is a collection of tools for manipulating EPROM load files. It reads,
writes, converts, compares, and summarizes formats including Motorola
S-Record, Intel HEX, Tektronix, and binary images.

%package devel
Summary:        Development files for SRecord
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libgcrypt-devel%{?_isa}

%description devel
Headers and the static library for developing applications with SRecord.

%prep
%autosetup -n srecord-%{version}-Source -p1

%build
%cmake_conf
%cmake_build

%install
%cmake_install
mv %{buildroot}%{_libdir}/liblib_srecord.a \
  %{buildroot}%{_libdir}/libsrecord.a
# Upstream's cross-platform install macro copies every runtime dependency on
# Linux as well as Windows. System libraries must remain owned by their RPMs.
find %{buildroot}%{_libdir} -mindepth 1 -maxdepth 1 \
  ! -name libsrecord.a -delete
rm -rf %{buildroot}%{_docdir}/%{name}/htdocs

%check
%ctest -- -j1

%files
%license LICENSE
%doc AUTHORS README.md RELEASE
%{_bindir}/srec_cat
%{_bindir}/srec_cmp
%{_bindir}/srec_info
%{_docdir}/%{name}/*.pdf
%{_mandir}/man1/srec_*.1*
%{_mandir}/man5/srec_*.5*

%files devel
%license LICENSE
%{_includedir}/srecord/
%{_libdir}/libsrecord.a
%{_mandir}/man3/srecord*.3*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.65.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
