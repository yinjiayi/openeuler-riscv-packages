# SPDX-License-Identifier: Apache-2.0
Name:           tfblib
Version:        0.1.1
Release:        1%{?dist}
Summary:        Low-level graphics library for drawing to the framebuffer
License:        BSD-2-Clause
URL:            https://github.com/vvaltchev/tfblib
Source0:        tfblib-0.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Low-level graphics library for drawing to the framebuffer

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
