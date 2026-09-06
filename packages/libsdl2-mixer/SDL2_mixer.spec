# SPDX-License-Identifier: Apache-2.0
Name:           SDL2_mixer
Version:        2.8.2
Release:        1%{?dist}
Summary:        Multi-channel audio mixer library for SDL 2
License:        Zlib
URL:            https://github.com/libsdl-org/SDL_mixer
Source0:        SDL2_mixer-%{version}.tar.gz

BuildRequires:  SDL2-devel
BuildRequires:  flac-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  gcc
BuildRequires:  libmodplug-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  make
BuildRequires:  mpg123-devel
BuildRequires:  opusfile-devel
BuildRequires:  pkgconf
BuildRequires:  wavpack-devel
Provides:       libsdl2-mixer = %{version}-%{release}
Provides:       bundled(timidity)

%description
SDL2_mixer is a multi-channel audio mixer library for SDL 2. It supports
streaming and sampled audio in common tracker, MIDI, lossless, and compressed
music formats.

%package devel
Summary:        Development files for SDL2_mixer
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-devel%{?_isa}
Requires:       pkgconf
Provides:       libsdl2-mixer-devel = %{version}-%{release}

%description devel
Header, shared-library linker name, pkg-config metadata, and CMake metadata for
developing applications with SDL2_mixer.

%prep
%autosetup -p1

%build
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --enable-music-mod-modplug \
  --disable-music-mod-modplug-shared \
  --disable-music-mod-xmp \
  --enable-music-midi-fluidsynth \
  --disable-music-midi-fluidsynth-shared \
  --disable-music-ogg-stb \
  --enable-music-ogg-vorbis \
  --disable-music-ogg-vorbis-shared \
  --disable-music-flac-drflac \
  --enable-music-flac-libflac \
  --disable-music-flac-libflac-shared \
  --disable-music-mp3-minimp3 \
  --enable-music-mp3-mpg123 \
  --disable-music-mp3-mpg123-shared \
  --disable-music-opus-shared \
  --disable-music-wavpack-shared
%make_build

%install
%make_install
rm -f -- %{buildroot}%{_libdir}/libSDL2_mixer.la

%check
./build-scripts/test-versioning.sh

%files
%license LICENSE.txt
%doc CHANGES.txt README.txt
%{_libdir}/libSDL2_mixer-2.0.so.0*

%files devel
%license LICENSE.txt
%{_includedir}/SDL2/SDL_mixer.h
%{_libdir}/libSDL2_mixer.so
%{_libdir}/pkgconfig/SDL2_mixer.pc
%{_libdir}/cmake/SDL2_mixer/

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.2-1
- Initial openEuler RISC-V package from the official SDL 2 series release.
- Link the fixed-repository codec providers directly and retain full format support.
