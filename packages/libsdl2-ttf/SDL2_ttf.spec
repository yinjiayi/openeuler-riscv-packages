# SPDX-License-Identifier: Apache-2.0
Name:           SDL2_ttf
Version:        2.24.0
Release:        2%{?dist}
Summary:        TrueType font rendering library for SDL2
License:        Zlib
URL:            https://github.com/libsdl-org/SDL_ttf
Source0:        SDL2_ttf-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(sdl2)

%description
SDL2_ttf is a TrueType font rendering library for SDL2 applications. It uses
FreeType for font loading and HarfBuzz for text shaping.

%package devel
Summary:        Development files for SDL2_ttf
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf
Requires:       pkgconfig(freetype2)
Requires:       pkgconfig(harfbuzz)
Requires:       pkgconfig(sdl2)

%description devel
The SDL2_ttf-devel package contains the public header, linker name, pkg-config
metadata, and CMake package files needed to develop SDL2_ttf applications.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DSDL2TTF_HARFBUZZ=ON \
  -DSDL2TTF_INSTALL=ON \
  -DSDL2TTF_SAMPLES=OFF \
  -DSDL2TTF_VENDORED=OFF
%cmake_build

%install
%cmake_install

%check
cat > api-check.c <<'EOF'
#define SDL_MAIN_HANDLED
#include <SDL.h>
#include "SDL_ttf.h"

int main(void) {
    int freetype_major = 0;
    int freetype_minor = 0;
    int freetype_patch = 0;
    int harfbuzz_major = 0;
    int harfbuzz_minor = 0;
    int harfbuzz_patch = 0;
    const SDL_version *linked = 0;
    TTF_Font *font = 0;
    SDL_Surface *surface = 0;
    SDL_Color white = {255, 255, 255, 255};

    SDL_SetMainReady();
    if (SDL_Init(0) != 0 || TTF_Init() != 0) {
        return 1;
    }
    linked = TTF_Linked_Version();
    TTF_GetFreeTypeVersion(&freetype_major, &freetype_minor, &freetype_patch);
    TTF_GetHarfBuzzVersion(&harfbuzz_major, &harfbuzz_minor, &harfbuzz_patch);
    font = TTF_OpenFont("external/harfbuzz/perf/fonts/Roboto-Regular.ttf", 18);
    if (font != 0) {
        surface = TTF_RenderUTF8_Blended(font, "openEuler RVA23", white);
    }
    if (surface == 0 || surface->w <= 0 || surface->h <= 0) {
        if (font != 0) {
            TTF_CloseFont(font);
        }
        TTF_Quit();
        SDL_Quit();
        return 1;
    }
    SDL_FreeSurface(surface);
    TTF_CloseFont(font);
    TTF_Quit();
    SDL_Quit();
    return linked == 0 || linked->major != 2 || linked->minor != 24 ||
           linked->patch != 0 || freetype_major <= 0 || harfbuzz_major <= 0;
}
EOF
%{__cc} %{optflags} api-check.c -I. \
  $(pkg-config --cflags sdl2) \
  -L%{_vpath_builddir} -Wl,-rpath,%{_vpath_builddir} \
  -lSDL2_ttf $(pkg-config --libs sdl2) -o api-check
./api-check

%files
%license %{_datadir}/licenses/SDL2_ttf/LICENSE.txt
%doc CHANGES.txt README-versions.md README.txt
%{_libdir}/libSDL2_ttf-2.0.so.0*

%files devel
%{_includedir}/SDL2/SDL_ttf.h
%{_libdir}/cmake/SDL2_ttf/
%{_libdir}/libSDL2_ttf-2.0.so
%{_libdir}/libSDL2_ttf.so
%{_libdir}/pkgconfig/SDL2_ttf.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.24.0-2
- Package the alternate development linker name installed by upstream CMake.

* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.24.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Build the shared SDL2 library with system FreeType and HarfBuzz dependencies.
