# SPDX-License-Identifier: Apache-2.0
Name:           descent3
Version:        1.5.0
Release:        2%{?dist}
Summary:        Descent 3 by Outrage Entertainment
License:        GPL-3.0-or-later
URL:            https://github.com/DescentDevelopers/Descent3
Source0:        descent3-1.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  SDL2-devel
BuildRequires:  gtest-devel
BuildRequires:  zlib-devel

%description
Descent 3 by Outrage Entertainment

%prep
%autosetup -n Descent3-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '"/%%P"\n' \
  | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-2
- Quote installed paths so RPM file manifests preserve embedded spaces.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Add the SDL 2, GoogleTest, and zlib development files required by CMake.
