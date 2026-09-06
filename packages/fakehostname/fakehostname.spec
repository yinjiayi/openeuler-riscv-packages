# SPDX-License-Identifier: Apache-2.0
Name:           fakehostname
Version:        0.3.2
Release:        1%{?dist}
Summary:        Run a command and fake your hostname.
License:        MIT
URL:            https://github.com/dtcooper/fakehostname
Source0:        fakehostname-0.3.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Run a command and fake your hostname.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
