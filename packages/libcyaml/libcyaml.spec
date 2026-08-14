# SPDX-License-Identifier: Apache-2.0
Name:           libcyaml
Version:        1.4.2
Release:        1%{?dist}
Summary:        Schema-based YAML parsing and serialization library
License:        ISC
URL:            https://github.com/tlsa/libcyaml
Source0:        libcyaml-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
LibCYAML is a C11 library for loading and saving structured YAML documents
using caller-defined schemas.

%package devel
Summary:        Development files for LibCYAML
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libyaml-devel%{?_isa}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with LibCYAML.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build \
  PREFIX=%{_prefix} \
  LIBDIR=%{_lib} \
  INCLUDEDIR=include \
  PKG_CONFIG=pkg-config

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_lib} \
  INCLUDEDIR=include \
  PKG_CONFIG=pkg-config
rm -f %{buildroot}%{_libdir}/libcyaml.a

%check
# Upstream's `test` target runs every unit against both shared and static libs.
%make_build test \
  PREFIX=%{_prefix} \
  LIBDIR=%{_lib} \
  INCLUDEDIR=include \
  PKG_CONFIG=pkg-config

%files
%license LICENSE
%doc CHANGES.md README.md
%{_libdir}/libcyaml.so.1*

%files devel
%license LICENSE
%{_includedir}/cyaml/
%{_libdir}/libcyaml.so
%{_libdir}/pkgconfig/libcyaml.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package with the complete shared/static upstream tests.
