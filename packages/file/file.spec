# SPDX-License-Identifier: Apache-2.0
Name:           file
Version:        5.48
Release:        1%{?dist}
Summary:        Utility for determining file types
License:        BSD-2-Clause-Darwin AND BSD-2-Clause
URL:            https://www.darwinsys.com/file/
Source0:        file-%{version}.tar.gz

BuildRequires:  bzip2-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zstd-devel
Requires:       file-libs%{?_isa} = %{version}-%{release}

%description
The file command classifies files by inspecting their contents rather than
only their names.

%package libs
Summary:        Runtime library and magic database for file

%description libs
This package contains libmagic and the compiled and textual magic databases.

%package devel
Summary:        Development files for libmagic
Requires:       file-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for libmagic.

%package help
Summary:        Documentation for file and libmagic
BuildArch:      noarch

%description help
Manual pages and upstream release documentation for file and libmagic.

%prep
%autosetup -p1

%build
%configure \
  --disable-lzlib \
  --disable-libseccomp \
  --disable-static \
  --enable-bzlib \
  --enable-fsect-man5 \
  --enable-xzlib \
  --enable-zlib \
  --enable-zstdlib
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libmagic.la
install -Dpm 0644 /dev/null %{buildroot}%{_sysconfdir}/magic
cat magic/Magdir/* > %{buildroot}%{_datadir}/misc/magic
mkdir -p %{buildroot}%{_datadir}/file
ln -s misc/magic %{buildroot}%{_datadir}/magic
ln -s ../magic %{buildroot}%{_datadir}/file/magic

%check
export LD_LIBRARY_PATH="$PWD/src/.libs"
%make_build check

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/magic
%{_bindir}/file

%files libs
%license COPYING
%{_libdir}/libmagic.so.1*
%{_datadir}/file/
%{_datadir}/magic
%{_datadir}/misc/magic*

%files devel
%license COPYING
%{_includedir}/magic.h
%{_libdir}/libmagic.so
%{_libdir}/pkgconfig/libmagic.pc

%files help
%license COPYING
%doc AUTHORS ChangeLog NEWS README.DEVELOPER README.md
%{_mandir}/man1/file.1*
%{_mandir}/man3/libmagic.3*
%{_mandir}/man5/magic.5*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.48-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
