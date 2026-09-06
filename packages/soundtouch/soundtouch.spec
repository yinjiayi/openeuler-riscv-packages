# SPDX-License-Identifier: Apache-2.0
Name:           soundtouch
Version:        2.4.1
Release:        1%{?dist}
Summary:        Audio tempo, pitch, and playback-rate processing library
License:        LGPL-2.1-or-later
URL:            https://www.surina.net/soundtouch/
Source0:        soundtouch-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
SoundTouch is a C++ audio processing library for independently changing tempo,
pitch, and playback rate. The soundstretch command-line utility is included.

%package devel
Summary:        Development files for SoundTouch
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, CMake metadata, and pkg-config
metadata for developing applications with SoundTouch.

%prep
%autosetup -p1 -n soundtouch

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DINTEGER_SAMPLES=OFF \
  -DNEON=OFF \
  -DOPENMP=OFF \
  -DSOUNDSTRETCH=ON \
  -DSOUNDTOUCH_DLL=OFF
%cmake_build

%install
%cmake_install

%check
version_output=$("%{_vpath_builddir}/soundstretch" 2>&1 || :)
printf '%s\n' "$version_output" | grep -F 'SoundStretch v2.4.1'
cat > api-check.cpp <<'EOF'
#include <SoundTouch.h>

int main() {
    soundtouch::SoundTouch processor;
    processor.setSampleRate(48000);
    processor.setChannels(2);
    processor.setTempo(1.0f);
    return processor.getVersionId() == 20401 ? 0 : 1;
}
EOF
%{__cxx} %{optflags} -std=c++17 api-check.cpp \
  -Iinclude -L%{_vpath_builddir} \
  -Wl,-rpath,%{_vpath_builddir} -lSoundTouch -o api-check
./api-check

%files
%license COPYING.TXT
%doc README.html readme.md
%{_bindir}/soundstretch
%{_libdir}/libSoundTouch.so.2*

%files devel
%license COPYING.TXT
%{_includedir}/soundtouch/
%{_libdir}/cmake/SoundTouch/
%{_libdir}/libSoundTouch.so
%{_libdir}/pkgconfig/soundtouch.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
