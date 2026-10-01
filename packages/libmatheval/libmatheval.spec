# SPDX-License-Identifier: Apache-2.0
Name:           libmatheval
Version:        1.1.11
Release:        1%{?dist}
Summary:        Library for parsing and evaluating symbolic expressions
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/libmatheval/
Source0:        libmatheval-%{version}.tar.gz
Patch0:         0001-guile-2.2.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  guile-devel
BuildRequires:  libtool
BuildRequires:  make

%description
GNU libmatheval parses mathematical expressions into in-memory trees that
can be evaluated, differentiated, and converted back to text.

%package devel
Summary:        Development files for libmatheval
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config metadata, and the unversioned library link for developing
applications with GNU libmatheval.

%prep
%autosetup -p1

%build
# The release archive omits this gettext auxiliary file required by autoreconf.
cp %{_datadir}/gettext/config.rpath config/config.rpath
autoreconf -fiv
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libmatheval.so.1*
%{_infodir}/libmatheval.info*

%files devel
%license COPYING
%{_includedir}/matheval.h
%{_libdir}/libmatheval.so
%{_libdir}/pkgconfig/libmatheval.pc

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.11-1
- Initial openEuler RISC-V package from the full package inventory.
