# SPDX-License-Identifier: Apache-2.0
Name:           xde-session
Version:        1.14
Release:        1%{?dist}
Summary:        X Desktop Environment Display and Session Management
License:        GPL-3.0-or-later
URL:            https://github.com/bbidulock/xde-session
Source0:        xde-session-1.14.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
X Desktop Environment Display and Session Management

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-1
- Initial openEuler RISC-V package from the full package inventory.
