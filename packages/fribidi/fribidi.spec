# SPDX-License-Identifier: Apache-2.0
Name:           fribidi
Version:        1.0.16
Release:        1%{?dist}
Summary:        Unicode Bidirectional Algorithm implementation
License:        LGPL-2.1-or-later AND Unicode-DFS-2016
URL:            https://github.com/fribidi/fribidi
Source0:        fribidi-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  python3

%description
FriBidi is a free implementation of the Unicode Bidirectional Algorithm for
displaying logical-order text containing right-to-left scripts.

%package devel
Summary:        Development files for FriBidi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for FriBidi.

%package help
Summary:        Documentation for FriBidi
BuildArch:      noarch

%description help
API manual pages and upstream release documentation for FriBidi.

%prep
%autosetup -p1

%build
%meson \
  -Dbin=true \
  -Ddeprecated=true \
  -Ddocs=true \
  -Dtests=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%{_bindir}/fribidi
%{_libdir}/libfribidi.so.0*

%files devel
%license COPYING
%{_includedir}/fribidi/
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/fribidi.pc

%files help
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md TODO
%{_mandir}/man3/fribidi_*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.16-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
