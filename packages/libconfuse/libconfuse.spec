# SPDX-License-Identifier: Apache-2.0
Name:           libconfuse
Version:        3.4
Release:        1%{?dist}
Summary:        Configuration file parser library
License:        ISC
URL:            https://github.com/libconfuse/libconfuse
Source0:        confuse-3.4.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make

%description
libConfuse is a small configuration-file parser library supporting sections,
lists, typed values, and callbacks.

%package devel
Summary:        Development files for libConfuse
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config metadata, and unversioned library link for developing
applications with libConfuse.

%prep
%autosetup -p1 -n confuse-%{version}

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libconfuse.la
rm -rf %{buildroot}%{_docdir}/confuse
%find_lang confuse

%check
%make_build check

%files -f confuse.lang
%license LICENSE
%doc AUTHORS ChangeLog.md README.md
%{_libdir}/libconfuse.so.2*

%files devel
%license LICENSE
%{_includedir}/confuse.h
%{_libdir}/libconfuse.so
%{_libdir}/pkgconfig/libconfuse.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package.
