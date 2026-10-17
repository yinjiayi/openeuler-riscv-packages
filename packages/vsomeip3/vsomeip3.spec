# SPDX-License-Identifier: Apache-2.0
Name:           vsomeip3
Version:        3.5.11
Release:        1%{?dist}
Summary:        COVESA implementation of SOME/IP protocol
License:        MPL-2.0
URL:            https://github.com/COVESA/vsomeip
Source0:        vsomeip3-3.5.11.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  boost-devel
BuildRequires:  systemd-devel

%description
COVESA implementation of SOME/IP protocol

%prep
%autosetup -n vsomeip-%{version} -p1

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
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.11-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Add the Boost and systemd development files required by CMake.
