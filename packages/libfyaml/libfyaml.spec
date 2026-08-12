# SPDX-License-Identifier: Apache-2.0
Name:           libfyaml
Version:        0.9.6
Release:        1%{?dist}
Summary:        Fully featured YAML parser and emitter library
License:        MIT AND GPL-2.0-only AND BSD-2-Clause
URL:            https://github.com/pantoniou/libfyaml
Source0:        libfyaml-%{version}.tar.gz
Source1:        yaml-test-suite-6e6c296ae9c9d2d5c4134b4b64d01b29ac19ff6f.tar.gz
Source2:        JSONTestSuite-d64aefb55228d9584d3e5b2433f720ea8fd00c82.tar.gz

BuildRequires:  bash
BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  jq
BuildRequires:  libyaml-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  pkgconf

%description
libfyaml is a YAML parser and emitter library supporting YAML 1.2, path
expressions, event streams, composition, and command-line processing tools.

%package devel
Summary:        Development files for libfyaml
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, manual pages, pkg-config metadata, and the unversioned linker name
for developing applications with libfyaml.

%package static
Summary:        Static library for libfyaml
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The static libfyaml library for applications that explicitly require static
linking.

%prep
%autosetup -p1 -a 1 -a 2
mv yaml-test-suite-6e6c296ae9c9d2d5c4134b4b64d01b29ac19ff6f \
  test/test-suite-data
mv JSONTestSuite-d64aefb55228d9584d3e5b2433f720ea8fd00c82 \
  test/json-test-suite-data
touch test/test-suite-data.checkout.timestamp
touch test/json-test-suite-data.checkout.timestamp

%build
%configure --enable-network --without-libclang
%make_build

%install
%make_install
rm -f -- %{buildroot}%{_libdir}/libfyaml.la

%check
%{__make} check

%files
%license LICENSE
%doc AUTHORS CHANGELOG.md README.md
%{_bindir}/fy-*
%{_libdir}/libfyaml.so.0*
%{_mandir}/man1/fy-*.1*

%files devel
%license LICENSE
%{_includedir}/libfyaml.h
%{_includedir}/libfyaml/
%{_libdir}/libfyaml.so
%{_libdir}/pkgconfig/libfyaml.pc
%{_mandir}/man3/libfyaml*.3*

%files static
%license LICENSE
%{_libdir}/libfyaml.a

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.6-1
- Initial openEuler RISC-V package with both pinned upstream conformance corpora.
- Run the full upstream check suite offline without disabling any declared test.
