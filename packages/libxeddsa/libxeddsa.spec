# SPDX-License-Identifier: Apache-2.0
Name:           libxeddsa
Version:        2.0.1
Release:        1%{?dist}
Summary:        A toolkit around Curve25519 and Ed25519 key pairs, with a focus on conversion between the two.
License:        MIT
URL:            https://github.com/Syndace/libxeddsa
Source0:        libxeddsa-2.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A toolkit around Curve25519 and Ed25519 key pairs, with a focus on conversion between the two.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
