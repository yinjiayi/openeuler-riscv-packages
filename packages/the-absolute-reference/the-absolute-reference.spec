# SPDX-License-Identifier: Apache-2.0
Name:           the-absolute-reference
Version:        0.5.7
Release:        1%{?dist}
Summary:        Reverse engineered implementation of Tetris the Absolute: The Grand Master 2 Plus
License:        MIT
URL:            https://github.com/burbruee/the-absolute-reference
Source0:        the-absolute-reference-0.5.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Reverse engineered implementation of Tetris the Absolute: The Grand Master 2 Plus

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license License.txt


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.7-1
- Initial openEuler RISC-V package from the full package inventory.
