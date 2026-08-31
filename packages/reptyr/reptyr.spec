# SPDX-License-Identifier: Apache-2.0
Name:           reptyr
Version:        0.10.0
Release:        1%{?dist}
Summary:        Utility for taking an existing running program and attaching it to a new terminal
License:        MIT
URL:            https://github.com/nelhage/reptyr
Source0:        reptyr-0.10.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Utility for taking an existing running program and attaching it to a new terminal

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license COPYING
%doc README.md
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.0-1
- Initial openEuler RISC-V package from the full package inventory.
