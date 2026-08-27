# SPDX-License-Identifier: Apache-2.0
Name:           udp2raw-tunnel
Version:        20230206.0
Release:        1%{?dist}
Summary:        UDP over TCP/ICMP/UDP tunnel
License:        MIT
URL:            https://github.com/wangyu-/udp2raw-tunnel
Source0:        udp2raw-tunnel-20230206.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
UDP over TCP/ICMP/UDP tunnel

%prep
%autosetup -n udp2raw-%{version} -p1

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
%license LICENSE.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20230206.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Configure CMake in the build directory consumed by the RPM macros.
