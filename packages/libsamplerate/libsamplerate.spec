# SPDX-License-Identifier: Apache-2.0
Name:           libsamplerate
Version:        0.2.2
Release:        1%{?dist}
Summary:        Sample rate conversion library
License:        BSD-2-Clause
URL:            https://libsndfile.github.io/libsamplerate/
Source0:        libsamplerate-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
libsamplerate provides high-quality sample rate conversion for audio data.

%package devel
Summary:        Development files for libsamplerate
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, shared-library link, pkg-config metadata, and API documentation.

%prep
%autosetup -p1

%build
%cmake_conf -DBUILD_TESTING=ON -DLIBSAMPLERATE_EXAMPLES=OFF -DLIBSAMPLERATE_INSTALL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_libdir}/libsamplerate.so.0*

%files devel
%{_includedir}/samplerate.h
%{_libdir}/libsamplerate.so
%{_libdir}/pkgconfig/samplerate.pc
%{_libdir}/cmake/SampleRate/
%{_datadir}/doc/libsamplerate/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
