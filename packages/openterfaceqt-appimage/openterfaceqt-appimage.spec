# SPDX-License-Identifier: Apache-2.0
Name:           openterfaceqt-appimage
Version:        0.5.25
Release:        1%{?dist}
Summary:        Openterface Mini-KVM Host Application (AppImage version)
License:        AGPL-3.0
URL:            https://github.com/TechxArtisanStudio/Openterface_QT
Source0:        openterfaceqt-appimage-0.5.25.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Openterface Mini-KVM Host Application (AppImage version)

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.25-1
- Initial openEuler RISC-V package from the full package inventory.
