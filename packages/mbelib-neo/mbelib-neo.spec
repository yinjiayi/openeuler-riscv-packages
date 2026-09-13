# SPDX-License-Identifier: Apache-2.0
Name:           mbelib-neo
Version:        2.0.0
Release:        2%{?dist}
Summary:        P25 Phase 1 and ProVoice IMBE and Half-rate AMBE vocoder library (modernized fork)
License:        GPL-2.0-or-later
URL:            https://github.com/arancormonk/mbelib-neo
Source0:        mbelib-neo-2.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
P25 Phase 1 and ProVoice IMBE and Half-rate AMBE vocoder library (modernized fork)

%prep
%autosetup -p1

%build
%cmake_conf -DMBELIB_BUILD_TESTS=ON
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
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-2
- Configure the build in the openEuler CMake vpath directory.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
