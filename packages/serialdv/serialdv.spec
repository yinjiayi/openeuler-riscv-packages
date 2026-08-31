# SPDX-License-Identifier: Apache-2.0
Name:           serialdv
Version:        1.1.5
Release:        3%{?dist}
Summary:        C++ interface to encode/decode audio with AMBE3000 based devices in packet mode
License:        GPL-3.0-or-later
URL:            https://github.com/f4exb/serialDV
Source0:        serialdv-1.1.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ interface to encode/decode audio with AMBE3000 based devices in packet mode

%prep
%autosetup -n serialDV-%{version} -p1

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


%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.5-3
- Configure CMake in the build directory consumed by the RPM macros.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.5-2
- Use the exact case-sensitive serialDV archive root during source preparation.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.5-1
- Initial openEuler RISC-V package from the full package inventory.
