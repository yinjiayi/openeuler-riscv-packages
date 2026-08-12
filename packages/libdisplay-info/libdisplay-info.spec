# SPDX-License-Identifier: Apache-2.0

Name:           libdisplay-info
Version:        0.4.0
Release:        1%{?dist}
Summary:        EDID and DisplayID parsing library
License:        MIT
URL:            https://gitlab.freedesktop.org/emersion/libdisplay-info
Source0:        libdisplay-info-%{version}.tar.xz

BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  hwdata
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  patch
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3

%description
libdisplay-info provides a low-level and high-level C API for parsing and
querying EDID and DisplayID display metadata.

%package tools
Summary:        Command-line EDID decoder
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
The di-edid-decode utility decodes EDID blobs with libdisplay-info.

%package devel
Summary:        Development files for libdisplay-info
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, the unversioned shared-library link, and pkg-config metadata for
developing applications with libdisplay-info.

%prep
%autosetup -p1

%build
%meson --wrap-mode=nodownload
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/libdisplay-info.so.4*

%files tools
%license LICENSE
%{_bindir}/di-edid-decode

%files devel
%license LICENSE
%{_includedir}/libdisplay-info/
%{_libdir}/libdisplay-info.so
%{_libdir}/pkgconfig/libdisplay-info.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package with all 68 registered upstream tests.
