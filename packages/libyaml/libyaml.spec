# SPDX-License-Identifier: Apache-2.0
Name:           libyaml
Version:        0.2.5
Release:        1%{?dist}
Summary:        YAML 1.1 parser and emitter library
License:        MIT
URL:            https://github.com/yaml/libyaml
Source0:        yaml-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
LibYAML is a C library for parsing and emitting YAML 1.1 streams.

%package devel
Summary:        Development files for LibYAML
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The LibYAML header, pkg-config metadata, and unversioned library link for
developing YAML parsers and emitters.

%prep
%autosetup -n yaml-%{version} -p1

%build
%configure --disable-static --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license License
%doc Changes ReadMe.md
%{_libdir}/libyaml-0.so.2*

%files devel
%license License
%{_includedir}/yaml.h
%{_libdir}/libyaml.so
%{_libdir}/pkgconfig/yaml-0.1.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.5-1
- Initial openEuler RISC-V package with upstream parser tests.
