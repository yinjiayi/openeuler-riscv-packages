# SPDX-License-Identifier: Apache-2.0
Name:           qt-img-viewer
Version:        0.1.5
Release:        1%{?dist}
Summary:        Qt 6 image viewer with directory thumbnails, animated GIF playback, and image-only floating mode
License:        MIT
URL:            https://github.com/jswysnemc/qt-img-viewer
Source0:        qt-img-viewer-0.1.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt 6 image viewer with directory thumbnails, animated GIF playback, and image-only floating mode

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.5-1
- Initial openEuler RISC-V package from the full package inventory.
