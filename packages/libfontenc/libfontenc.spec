# SPDX-License-Identifier: Apache-2.0
Name:           libfontenc
Version:        1.1.9
Release:        1%{?dist}
Summary:        Font encoding library for X.Org applications
License:        MIT AND ISC
URL:            https://www.x.org/
Source0:        libfontenc-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  xorg-x11-font-utils
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  zlib-devel

%description
libfontenc parses and maps font encodings for X.Org applications.

%package devel
Summary:        Development files for libfontenc
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-proto-devel

%description devel
The public header, pkg-config metadata, and unversioned library link needed
to build programs using libfontenc.

%prep
%autosetup -p1

%build
%configure --disable-static --with-fontrootdir=%{_datadir}/X11/fonts
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libfontenc.la

%check
%make_build check
# Upstream registers no automated test programs; test its built-in map here.
cat > fontenc-api-check.c <<'EOF'
#include <X11/fonts/fontenc.h>
#include <string.h>

int main(void) {
    FontEncPtr encoding = FontEncFind("iso8859-1", 0);
    FontMapPtr mapping = FontMapFind(encoding, FONT_ENCODING_UNICODE, 0, 0);
    const char *xlfd = "-misc-fixed-medium-r-normal--13-120-75-75-c-70-iso8859-1";
    char *name = FontEncFromXLFD(xlfd, strlen(xlfd));
    if (!encoding || !mapping || !name) return 1;
    if (strcmp(name, "iso8859-1") != 0) return 2;
    return FontEncRecode(0x41, mapping) == 0x41 ? 0 : 3;
}
EOF
${CC:-cc} -Iinclude fontenc-api-check.c -Lsrc/.libs -lfontenc -o fontenc-api-check
LD_LIBRARY_PATH="$PWD/src/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./fontenc-api-check

%files
%license COPYING
%doc ChangeLog README.md
%{_libdir}/libfontenc.so.1*

%files devel
%license COPYING
%{_includedir}/X11/fonts/fontenc.h
%{_libdir}/libfontenc.so
%{_libdir}/pkgconfig/fontenc.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.9-1
- Initial package from the official, SHA-256-pinned X.Org release.
