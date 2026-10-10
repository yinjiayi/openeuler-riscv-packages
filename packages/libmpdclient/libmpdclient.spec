# SPDX-License-Identifier: Apache-2.0
Name:           libmpdclient
Version:        2.26
Release:        1%{?dist}
Summary:        C client library for the Music Player Daemon protocol
License:        BSD-2-Clause AND BSD-3-Clause
URL:            https://musicpd.org/libs/libmpdclient/
Source0:        libmpdclient-%{version}.tar.xz

BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf

%description
libmpdclient provides a stable C API for communicating with Music Player
Daemon servers.

%package devel
Summary:        Headers and pkg-config metadata for libmpdclient
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public headers, the unversioned library link, and pkg-config metadata for
applications using the Music Player Daemon client protocol.

%prep
%autosetup -p1

%build
%meson -Dtest=true -Ddocumentation=false
%meson_build

%install
%meson_install
# Meson also installs source documentation; RPM owns canonical %doc and %license.
rm -rf %{buildroot}%{_docdir}/%{name}

%check
# Run both registered upstream Check-based Meson tests.
%meson_test

%files
%license LICENSES/BSD-2-Clause.txt LICENSES/BSD-3-Clause.txt
%doc AUTHORS NEWS README.rst
%{_libdir}/libmpdclient.so.2*

%files devel
%license LICENSES/BSD-2-Clause.txt LICENSES/BSD-3-Clause.txt
%{_includedir}/mpd/
%{_libdir}/libmpdclient.so
%{_libdir}/pkgconfig/libmpdclient.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.26-1
- Initial package from the official 2.26 archive with both upstream tests.
