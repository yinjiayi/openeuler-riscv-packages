# SPDX-License-Identifier: Apache-2.0
Name:           jq
Version:        1.8.2
Release:        1%{?dist}
Summary:        Command-line JSON processor
License:        MIT AND ICU AND CC-BY-3.0
URL:            https://jqlang.org/
Source0:        jq-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  oniguruma-devel
BuildRequires:  tzdata

%description
jq is a command-line utility and library for selecting, filtering, mapping,
and transforming JSON data.

%package devel
Summary:        Development files for libjq
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for libjq.

%package help
Summary:        Documentation for jq
BuildArch:      noarch

%description help
The jq manual page and upstream release documentation.

%prep
%autosetup -p1

%build
%configure \
  --disable-docs \
  --disable-static \
  --disable-valgrind
test ! -f vendor/oniguruma/Makefile
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libjq.la
rm -rf %{buildroot}%{_docdir}/%{name}

%check
%make_build check

%files
%license COPYING
%{_bindir}/jq
%{_libdir}/libjq.so.1*

%files devel
%license COPYING
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_libdir}/libjq.so
%{_libdir}/pkgconfig/libjq.pc

%files help
%license COPYING
%doc AUTHORS ChangeLog NEWS.md README.md
%{_mandir}/man1/jq.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
