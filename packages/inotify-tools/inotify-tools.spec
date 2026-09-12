# SPDX-License-Identifier: Apache-2.0
Name:           inotify-tools
Version:        4.25.9.0
Release:        1%{?dist}
Summary:        inotify-tools is a C library and a set of command-line programs for Linux providing a simple interface to inotify.
License:        GPL-2.0-or-later
URL:            https://github.com/inotify-tools/inotify-tools
Source0:        inotify-tools-4.25.9.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
inotify-tools is a C library and a set of command-line programs for Linux providing a simple interface to inotify.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.25.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
