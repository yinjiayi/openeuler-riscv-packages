# SPDX-License-Identifier: Apache-2.0
Name:           msr-safe
Version:        1.7.0
Release:        1%{?dist}
Summary:        Kernel module and utility to control MSR access
License:        GPL-2.0-or-later
URL:            https://github.com/LLNL/msr-safe
Source0:        msr-safe-1.7.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Kernel module and utility to control MSR access

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
