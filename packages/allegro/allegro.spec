# SPDX-License-Identifier: Apache-2.0
Name:           allegro
Version:        5.2.11.3
Release:        1%{?dist}
Summary:        Cross-platform game programming library
License:        Zlib AND BSD-3-Clause AND OFL-1.1 AND LicenseRef-Custom
URL:            https://liballeg.org/
Source0:        allegro-5.2.11.3.tar.gz
Patch0:         0001-cmake-use-configured-install-libdir-in-pkgconfig.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  flac-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk3-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libogg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libwebp-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  openal-soft-devel
BuildRequires:  opus-devel
BuildRequires:  opusfile-devel
BuildRequires:  physfs-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pulseaudio-libs-devel

%description
Allegro 5 is a cross-platform library for video game and multimedia
programming.  It provides graphics, input, audio, image, font, filesystem,
native-dialog, and video APIs while keeping the Allegro 5 ABI separate from
the incompatible Allegro 4 series.

%package devel
Summary:        Development files for Allegro 5
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, linker names, pkg-config modules, and CMake package metadata for
building Allegro 5 applications and add-ons.

%prep
%autosetup -p1

%build
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_C_FLAGS_RELWITHDEBINFO='%{build_cflags}' \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO='%{build_cxxflags}' \
  -DCMAKE_EXE_LINKER_FLAGS='%{build_ldflags}' \
  -DCMAKE_SHARED_LINKER_FLAGS='%{build_ldflags}' \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DSHARED=ON \
  -DWANT_X11=ON \
  -DWANT_OPENGL=ON \
  -DWANT_AUDIO=ON \
  -DWANT_IMAGE=ON \
  -DWANT_FONT=ON \
  -DWANT_TTF=ON \
  -DWANT_COLOR=ON \
  -DWANT_MEMFILE=ON \
  -DWANT_PHYSFS=ON \
  -DWANT_PRIMITIVES=ON \
  -DWANT_NATIVE_DIALOG=ON \
  -DWANT_VIDEO=ON \
  -DWANT_IMAGE_FREEIMAGE=OFF \
  -DWANT_DUMB=OFF \
  -DWANT_OPENMPT=OFF \
  -DWANT_MP3=OFF \
  -DWANT_DEMO=OFF \
  -DWANT_EXAMPLES=OFF \
  -DWANT_DOCS=OFF \
  -DWANT_TESTS=ON
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build

%check
# The graphical test driver requires a display.  Keep and execute upstream's
# deterministic, display-independent internal list test under target QEMU.
cmake --build build --target run_standalone_tests

%files
%license LICENSE.txt
%doc README.txt README_packaging.txt
%{_libdir}/liballegro*.so.*

%files devel
%{_includedir}/allegro5/
%{_libdir}/liballegro*.so
%{_libdir}/cmake/allegro/
%{_libdir}/pkgconfig/allegro*-5.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.2.11.3-1
- Initial openEuler RISC-V package with the headless upstream list test.
