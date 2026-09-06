# SPDX-License-Identifier: Apache-2.0
Name:           freewheeling
Version:        0.6.6
Release:        1%{?dist}
Summary:        A live looper
License:        GPL-2.0-or-later
URL:            https://github.com/free-wheeling/freewheeling
Source0:        freewheeling-0.6.6.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A live looper

%prep
%autosetup -p1

%build
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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.6-1
- Initial openEuler RISC-V package from the full package inventory.
