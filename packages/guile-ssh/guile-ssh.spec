# SPDX-License-Identifier: Apache-2.0
Name:           guile-ssh
Version:        0.18.0
Release:        1%{?dist}
Summary:        SSH module for Guile based on libssh
License:        GPL-3.0-or-later
URL:            https://github.com/artyom-poptsov/guile-ssh
Source0:        guile-ssh-0.18.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
SSH module for Guile based on libssh

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18.0-1
- Initial openEuler RISC-V package from the full package inventory.
