# SPDX-License-Identifier: Apache-2.0
Name:           systembus-notify
Version:        1.1
Release:        1%{?dist}
Summary:        System bus notification daemon
License:        MIT
URL:            https://github.com/rfjakob/systembus-notify
Source0:        systembus-notify-1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
System bus notification daemon

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package from the full package inventory.
