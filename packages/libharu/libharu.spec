# SPDX-License-Identifier: Apache-2.0
Name:           libharu
Version:        2.4.6
Release:        1%{?dist}
Summary:        C library for generating PDF documents
License:        Zlib
URL:            https://github.com/libharu/libharu
Source0:        libharu-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  make
BuildRequires:  zlib-devel

%description
libHaru is a C library for generating PDF documents. It supports text,
graphics, images, and compression through libpng and zlib.

%package devel
Summary:        Development files for libHaru
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public C headers and the unversioned library link for applications that
generate PDF documents with libHaru.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DLIBHPDF_EXAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
cat > %{_vpath_builddir}/hpdf-check.c <<'EOF'
#include <hpdf.h>
#include <string.h>

int main(void) {
    HPDF_Doc pdf;
    HPDF_Page page;
    HPDF_Font font;
    HPDF_STATUS result;
    if (strcmp(HPDF_GetVersion(), "2.4.6") != 0) return 1;
    pdf = HPDF_New(NULL, NULL);
    if (pdf == NULL) return 2;
    page = HPDF_AddPage(pdf);
    if (page == NULL) return 3;
    font = HPDF_GetFont(pdf, "Helvetica", NULL);
    if (font == NULL) return 4;
    result = HPDF_Page_BeginText(page);
    if (result == HPDF_OK) result = HPDF_Page_SetFontAndSize(page, font, 12);
    if (result == HPDF_OK) result = HPDF_Page_TextOut(page, 20, 20, "riscv64 RVA23");
    if (result == HPDF_OK) result = HPDF_Page_EndText(page);
    if (result == HPDF_OK) result = HPDF_SaveToFile(pdf, "hpdf-check.pdf");
    HPDF_Free(pdf);
    return result == HPDF_OK ? 0 : 5;
}
EOF
%{__cc} %{optflags} -Iinclude -I%{_vpath_builddir}/include \
  %{_vpath_builddir}/hpdf-check.c -L%{_vpath_builddir}/src -lhpdf \
  %{build_ldflags} -o %{_vpath_builddir}/hpdf-check
LD_LIBRARY_PATH=%{_vpath_builddir}/src %{_vpath_builddir}/hpdf-check
head -c 5 hpdf-check.pdf | grep -aFx '%PDF-'
tail -c 16 hpdf-check.pdf | grep -aF '%%EOF'

%files
%license LICENSE
%{_libdir}/libhpdf.so.2*
%{_docdir}/libharu/

%files devel
%license LICENSE
%{_includedir}/hpdf*.h
%{_libdir}/libhpdf.so

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.6-1
- Initial openEuler RISC-V package from the official Zlib-licensed tag.
