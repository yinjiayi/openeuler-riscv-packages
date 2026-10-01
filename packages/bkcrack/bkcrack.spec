# SPDX-License-Identifier: Apache-2.0
Name:           bkcrack
Version:        1.8.1
Release:        1%{?dist}
Summary:        Crack legacy zip encryption with Biham and Kocher's known plaintext attack.
License:        Zlib
URL:            https://github.com/kimci86/bkcrack
Source0:        bkcrack-1.8.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Crack legacy zip encryption with Biham and Kocher's known plaintext attack.

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
%license license.txt


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
