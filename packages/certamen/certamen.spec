# SPDX-License-Identifier: Apache-2.0
Name:           certamen
Version:        1.0.3
Release:        1%{?dist}
Summary:        TUI quiz game engine with SSH multiplayer support written in CPP with FTXUI
License:        MIT
URL:            https://github.com/trintlermint/certamen
Source0:        certamen-1.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libssh-devel
BuildRequires:  make
BuildRequires:  yaml-cpp-devel

%description
TUI quiz game engine with SSH multiplayer support written in CPP with FTXUI

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
