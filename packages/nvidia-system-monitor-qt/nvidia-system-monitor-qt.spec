# SPDX-License-Identifier: Apache-2.0
Name:           nvidia-system-monitor-qt
Version:        1.6
Release:        2%{?dist}
Summary:        Task Manager for Linux for Nvidia graphics cards (QT vesrion)
License:        MIT
URL:            https://github.com/congard/nvidia-system-monitor-qt
Source0:        nvidia-system-monitor-qt-1.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt5-qtbase-devel

%description
Task Manager for Linux for Nvidia graphics cards (QT vesrion)

%prep
%autosetup -p1

%build
%cmake \
  -DBUILD_TESTING=ON \
  -DIconPath=%{_datadir}/icons/hicolor/512x512/apps/qnvsm.png \
  -DVersionPrefix=%{release}
%cmake_build

%install
install -Dpm0755 %{_vpath_builddir}/qnvsm %{buildroot}%{_bindir}/qnvsm
install -Dpm0644 package/rpm/qnvsm.desktop %{buildroot}%{_datadir}/applications/qnvsm.desktop
install -Dpm0644 icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/qnvsm.png
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-2
- Add the Qt Widgets build dependency and explicitly install upstream artifacts.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
