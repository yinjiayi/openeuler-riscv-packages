# SPDX-License-Identifier: Apache-2.0
Name:           chromaprint
Version:        1.6.1
Release:        1%{?dist}
Summary:        Audio fingerprinting library and tool
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND BSD-3-Clause
URL:            https://acoustid.org/chromaprint
Source0:        chromaprint-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ffmpeg-devel
BuildRequires:  fftw-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf
Requires:       libchromaprint%{?_isa} = %{version}-%{release}

%description
Chromaprint extracts compact fingerprints from audio. This package provides
fpcalc, the command-line fingerprint calculator.

%package -n libchromaprint
Summary:        Audio fingerprinting runtime library

%description -n libchromaprint
libchromaprint implements the Chromaprint audio fingerprinting algorithms and
public C API.

%package -n libchromaprint-devel
Summary:        Development files for libchromaprint
Requires:       libchromaprint%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description -n libchromaprint-devel
Header, unversioned linker name, pkg-config metadata, and CMake metadata for
developing applications with libchromaprint.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DAUDIO_PROCESSOR_LIB=swresample \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTS=ON \
  -DBUILD_TOOLS=ON \
  -DFFT_LIB=fftw3 \
  -DUSE_INTERNAL_AVRESAMPLE=ON
%cmake_build

%install
%cmake_install
# Upstream incorrectly substitutes bindir for exec_prefix. Normalize the
# otherwise-correct installed pkg-config metadata without changing sources.
sed -i 's|^exec_prefix=.*|exec_prefix=${prefix}|' \
  %{buildroot}%{_libdir}/pkgconfig/libchromaprint.pc

%check
%ctest --output-on-failure --parallel 1

%files
%license LICENSE.md
%doc README.md NEWS.txt
%{_bindir}/fpcalc

%files -n libchromaprint
%license LICENSE.md
%{_libdir}/libchromaprint.so.1*

%files -n libchromaprint-devel
%license LICENSE.md
%{_includedir}/chromaprint.h
%{_libdir}/libchromaprint.so
%{_libdir}/pkgconfig/libchromaprint.pc
%{_libdir}/cmake/Chromaprint/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-1
- Update the target's compatible libchromaprint ABI and add the fpcalc tool.
- Run all 100 upstream tests with the target-matching FFTW3 backend.
