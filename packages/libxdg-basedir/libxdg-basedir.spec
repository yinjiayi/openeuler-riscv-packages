# SPDX-License-Identifier: Apache-2.0
Name:           libxdg-basedir
Version:        1.2.3
Release:        1%{?dist}
Summary:        Implementation of the XDG Base Directory specification
License:        MIT
URL:            https://github.com/devnev/libxdg-basedir
Source0:        libxdg-basedir-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
libxdg-basedir provides functions for discovering and using paths defined by
the freedesktop.org XDG Base Directory specification.

%package devel
Summary:        Development files for libxdg-basedir
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with libxdg-basedir.

%prep
%autosetup -n libxdg-basedir-b978568d1b3ee04e8197f23ca4e3abdd372f85e1 -p1

%build
autoreconf -fi
%configure --disable-static --disable-doxygen-doc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libxdg-basedir.la

%check
# Run the complete 31-case maintained cache and XDG-directory query suite.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libxdg-basedir.so.1*

%files devel
%license COPYING
%{_includedir}/basedir.h
%{_includedir}/basedir_fs.h
%{_libdir}/libxdg-basedir.so
%{_libdir}/pkgconfig/libxdg-basedir.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.3-1
- Initial openEuler RISC-V package with all 31 upstream tests.
