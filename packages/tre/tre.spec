# SPDX-License-Identifier: Apache-2.0
Name:           tre
Version:        0.9.0
Release:        1%{?dist}
Summary:        Approximate regular expression matching library
License:        BSD-2-Clause
URL:            https://github.com/laurikari/tre
Source0:        tre-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  glibc-all-langpacks
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
TRE is a POSIX-compatible regular expression library with approximate
matching, wide-character support, and a stream-oriented matching API.

%package -n agrep
Summary:        Approximate grep utility built with TRE
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n agrep
agrep searches text using exact or approximate regular expressions and
supports record-oriented matching.

%package devel
Summary:        Development files for TRE
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for TRE.

%package help
Summary:        Documentation and translations for TRE
BuildArch:      noarch

%description help
TRE API and syntax references, release documentation, and translated agrep
messages.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-rpath \
  --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%find_lang %{name}

%check
%make_build check

%files
%license LICENSE
%{_libdir}/libtre.so.5*

%files -n agrep
%license LICENSE
%{_bindir}/agrep
%{_mandir}/man1/agrep.1*

%files devel
%license LICENSE
%{_includedir}/tre/
%{_libdir}/libtre.so
%{_libdir}/pkgconfig/tre.pc

%files help -f %{name}.lang
%license LICENSE
%doc AUTHORS ChangeLog NEWS README.md THANKS TODO
%doc doc/default.css doc/tre-api.html doc/tre-syntax.html

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
