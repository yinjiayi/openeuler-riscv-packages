# SPDX-License-Identifier: Apache-2.0
Name:           rakarrack-plus
Version:        1.4.1
Release:        6%{?dist}
Summary:        Guitar Effects Processor
License:        GPL-2.0-or-later
URL:            https://github.com/Stazed/rakarrack-plus
Source0:        rakarrack-plus-1.4.1.tar.gz
BuildRequires:  cmake
BuildRequires:  alsa-lib-devel
BuildRequires:  alsa-utils
BuildRequires:  fltk-devel
BuildRequires:  fltk-fluid
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  liblo-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libX11-devel
BuildRequires:  libXft-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXrender-devel
BuildRequires:  lv2-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  zlib-devel

%description
Guitar Effects Processor

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_TESTING=ON \
  -DBUILD_RPLUS_STANDALONE=ON \
  -DBUILD_RPLUS_LV2=OFF \
  -DBUILD_LV2_EFFECTS=ON \
  -DENABLE_ZITA=OFF
%cmake_build

%install
%cmake_install
# RPM compresses manual pages after install; list that page in %%files below.
find %{buildroot} \( -type f -o -type l \) \
  ! -path '%{buildroot}%{_mandir}/man1/rakarrack-plus.1' \
  -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%{_mandir}/man1/rakarrack-plus.1*
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-6
- Match the manual page after RPM's post-install compression.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-5
- Allow 120 minutes for the complete QEMU build and upstream test suite.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-4
- Configure in the RPM out-of-source build directory used by later macros.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-3
- Add the split FLTK fluid compiler required by CMake's FLTK discovery.
- Keep the standalone application and RakarrackPlus LV2 effects enabled.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-2
- Declare the full standalone and LV2-effects build dependency set.
- Use upstream's supported FLTK/libsamplerate configuration where NTK and
  zita-resampler are unavailable in the target repositories.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
