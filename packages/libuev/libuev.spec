# SPDX-License-Identifier: Apache-2.0
Name:           libuev
Version:        2.4.1
Release:        1%{?dist}
Summary:        Small Linux event loop library
License:        MIT
URL:            https://github.com/troglobit/libuev
Source0:        libuev-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf

%description
libuEv is a small event loop library for Linux built on epoll, timerfd,
signalfd, and eventfd.

%package devel
Summary:        Development files for libuEv
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared library link for
developing applications with libuEv.

%prep
%autosetup -p1

%build
%set_build_flags
%configure --disable-static --disable-doxygen-doc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libuev.la
rm -f %{buildroot}%{_docdir}/libuev/LICENSE

%check
# Run all seven maintained event-loop and API tests.
%make_build check

%files
%license LICENSE
%doc AUTHORS ChangeLog.md README.md
%{_libdir}/libuev.so.3*

%files devel
%license LICENSE
%{_includedir}/uev/
%{_libdir}/libuev.so
%{_libdir}/pkgconfig/libuev.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package with all seven upstream event-loop tests.
