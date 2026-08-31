# SPDX-License-Identifier: Apache-2.0
Name:           iniparser
Version:        4.2.6
Release:        1%{?dist}
Summary:        Portable C library for parsing INI files
License:        MIT
URL:            https://gitlab.com/iniparser/iniparser
Source0:        iniparser-%{version}.tar.gz
Source1:        unity-2.7.0.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ruby
BuildRequires:  rubygem-psych

%description
iniparser is a portable C library for reading, querying, and writing INI-style
configuration files.

%package devel
Summary:        Development files for iniparser
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, static library, pkg-config metadata, CMake integration, and the
unversioned shared-library link for developing applications with iniparser.

%prep
%autosetup -p1 -n iniparser-v%{version} -a 1
# FETCHCONTENT_SOURCE_DIR_UNITY intentionally bypasses FetchContent's download,
# update, and patch steps. Reproduce upstream's declared PATCH_COMMAND locally
# so UNITY_INCLUDE_CONFIG_H resolves without allowing configuration-time I/O.
install -m 0644 test/unity_config.h Unity-2.7.0/src/unity_config.h

%build
%cmake_conf \
  -DBUILD_DOCS=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_UNITY="$PWD/Unity-2.7.0"
%cmake_build

%install
%cmake_install
# Unity is a pinned test-only dependency; do not ship its install targets as
# part of iniparser.
rm -rf %{buildroot}%{_includedir}/unity
rm -rf %{buildroot}%{_libdir}/cmake/unity
rm -f %{buildroot}%{_libdir}/libunity.a

%check
%ctest

%files
%license LICENSE
%doc AUTHORS FAQ-en.md FAQ-zhcn.md README.md
%{_libdir}/libiniparser.so.4*

%files devel
%license LICENSE
%{_includedir}/iniparser/
%{_libdir}/libiniparser.a
%{_libdir}/libiniparser.so
%{_libdir}/cmake/iniparser/
%{_libdir}/pkgconfig/iniparser.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.6-1
- Initial openEuler RISC-V package with the complete offline upstream CTest suite.
- Pin the Unity 2.7.0 test dependency instead of fetching a mutable branch.
