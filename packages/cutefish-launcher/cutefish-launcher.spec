# SPDX-License-Identifier: Apache-2.0
Name:           cutefish-launcher
Version:        0.8
Release:        1%{?dist}
Summary:        CutefishOS's full-screen application launcher
License:        GPL-3.0-or-later
URL:            https://github.com/cutefishos/launcher
Source0:        cutefish-launcher-0.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
CutefishOS's full-screen application launcher

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8-1
- Initial openEuler RISC-V package from the full package inventory.
