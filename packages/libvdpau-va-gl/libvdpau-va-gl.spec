# SPDX-License-Identifier: Apache-2.0
Name:           libvdpau-va-gl
Version:        0.4.2
Release:        1%{?dist}
Summary:        VDPAU driver with OpenGL/VAAPI backend
License:        MIT
URL:            https://github.com/i-rinat/libvdpau-va-gl
Source0:        libvdpau-va-gl-0.4.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
VDPAU driver with OpenGL/VAAPI backend

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.2-1
- Initial openEuler RISC-V package from the full package inventory.
