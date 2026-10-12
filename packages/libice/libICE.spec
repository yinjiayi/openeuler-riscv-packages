# SPDX-License-Identifier: Apache-2.0
Name:           libICE
Version:        1.1.2
Release:        1%{?dist}
Summary:        X.Org Inter-Client Exchange protocol library
License:        MIT
URL:            https://www.x.org/
Source0:        libICE-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-xtrans-devel

%description
libICE implements the X.Org Inter-Client Exchange protocol and its authority
record format.

%package devel
Summary:        Development files for libICE
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-proto-devel

%description devel
Headers, pkg-config metadata, unversioned library link, and XML protocol
documentation for applications using libICE.

%prep
%autosetup -p1 -n libICE-%{version}

%build
%configure --disable-static --enable-docs --enable-specs \
  --without-xmlto --without-fop --without-xsltproc \
  --docdir=%{_docdir}/%{name}
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libICE.la

%check
%make_build check
# Upstream registers no test programs; verify the authority record API.
cat > ice-api-check.c <<'EOF'
#include <X11/ICE/ICElib.h>
#include <X11/ICE/ICEutil.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char payload[] = "abcdef";
    char empty[] = "";
    IceAuthFileEntry original = {0};
    IceAuthFileEntry *readback = NULL;
    FILE *stream = tmpfile();
    int result = 0;
    if (!stream) return 1;
    original.protocol_name = "ICE";
    original.protocol_data = empty;
    original.network_id = "local/0";
    original.auth_name = "MIT-MAGIC-COOKIE-1";
    original.auth_data_length = sizeof(payload) - 1;
    original.auth_data = payload;
    if (!IceWriteAuthFileEntry(stream, &original)) result = 2;
    if (!result && fseek(stream, 0, SEEK_SET) != 0) result = 3;
    if (!result) readback = IceReadAuthFileEntry(stream);
    if (!result && !readback) result = 4;
    if (!result && (strcmp(readback->protocol_name, "ICE") != 0 ||
                    strcmp(readback->network_id, "local/0") != 0 ||
                    strcmp(readback->auth_name, "MIT-MAGIC-COOKIE-1") != 0 ||
                    readback->auth_data_length != sizeof(payload) - 1 ||
                    memcmp(readback->auth_data, payload, sizeof(payload) - 1) != 0)) result = 5;
    IceFreeAuthFileEntry(readback);
    fclose(stream);
    return result;
}
EOF
${CC:-cc} -Iinclude ice-api-check.c -Lsrc/.libs -lICE -o ice-api-check
LD_LIBRARY_PATH="$PWD/src/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./ice-api-check

%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_libdir}/libICE.so.6*

%files devel
%license COPYING
%{_includedir}/X11/ICE/
%{_libdir}/libICE.so
%{_libdir}/pkgconfig/ice.pc
%{_docdir}/libICE/*.xml

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial package from the official, SHA-256-pinned X.Org release.
