# SPDX-License-Identifier: Apache-2.0
Name:           qemuconf
Version:        0.2.1
Release:        1%{?dist}
Summary:        Utility to use qemu configuration files for VM
License:        MIT
URL:            https://github.com/Gottox/qemuconf
Source0:        qemuconf-0.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Utility to use qemu configuration files for VM

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
