# SPDX-License-Identifier: Apache-2.0
Name:           opus
Version:        1.6.1
Release:        1%{?dist}
Summary:        Low-delay speech and audio codec library
License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://opus-codec.org/
Source0:        opus-%{version}.tar.gz

BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  make

%description
Opus is a low-delay, open audio codec designed for interactive speech and
music transmission over the Internet.

%package devel
Summary:        Development files for Opus
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned library link, pkg-config metadata, and Autoconf
integration files for developing applications with Opus.

%package help
Summary:        API documentation for Opus
BuildArch:      noarch

%description help
Generated API documentation and manual pages for the Opus codec library.

%prep
%autosetup -p1

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-custom-modes
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libopus.la

%check
%make_build check

%files
%license COPYING
%{_libdir}/libopus.so.0*

%files devel
%license COPYING
%{_includedir}/opus/
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4

%files help
%license COPYING
%doc AUTHORS README
%{_docdir}/opus/html/
%{_mandir}/man3/opus*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
