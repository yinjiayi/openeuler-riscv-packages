# SPDX-License-Identifier: Apache-2.0
Name:           libdatrie
Version:        0.2.14
Release:        1%{?dist}
Summary:        Double-array trie library
License:        LGPL-2.1-or-later
URL:            https://github.com/tlwg/libdatrie
Source0:        libdatrie-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
libdatrie implements a compact and efficient double-array trie data structure.

%package devel
Summary:        Development files for libdatrie
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for applications using libdatrie.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/trietool*
%{_libdir}/libdatrie.so.1*
%{_mandir}/man1/trietool*.1*

%files devel
%{_includedir}/datrie/
%{_libdir}/libdatrie.so
%{_libdir}/pkgconfig/datrie-0.2.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.14-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
