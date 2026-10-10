# SPDX-License-Identifier: Apache-2.0
Name:           libiptcdata
Version:        1.0.5
Release:        1%{?dist}
Summary:        IPTC metadata parsing and editing library
License:        LGPL-2.0-or-later
URL:            https://github.com/ianw/libiptcdata
Source0:        libiptcdata-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libiptcdata reads and writes International Press Telecommunications Council
metadata, including IPTC records embedded in JPEG images. The iptc command
provides an interface for viewing and editing that metadata.

%package devel
Summary:        Development files for libiptcdata
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, unversioned linker name, and pkg-config metadata for
applications using libiptcdata.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-python --disable-gtk-doc
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
%find_lang libiptcdata
%find_lang iptc
cat iptc.lang >> libiptcdata.lang

%check
# The release does not register a library test program. Retain its check
# target and prove a complete IPTC caption encode/decode round trip.
%make_build check
./iptc/iptc --version | grep -F 'iptc %{version}'
./iptc/iptc --list | grep -F 'Caption'
cat > iptc-roundtrip.c <<'EOF'
#include <libiptcdata/iptc-data.h>
#include <string.h>

int main(void) {
    static const unsigned char caption[] = "riscv";
    IptcData *original = iptc_data_new();
    IptcData *parsed;
    IptcDataSet *dataset;
    unsigned char *encoded = 0;
    unsigned int size = 0;
    int ok;
    if (!original) return 1;
    if (iptc_data_add_dataset_with_contents(original, IPTC_RECORD_APP_2,
            IPTC_TAG_CAPTION, caption, sizeof(caption) - 1,
            IPTC_VALIDATE) != (int)(sizeof(caption) - 1)) return 2;
    if (iptc_data_save(original, &encoded, &size) != 0 || !encoded || !size)
        return 3;
    parsed = iptc_data_new_from_data(encoded, size);
    if (!parsed) return 4;
    dataset = iptc_data_get_dataset(parsed, IPTC_RECORD_APP_2,
                                    IPTC_TAG_CAPTION);
    ok = dataset && dataset->size == sizeof(caption) - 1 &&
         memcmp(dataset->data, caption, sizeof(caption) - 1) == 0;
    if (dataset) iptc_dataset_unref(dataset);
    iptc_data_unref(parsed);
    iptc_data_free_buf(original, encoded);
    iptc_data_unref(original);
    return ok ? 0 : 5;
}
EOF
gcc %{optflags} -I. -Ilibiptcdata iptc-roundtrip.c \
  -Llibiptcdata/.libs -Wl,-rpath,$PWD/libiptcdata/.libs \
  -liptcdata -o iptc-roundtrip
./iptc-roundtrip

%files -f libiptcdata.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libiptcdata.so.0*
%{_bindir}/iptc

%files devel
%license COPYING
%{_includedir}/libiptcdata/
%{_libdir}/libiptcdata.so
%{_libdir}/pkgconfig/libiptcdata.pc
%{_datadir}/gtk-doc/html/libiptcdata/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package with IPTC metadata round-trip tests.
