# SPDX-License-Identifier: Apache-2.0
Name:           liblqr
Version:        0.4.3
Release:        1%{?dist}
Summary:        Seam-carving library for content-aware image resizing
License:        LGPL-3.0-only
URL:            https://liblqr.wikidot.com/
Source0:        liblqr-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
liblqr is a C library for content-aware image resizing using seam carving.
It accepts pixel buffers and exposes a C API for controlling the resizing.

%package devel
Summary:        Development files for liblqr
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconf-pkg-config

%description devel
Public C headers, pkg-config metadata, manual pages, and the unversioned
library link for applications that use liblqr.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-install-man
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/liblqr-1.la

%check
cat > resize-check.c <<'EOF'
#include <lqr.h>
#include <glib.h>

int main(void) {
    guchar *pixels = g_malloc0(8 * 8 * 3);
    LqrCarver *carver;
    int result = 0;
    for (int i = 0; i < 8 * 8 * 3; ++i) pixels[i] = (guchar)i;
    carver = lqr_carver_new(pixels, 8, 8, 3);
    if (carver == NULL) { g_free(pixels); return 1; }
    if (lqr_carver_init(carver, 1, 0.0f) != LQR_OK) result = 2;
    if (result == 0 && lqr_carver_resize(carver, 7, 8) != LQR_OK) result = 3;
    if (result == 0 && (lqr_carver_get_width(carver) != 7 ||
                        lqr_carver_get_height(carver) != 8)) result = 4;
    lqr_carver_destroy(carver);
    return result;
}
EOF
%{__cc} %{optflags} -std=c99 -I. -Ilqr $(pkg-config --cflags glib-2.0) \
  resize-check.c -Llqr/.libs -llqr-1 $(pkg-config --libs glib-2.0) \
  %{build_ldflags} -o resize-check
LD_LIBRARY_PATH="$PWD/lqr/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  ./resize-check

%files
%license COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/liblqr-1.so.0*

%files devel
%license COPYING.LESSER
%{_includedir}/lqr-1/
%{_libdir}/liblqr-1.so
%{_libdir}/pkgconfig/lqr-1.pc
%{_mandir}/man3/*.3*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.3-1
- Initial openEuler RISC-V package from the official LGPL-licensed tag.
