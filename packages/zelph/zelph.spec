# SPDX-License-Identifier: Apache-2.0
Name:           zelph
Version:        0.9.9
Release:        1%{?dist}
Summary:        A sophisticated semantic network system capable of encoding inference rules within the network itself. Built for powerful logical reasoning, it can process
License:        AGPL-3.0
URL:            https://github.com/acrion/zelph
Source0:        zelph-0.9.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A sophisticated semantic network system capable of encoding inference rules within the network itself. Built for powerful logical reasoning, it can process

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.9-1
- Initial openEuler RISC-V package from the full package inventory.
