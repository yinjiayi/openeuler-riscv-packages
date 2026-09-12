# SPDX-License-Identifier: Apache-2.0
Name:           acreetionos-mediawriter
Version:        5.3.1
Release:        2%{?dist}
Summary:        AcreetionOS USB Flasher — Write AcreetionOS images to USB drives
License:        GPL-2.0-or-later
URL:            https://github.com/spivanatalie64/AcreetionMediaWriter
Source0:        acreetionos-mediawriter-5.3.1.tar.gz
Patch0:         patches/0001-cmake-target-stable-version-and-qt-6.5.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  xz-devel
Requires:       bash
Requires:       coreutils
Requires:       curl
Requires:       tar
Requires:       udisks2
Requires:       util-linux

%description
AcreetionOS USB Flasher — Write AcreetionOS images to USB drives

%prep
%autosetup -n AcreetionMediaWriter-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/org.acreetionos.MediaWriter.metainfo.xml

%files -f %{name}.files
%license LICENSE.GPL-2
%license LICENSE.LGPL-2
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.1-2
- Match the verified source root and declare the complete Linux build dependencies.
- Report the stable version and support the target Qt 6.5.2 release without disabling components.
- Validate the installed AppStream metadata.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
