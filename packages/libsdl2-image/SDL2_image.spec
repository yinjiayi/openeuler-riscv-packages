# SPDX-License-Identifier: Apache-2.0
Name:           SDL2_image
Version:        2.8.8
Release:        1%{?dist}
Summary:        Image loading library for SDL 2
License:        Zlib
URL:            https://github.com/libsdl-org/SDL_image
Source0:        SDL2_image-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
BuildRequires:  make
BuildRequires:  SDL2-devel
BuildRequires:  SDL2-static

%description
SDL2_image extends SDL 2 with image-file detection, decoding, and encoding.
This build provides the shared library with its portable built-in loaders and
the JPEG, PNG, TIFF, and WebP system-library backends available in the fixed
openEuler target repository.

%package devel
Summary:        Development files for SDL2_image
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libjpeg-turbo-devel%{?_isa}
Requires:       libpng-devel%{?_isa}
Requires:       libtiff-devel%{?_isa}
Requires:       libwebp-devel%{?_isa}
Requires:       SDL2-devel%{?_isa}
Provides:       cmake(SDL2_image) = %{version}
Provides:       pkgconfig(SDL2_image) = %{version}

%description devel
Header, unversioned library link, pkg-config metadata, and CMake package
configuration for developing applications with SDL2_image.

%prep
%autosetup -p1 -n SDL2_image-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DSDL2IMAGE_AVIF=OFF \
  -DSDL2IMAGE_BACKEND_STB=OFF \
  -DSDL2IMAGE_BMP=ON \
  -DSDL2IMAGE_DEPS_SHARED=OFF \
  -DSDL2IMAGE_GIF=ON \
  -DSDL2IMAGE_INSTALL=ON \
  -DSDL2IMAGE_JPG=ON \
  -DSDL2IMAGE_JPG_SAVE=ON \
  -DSDL2IMAGE_JXL=OFF \
  -DSDL2IMAGE_LBM=ON \
  -DSDL2IMAGE_PCX=ON \
  -DSDL2IMAGE_PNG=ON \
  -DSDL2IMAGE_PNG_SAVE=ON \
  -DSDL2IMAGE_PNM=ON \
  -DSDL2IMAGE_QOI=ON \
  -DSDL2IMAGE_SAMPLES=ON \
  -DSDL2IMAGE_SAMPLES_INSTALL=OFF \
  -DSDL2IMAGE_STRICT=ON \
  -DSDL2IMAGE_SVG=ON \
  -DSDL2IMAGE_TGA=ON \
  -DSDL2IMAGE_TESTS=ON \
  -DSDL2IMAGE_TESTS_INSTALL=OFF \
  -DSDL2IMAGE_TIF=ON \
  -DSDL2IMAGE_VENDORED=OFF \
  -DSDL2IMAGE_WEBP=ON \
  -DSDL2IMAGE_XCF=ON \
  -DSDL2IMAGE_XPM=ON \
  -DSDL2IMAGE_XV=ON
%cmake_build

%install
%cmake_install

%check
%ctest --parallel 1

%files
%license LICENSE.txt
%doc CHANGES.txt README.txt
%{_libdir}/libSDL2_image-2.0.so.0*

%files devel
%license LICENSE.txt
%{_includedir}/SDL2/SDL_image.h
%{_libdir}/libSDL2_image.so
%{_libdir}/cmake/SDL2_image/
%{_libdir}/pkgconfig/SDL2_image.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.8-1
- Initial openEuler RISC-V package from verified official SDL 2 release bytes.
