# SPDX-License-Identifier: Apache-2.0
Name:           ermis
Version:        1.1.3
Release:        1%{?dist}
Summary:        Image, audio, text, PDF, distributed and network steganography suite.
License:        GPL-3.0-or-later
URL:            https://github.com/alamahant/Ermis
Source0:        ermis-1.1.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Image, audio, text, PDF, distributed and network steganography suite.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
