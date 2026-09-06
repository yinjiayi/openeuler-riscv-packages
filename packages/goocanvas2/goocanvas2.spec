# SPDX-License-Identifier: Apache-2.0
Name:           goocanvas2
Version:        2.0.4
Release:        1%{?dist}
Summary:        Cairo canvas widget library for GTK 3
License:        LGPL-2.0-only
URL:            https://gitlab.gnome.org/GNOME/goocanvas
Source0:        goocanvas-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(cairo) >= 1.10.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:  pkgconfig(pygobject-3.0) >= 2.90.4
BuildRequires:  python3
BuildRequires:  python3-gobject

%description
GooCanvas is a Cairo-based canvas widget for GTK 3. It provides canvas items,
model/view support, affine transformations, accessibility, scrolling,
zooming, printing, and GObject introspection for applications that use the
stable 2.x API.

%package devel
Summary:        Development files for GooCanvas 2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned linker name, pkg-config metadata, and GObject
introspection metadata for developing applications with GooCanvas 2.

%package -n python3-goocanvas2
Summary:        Python 3 overrides for GooCanvas 2
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-gobject

%description -n python3-goocanvas2
Python 3 PyGObject overrides for the GooCanvas 2 introspection interface.

%prep
%autosetup -n goocanvas-%{version} -p1

%build
%configure \
  --disable-gtk-doc \
  --disable-rebuilds \
  --disable-static \
  --enable-introspection \
  --enable-python
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%find_lang goocanvas2

%check
# Upstream's released tree only registers gtk-doc consistency checks when API
# documentation regeneration is enabled. Retain its check target, then compile
# and execute a display-independent probe against the exported 2.x C ABI.
%make_build check
cat > goocanvas2-abi-check.c <<'EOF'
#include <goocanvas.h>
#include <glib-object.h>
int main(void) {
  GType canvas_type = goo_canvas_get_type();
  return canvas_type == G_TYPE_INVALID ? 1 : 0;
}
EOF
%{__cc} %{build_cflags} \
  -I"$PWD/src" \
  $(pkg-config --cflags gtk+-3.0 cairo) \
  goocanvas2-abi-check.c \
  -L"$PWD/src/.libs" -Wl,-rpath,"$PWD/src/.libs" -lgoocanvas-2.0 \
  $(pkg-config --libs gtk+-3.0 cairo) \
  %{build_ldflags} -o goocanvas2-abi-check
./goocanvas2-abi-check

%files -f goocanvas2.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README TODO
%{_libdir}/libgoocanvas-2.0.so.9*
%{_libdir}/girepository-1.0/GooCanvas-2.0.typelib

%files devel
%{_includedir}/goocanvas-2.0/
%{_libdir}/libgoocanvas-2.0.so
%{_libdir}/pkgconfig/goocanvas-2.0.pc
%{_datadir}/gir-1.0/GooCanvas-2.0.gir

%files -n python3-goocanvas2
%{python3_sitearch}/gi/overrides/GooCanvas.py
%{python3_sitearch}/gi/overrides/__pycache__/GooCanvas.*

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.4-1
- Initial openEuler RISC-V package for the complete GooCanvas 2 compatibility ABI.
