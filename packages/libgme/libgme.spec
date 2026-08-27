# SPDX-License-Identifier: Apache-2.0
Name:           libgme
Version:        0.6.5
Release:        1%{?dist}
Summary:        Video game music file emulation/playback library
License:        LGPL-2.1-or-later
URL:            https://github.com/libgme/game-music-emu
Source0:        libgme-0.6.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Video game music file emulation/playback library

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
%license license.gpl2.txt
%license license.txt


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.5-1
- Initial openEuler RISC-V package from the full package inventory.
