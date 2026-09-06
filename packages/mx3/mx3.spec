# SPDX-License-Identifier: Apache-2.0
Name:           mx3
Version:        1.0.1
Release:        1%{?dist}
Summary:        Gesture remapping driver for Logitech MX Master 3 mice on Linux
License:        MIT
URL:            https://github.com/enBonnet/mx3-linux-driver
Source0:        mx3-1.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Gesture remapping driver for Logitech MX Master 3 mice on Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
