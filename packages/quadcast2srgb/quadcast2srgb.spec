# SPDX-License-Identifier: Apache-2.0
Name:           quadcast2srgb
Version:        0.4.0
Release:        1%{?dist}
Summary:        Customizable RGB LED controller for HyperX Quadcast 2S
License:        MIT
URL:            https://github.com/MuffinMario/quadcast2Srgb
Source0:        quadcast2srgb-0.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Customizable RGB LED controller for HyperX Quadcast 2S

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
