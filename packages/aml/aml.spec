# SPDX-License-Identifier: Apache-2.0
Name:           aml
Version:        1.0.0
Release:        1%{?dist}
Summary:        Another Main Loop event library
License:        ISC
URL:            https://github.com/any1/aml
Source0:        aml-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build

%description
aml is a small C event-loop library with file-descriptor, timer, ticker,
signal, idle-dispatch, and thread-pool support.

%package devel
Summary:        Development files for aml
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config metadata, and unversioned library link for developing
applications with aml.

%prep
%autosetup -p1

%build
%meson -Dexamples=true
%meson_build

%install
%meson_install

%check
printf 'exit\n' | "%{_vpath_builddir}/examples/reader" | grep -F 'Exiting...'

%files
%license COPYING
%doc README.md
%{_libdir}/libaml.so.1*

%files devel
%license COPYING
%{_includedir}/aml1/
%{_libdir}/libaml.so
%{_libdir}/pkgconfig/aml1.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package.
