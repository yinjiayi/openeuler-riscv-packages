# SPDX-License-Identifier: Apache-2.0
Name:           miniterm
Version:        1.7.0
Release:        1%{?dist}
Summary:        Lightweight VTE terminal emulator with colorscheme support (fork of tinyterm)
License:        MIT
URL:            https://github.com/laelath/miniterm
Source0:        miniterm-1.7.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Lightweight VTE terminal emulator with colorscheme support (fork of tinyterm)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
