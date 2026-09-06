# SPDX-License-Identifier: Apache-2.0
Name:           neovim-qt
Version:        0.2.19
Release:        1%{?dist}
Summary:        GUI for Neovim
License:        ISC
URL:            https://github.com/equalsraf/neovim-qt
Source0:        neovim-qt-0.2.19.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GUI for Neovim

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.19-1
- Initial openEuler RISC-V package from the full package inventory.
