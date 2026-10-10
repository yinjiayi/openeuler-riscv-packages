# SPDX-License-Identifier: Apache-2.0
Name:           ctemplate
Version:        2.4
Release:        1%{?dist}
Summary:        A library implementing a simple but powerful template language for C++
License:        BSD-3-Clause
URL:            https://github.com/olafvdspek/ctemplate
Source0:        ctemplate-2.4.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A library implementing a simple but powerful template language for C++

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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4-1
- Initial openEuler RISC-V package from the full package inventory.
