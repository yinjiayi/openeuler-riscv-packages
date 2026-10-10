# SPDX-License-Identifier: Apache-2.0
Name:           libart-lgpl
Version:        2.3.21
Release:        1%{?dist}
Summary:        LGPL 2D graphics primitives
License:        LGPL-2.0-or-later
URL:            https://levien.com/libart/
Source0:        libart_lgpl-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make

%description
Libart provides fast 2D graphics primitives, including affine transforms,
paths, rasterization, and alpha compositing.

%package devel
Summary:        Development files for libart-lgpl
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and link-time libraries for libart-lgpl.

%prep
%autosetup -n libart_lgpl-%{version} -p1

%build
%configure
%make_build

%install
%make_install

%check
# Upstream's `tests` target builds two generators but does not execute them.
# Run all five testart modes and testuta, checking each output is nonempty.
%make_build tests
test_output=$(mktemp -d)
trap 'rm -r "$test_output"' EXIT
for mode in testpat gradient dash dist intersect; do
  ./testart "$mode" > "$test_output/$mode"
  test -s "$test_output/$mode"
done
./testuta > "$test_output/testuta"
test -s "$test_output/testuta"

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libart_lgpl_2.so.2*

%files devel
%{_bindir}/libart2-config
%{_includedir}/libart-2.0/
%{_libdir}/libart_lgpl_2.so
%{_libdir}/libart_lgpl_2.a
%{_libdir}/libart_lgpl_2.la
%{_libdir}/pkgconfig/libart-2.0.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.21-1
- Package the official SHA-256-pinned GNOME Libart 2.3.21 release.
