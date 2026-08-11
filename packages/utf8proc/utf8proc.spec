# SPDX-License-Identifier: Apache-2.0
Name:           utf8proc
Version:        2.11.3
Release:        1%{?dist}
Summary:        Unicode normalization and case-folding library
License:        MIT
URL:            https://github.com/JuliaStrings/utf8proc
Source0:        utf8proc-%{version}.tar.gz
Source1:        NormalizationTest-17.0.0.txt
Source2:        GraphemeBreakTest-17.0.0.txt
Patch0:         0001-tests-use-pinned-unicode-data.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
utf8proc is a compact C library for Unicode normalization, case folding,
character properties, and grapheme-boundary processing.

%package devel
Summary:        Development files for utf8proc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header, pkg-config and CMake metadata, and unversioned shared-library
link for developing applications with utf8proc.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DUTF8PROC_ENABLE_TESTING=ON \
  -DUTF8PROC_GRAPHEME_BREAK_TEST_FILE=%{SOURCE2} \
  -DUTF8PROC_NORMALIZATION_TEST_FILE=%{SOURCE1}
%cmake_build

%install
%cmake_install

%check
%ctest -- -j1

%files
%license LICENSE.md
%doc NEWS.md README.md
%{_libdir}/libutf8proc.so.3*

%files devel
%license LICENSE.md
%{_includedir}/utf8proc.h
%{_libdir}/libutf8proc.so
%{_libdir}/pkgconfig/libutf8proc.pc
%{_libdir}/cmake/utf8proc/

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.11.3-1
- Initial openEuler RISC-V package with pinned Unicode 17.0.0 conformance data.
