# SPDX-License-Identifier: Apache-2.0
Name:           slowhttptest
Version:        1.9.0
Release:        1%{?dist}
Summary:        Highly configurable tool that simulates some Application Layer Denial of Service (DoS) attacks
License:        Apache-2.0
URL:            https://github.com/shekyan/slowhttptest
Source0:        slowhttptest-1.9.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Highly configurable tool that simulates some Application Layer Denial of Service (DoS) attacks

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
