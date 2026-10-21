# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           tllist
Version:        1.1.0
Release:        1%{?dist}
Summary:        Typed linked-list header for C
License:        MIT
URL:            https://codeberg.org/dnkl/tllist
Source0:        tllist-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
tllist is a header-only C implementation of type-safe doubly linked lists
using preprocessor macros. It installs the public header and pkg-config data.

%prep
%autosetup -p1 -n tllist

%build
%meson
%meson_build

%install
%meson_install
rm -rf %{buildroot}%{_docdir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_libdir}/pkgconfig/tllist.pc \
  %{buildroot}%{_datadir}/pkgconfig/tllist.pc
rmdir %{buildroot}%{_libdir}/pkgconfig
rmdir %{buildroot}%{_libdir}

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_includedir}/tllist.h
%{_datadir}/pkgconfig/tllist.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package with the complete upstream unit test.
