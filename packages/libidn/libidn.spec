# SPDX-License-Identifier: Apache-2.0
Name:           libidn
Version:        1.44
Release:        1%{?dist}
Summary:        Internationalized Domain Name support library
License:        (LGPL-3.0-or-later OR GPL-2.0-or-later) AND GPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://www.gnu.org/software/libidn/
Source0:        libidn-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  grep
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  texinfo

%description
GNU Libidn implements Stringprep, Punycode, and the IDNA 2003 specifications
for internationalized domain names. This package contains the runtime library
and command-line tool.

%package devel
Summary:        Development files for GNU Libidn
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, examples, pkg-config metadata, and the unversioned linker name for
developing applications with GNU Libidn.

%package help
Summary:        Documentation for GNU Libidn
BuildArch:      noarch

%description help
GNU Libidn manual pages, Info documentation, and upstream release notes.

%prep
%autosetup -p1

%build
EMACS=no %configure \
  --disable-csharp \
  --disable-java \
  --disable-static \
  --disable-valgrind-tests
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libidn.la
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
export LD_LIBRARY_PATH="$PWD/lib/.libs"
%make_build check

%files -f %{name}.lang
%license COPYING COPYING.LESSERv3
%{_bindir}/idn
%{_libdir}/libidn.so.12*

%files devel
%license COPYING COPYING.LESSERv3
%doc examples/
%{_includedir}/*.h
%{_libdir}/libidn.so
%{_libdir}/pkgconfig/libidn.pc

%files help
%license COPYING COPYING.LESSERv3
%doc AUTHORS FAQ NEWS README THANKS
%{_infodir}/libidn.info*
%{_mandir}/man1/idn.1*
%{_mandir}/man3/*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.44-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
