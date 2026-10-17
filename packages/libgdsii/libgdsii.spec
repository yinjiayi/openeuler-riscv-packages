# SPDX-License-Identifier: Apache-2.0
Name:           libgdsii
Version:        0.21
Release:        1%{?dist}
Summary:        C++ library and converter for GDSII geometry files
License:        GPL-2.0-or-later
URL:            https://github.com/HomerReid/libGDSII
Source0:        libgdsii-0.21.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  glibc-common
Requires:       gcc-c++
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       grep
Requires:       glibc-common
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Read and flatten GDSII geometry files through a C++ library, or convert them
to textual and GMSH forms using GDSIIConvert. Preserve the configured shared
and static libraries, public header, libtool archive and original example data.

%prep
%setup -q -n libGDSII-a6f6f2de4894075ed1bcf70d0542122781856c4e
# Never dereference the two machine-specific absolute documentation links.
test -L COPYING
test "$(readlink COPYING)" = /usr/share/automake-1.15/COPYING
test -L INSTALL
test "$(readlink INSTALL)" = /home/homer/codes/anaconda3/envs/hrpy36/share/automake-1.16/INSTALL
rm -- COPYING INSTALL
cp -p LICENSE COPYING
touch ChangeLog
mkdir -p m4
# Default copy mode, not upstream autogen.sh's repeated --symlink invocations.
autoreconf --force --install --verbose
test -f INSTALL
test ! -L INSTALL
cmp LICENSE COPYING

%build
# Preserve all features selected by the target's standard configure macro.
%configure
%make_build

%install
%make_install
# Keep the original generated Version 0.1 from AC_INIT, not the tag version.
install -D -m 0644 libGDSII-pkgconfig %{buildroot}%{_libdir}/pkgconfig/libGDSII.pc
install -D -m 0644 lib/libGDSII.h %{buildroot}%{_datadir}/libgdsii/tests/libGDSII.h
(cd lib; sha256sum libGDSII.h) > %{buildroot}%{_datadir}/libgdsii/tests/SHA256SUMS
cat > %{buildroot}%{_datadir}/libgdsii/tests/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
test "$#" -le 1
root=${1:-}
prefix="$root/usr"
base="$prefix/share/libgdsii/tests"
fixture="$prefix/share/libGDSII/examples/bend-flux/bend-flux.gds"
unset LIBGDSII_LENGTH_UNIT LD_PRELOAD LD_LIBRARY_PATH
if test -n "$root"; then
  # A staged buildroot is not installed in the system loader's search path.
  export LD_LIBRARY_PATH="$prefix/lib64"
fi
(cd "$base"; sha256sum -c SHA256SUMS)
cmp "$base/libGDSII.h" "$prefix/include/libGDSII.h"
echo "307abe83a64a3a285d227376e7074d6e6383bc2a2e8a0b28a5206f105ec2e768  $fixture" | sha256sum -c -
test -f "$prefix/lib64/libGDSII.a"
test -f "$prefix/lib64/libGDSII.la"
test -f "$prefix/lib64/libGDSII.so.0.0.0"
test -L "$prefix/lib64/libGDSII.so.0"
test "$(readlink "$prefix/lib64/libGDSII.so.0")" = libGDSII.so.0.0.0
test -L "$prefix/lib64/libGDSII.so"
test "$(readlink "$prefix/lib64/libGDSII.so")" = libGDSII.so.0.0.0
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cat > "$work/consumer.cpp" <<'CPP'
#include <libGDSII.h>
#include <cmath>
#include <cstring>
#include <cstdio>
static bool near(double a,double b) { return std::isfinite(a) && std::abs(a-b)<1e-6; }
int main(int argc,char** argv) {
    if(argc!=2) return 1;
    libGDSIIExists();
    libGDSII::GDSIIData data(argv[1]);
    if(data.ErrMsg || !data.LibName || *data.LibName!="LIB") return 2;
    iVec layers=data.GetLayers();
    if(layers.size()!=7) return 3;
    const unsigned sizes[7]={8,8,12,4,4,4,4};
    const double xy[7][2]={{-8000,-16000},{-8000,-12000},{-8000,-12000},
        {-7000,-12000},{-6500,-12500},{6500,-12500},{2500,14500}};
    for(int l=0;l<7;++l) {
        if(layers[l]!=l) return 4;
        PolygonList p=data.GetPolygons(l);
        if(p.size()!=1 || p[0].size()!=sizes[l]) return 5;
        for(double v:p[0]) if(!std::isfinite(v)) return 6;
        if(!near(p[0][0],xy[l][0]) || !near(p[0][1],xy[l][1])) return 7;
    }
    if(data.GetPolygons().size()!=7 || !data.GetPolygons(99).empty()) return 8;
    TextStringList texts=data.GetTextStrings();
    if(texts.size()!=1 || texts[0].Layer!=0 || std::strcmp(texts[0].Text,"Geometry")) return 9;
    if(data.GetPolygons("Geometry").size()!=1 || !data.GetPolygons("absent-label").empty()) return 10;
    dVec square={0,0,2,0,2,2,0,2};
    if(!libGDSII::PointInPolygon(square,1,1) || libGDSII::PointInPolygon(square,3,1)) return 11;
    if(libGDSII::GetLayers(argv[1])!=layers || libGDSII::GetPolygons(argv[1]).size()!=7 ||
       libGDSII::GetTextStrings(argv[1]).size()!=1) return 12;
    libGDSII::ClearGDSIICache();
    std::puts("PASS downstream layers=7 polygons-and-paths=7 text=1 cached-api=3 point-in-polygon=2 skips=0");
}
CPP
PKG_CONFIG_PATH="$prefix/lib64/pkgconfig" PKG_CONFIG_SYSROOT_DIR="$root" pkg-config --exists --exact-version=0.1 libGDSII
g++ -std=c++11 -UNDEBUG "$work/consumer.cpp" \
  $(PKG_CONFIG_PATH="$prefix/lib64/pkgconfig" PKG_CONFIG_SYSROOT_DIR="$root" pkg-config --cflags --libs libGDSII) -o "$work/consumer-pc"
ldd "$work/consumer-pc" > "$work/consumer-pc.ldd"
if test -n "$root"; then
  grep -F "libGDSII.so.0 => $prefix/lib64/libGDSII.so.0 " "$work/consumer-pc.ldd"
else
  # Installed verification must use the normal loader, never a staged override.
  grep -F -e 'libGDSII.so.0 => /usr/lib64/libGDSII.so.0 ' \
    -e 'libGDSII.so.0 => /lib64/libGDSII.so.0 ' "$work/consumer-pc.ldd"
fi
"$work/consumer-pc" "$fixture"
g++ -std=c++11 -UNDEBUG -I"$prefix/include" "$work/consumer.cpp" "$prefix/lib64/libGDSII.a" -o "$work/consumer-direct"
"$work/consumer-direct" "$fixture"
if "$prefix/bin/GDSIIConvert" > "$work/usage.log" 2>&1; then
  echo 'Expected missing-input CLI failure' >&2; exit 1
fi
grep -F 'Usage: GDSIIConvert' "$work/usage.log"
"$prefix/bin/GDSIIConvert" "$fixture" --raw --analyze --GMSH \
  --FileBase "$work/bend" --LogFile "$work/cli.log" > "$work/cli-output.log"
grep -F 'Read 60 data records' "$work/cli-output.log"
grep -F 'ENDLIB' "$work/cli-output.log"
grep -F 'Struct 0: bend-flux' "$work/cli-output.log"
grep -F 'Wrote 7 metallization polygons' "$work/cli-output.log"
test "$(grep -c '^Point(' "$work/bend.geo")" -eq 22
test "$(grep -c '^Line(' "$work/bend.geo")" -eq 18
test "$(grep -c '^Plane Surface(' "$work/bend.geo")" -eq 3
grep -F 'Geometry' "$work/bend.pp"
echo 'PASS downstream original-fixture-hash=1 installed-header-hash=1 metadata-consumers=2 cli-cases=2 gmsh-points=22 gmsh-lines=18 gmsh-surfaces=3 skips=0'
SH
chmod 0755 %{buildroot}%{_datadir}/libgdsii/tests/run-tests.sh

%check
# No registered upstream TESTS/check_PROGRAMS; retain original default check.
%make_build check
# Explicitly additional downstream checks on staged installed bytes.
bash %{buildroot}%{_datadir}/libgdsii/tests/run-tests.sh %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE COPYRIGHT
%doc README.md AUTHORS
%{_bindir}/GDSIIConvert
%{_includedir}/libGDSII.h
%{_libdir}/libGDSII.a
%{_libdir}/libGDSII.la
%{_libdir}/libGDSII.so
%{_libdir}/libGDSII.so.0*
%{_libdir}/pkgconfig/libGDSII.pc
%{_datadir}/libGDSII/
%{_datadir}/libgdsii/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21-1
- Pin official stable source, retain defaults and safely replace stale doc links.
- Preserve make check; add original-fixture API, pkg-config and CLI consumers.
