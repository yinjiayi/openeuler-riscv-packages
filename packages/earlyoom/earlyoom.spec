# SPDX-License-Identifier: Apache-2.0
Name:           earlyoom
Version:        1.9.0
Release:        1%{?dist}
Summary:        earlyoom - Early OOM Daemon for Linux
License:        MIT
URL:            https://github.com/rfjakob/earlyoom
Source0:        earlyoom-1.9.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
earlyoom - Early OOM Daemon for Linux

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
