# SPDX-License-Identifier: Apache-2.0
Name:           sysinfoviewer
Version:        0.3.2
Release:        5%{?dist}
Summary:        A comprehensive system information viewer built with wxWidgets
License:        MIT
URL:            https://github.com/Magpiny/sysinfoviewer
Source0:        sysinfoviewer-0.3.2.tar.gz
Patch0:         0001-cmake-support-version-3.27.patch
Patch1:         0002-wxarraystring-compat.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 3.27
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  wxGTK3-devel

%description
A comprehensive system information viewer built with wxWidgets

%prep
%autosetup -p1

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

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-5
- Build with the wxArrayString API provided by the target wxWidgets 3.2.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-4
- Generate the CMake build tree where the build, install, and check macros expect it.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-3
- Allow the complete required GUI dependency closure enough time to download.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-2
- Support the CMake 3.27 version shipped by openEuler 24.03 LTS SP3.
- Add the development dependencies required by the upstream CMake project.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
