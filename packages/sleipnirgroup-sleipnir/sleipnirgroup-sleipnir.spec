# SPDX-License-Identifier: Apache-2.0
Name:           sleipnirgroup-sleipnir
Version:        0.6.4
Release:        1%{?dist}
Summary:        Reverse mode autodiff library, interior-point method, and NLP solver DSL
License:        BSD-3-Clause
URL:            https://github.com/SleipnirGroup/Sleipnir
Source0:        sleipnirgroup-sleipnir-0.6.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Reverse mode autodiff library, interior-point method, and NLP solver DSL

%prep
%autosetup -n Sleipnir-%{version} -p1

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Configure CMake in the build directory consumed by the RPM macros.
