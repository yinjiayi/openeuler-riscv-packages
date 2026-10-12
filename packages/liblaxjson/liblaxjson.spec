# SPDX-License-Identifier: Apache-2.0
Name:           liblaxjson
Version:        1.0.5
Release:        1%{?dist}
%global upstream_commit 9f55366a50c31c3be33705a3ee21d52eb77cb4ab
Summary:        Streaming permissive JSON parser library
License:        MIT
URL:            https://github.com/andrewrk/liblaxjson
Source0:        liblaxjson-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
liblaxjson is a small streaming C parser for JSON configuration files.

%package devel
Summary:        Development files for liblaxjson
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public C header, unversioned shared-library link, and static library for
developing applications with liblaxjson.

%prep
%autosetup -n liblaxjson-%{upstream_commit} -p1

%build
%cmake_conf
%cmake_build

%install
%cmake_install
# Upstream hardcodes a prefix-relative lib/ destination; place both libraries
# in the target architecture's canonical libdir without changing the source.
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/liblaxjson* %{buildroot}%{_libdir}/

%check
# Run the sole registered upstream CTest, which covers JSON primitive parsing.
%ctest -- -j1

%files
%license COPYING
%doc README.md CHANGELOG.md
%{_libdir}/liblaxjson.so.1*

%files devel
%license COPYING
%{_includedir}/laxjson.h
%{_libdir}/liblaxjson.so
%{_libdir}/liblaxjson.a

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial package from the official SHA-256-pinned liblaxjson 1.0.5 source.
