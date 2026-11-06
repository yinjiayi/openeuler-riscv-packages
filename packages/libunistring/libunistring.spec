# SPDX-License-Identifier: Apache-2.0
Name:           libunistring
Version:        1.4.2
Release:        2%{?dist}
Summary:        Unicode string manipulation library for C
License:        GPL-2.0-or-later OR LGPL-3.0-or-later
URL:            https://www.gnu.org/software/libunistring/
Source0:        libunistring-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
GNU libunistring provides Unicode string handling and conversions for C
programs, including UTF encodings, normalization, and character properties.

%package devel
Summary:        Development files for libunistring
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, Info documentation, and the unversioned library link for developing
applications with libunistring.

%prep
%autosetup -p1

%build
%configure --disable-rpath --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libunistring.la
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%check
%make_build check

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/libunistring.so.5*

%files devel
%license COPYING COPYING.LIB
%doc DEPENDENCIES HACKING THANKS ChangeLog
%{_includedir}/*.h
%{_includedir}/unistring/
%{_infodir}/libunistring.info*
%{_libdir}/libunistring.so

%changelog
* Sat Sep 05 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-2
- Raise the bounded QEMU package timeout after normal compilation exhausted the
  former 60-minute budget; keep the complete upstream test suite enabled.

* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package with the complete upstream test suite.
