# SPDX-License-Identifier: Apache-2.0
Name:           bythos
Version:        0.1.0
Release:        1%{?dist}
Summary:        Secret knowledge of the machine
License:        MIT
URL:            https://github.com/q1sh101/bythos
Source0:        bythos-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Secret knowledge of the machine

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
