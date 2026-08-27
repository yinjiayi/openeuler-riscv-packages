# SPDX-License-Identifier: Apache-2.0
Name:           argh
Version:        1.3.2
Release:        1%{?dist}
Summary:        Argh! A minimalist argument handler.
License:        BSD-3-Clause
URL:            https://github.com/adishavit/argh
Source0:        argh-1.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Argh! A minimalist argument handler.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
