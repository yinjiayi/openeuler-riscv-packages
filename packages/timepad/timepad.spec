# SPDX-License-Identifier: Apache-2.0
Name:           timepad
Version:        0.1.0
Release:        3%{?dist}
Summary:        A minimal Timer App for Linux that has a picture-in-picture mode
License:        MIT
URL:            https://github.com/agokule/timepad
Source0:        timepad-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libX11-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXtst-devel
BuildRequires:  make

%description
A minimal Timer App for Linux that has a picture-in-picture mode

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DBUILD_TESTING=ON \
  -DDISTRIBUTION_MODE=ON \
  -DSDL_DEPS_SHARED=OFF \
  -DSDL_INSTALL=OFF \
  -DSDL_SHARED=OFF \
  -DSDL_STATIC=ON \
  -DSDL_TEST_LIBRARY=OFF \
  -DSDL_TESTS=OFF
%cmake_build

%install
install -Dpm0755 %{_vpath_builddir}/Timepad %{buildroot}%{_bindir}/Timepad
install -Dpm0644 Timepad.desktop %{buildroot}%{_datadir}/applications/timepad.desktop
sed -i \
  -e 's|^Exec=.*|Exec=Timepad|' \
  -e 's|^Icon=.*|Icon=timepad|' \
  %{buildroot}%{_datadir}/applications/timepad.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/timepad.desktop
install -Dpm0644 assets/icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/timepad.png
install -d %{buildroot}%{_datadir}/timepad
cp -a assets/fonts assets/sound %{buildroot}%{_datadir}/timepad/
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure
test -x %{_vpath_builddir}/Timepad

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-3
- Allow the complete SDL and Timepad build to finish under QEMU.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-2
- Enable the complete SDL X11 backend and install the application resources.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
