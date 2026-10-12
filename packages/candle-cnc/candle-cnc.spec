# SPDX-License-Identifier: Apache-2.0
Name:           candle-cnc
Version:        11.2
Release:        1%{?dist}
Summary:        GRBL controller application with G-Code visualizer written in Qt
License:        GPL-3.0-or-later
URL:            https://github.com/Denvi/Candle
Source0:        candle-cnc-11.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GRBL controller application with G-Code visualizer written in Qt

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


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 11.2-1
- Initial openEuler RISC-V package from the full package inventory.
