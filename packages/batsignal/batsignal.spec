# SPDX-License-Identifier: Apache-2.0
Name:           batsignal
Version:        1.8.0
Release:        1%{?dist}
Summary:        A lightweight battery monitor daemon
License:        ISC
URL:            https://github.com/electrickite/batsignal
Source0:        batsignal-1.8.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A lightweight battery monitor daemon

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
