# SPDX-License-Identifier: Apache-2.0
# Upstream defaults to a static archive, without a standalone debuginfo payload.
%global debug_package %{nil}
Name:           libtmx
Version:        1.10.1
Release:        1%{?dist}
Summary:        Portable C loader for Tiled TMX maps
License:        BSD-2-Clause
URL:            https://github.com/baylej/tmx
Source0:        libtmx-1.10.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  python3
Requires:       gcc
Requires:       gcc-c++
Requires:       make
Requires:       cmake
Requires:       pkgconf
Requires:       zlib-devel
Requires:       libxml2-devel
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Portable C loader for Tiled TMX maps, including the default static library,
public header and original CMake exports. Zlib support remains enabled.
Includes unchanged upstream examples/fixtures and offline installed tests.

%prep
%setup -q -n tmx-b671187d51a5616b80774c94650a360ce48a872f

%build
# Preserve upstream defaults: static, zlib ON, zstd and Sphinx docs OFF.
# Keep distribution optimization/debug flags even for the static-only package.
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_C_FLAGS_RELEASE="%{optflags}"
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libtmx/data
install -m 0644 examples/dumper/dumper.c examples/dumper/CMakeLists.txt %{buildroot}%{_datadir}/libtmx/
install -m 0644 examples/data/* %{buildroot}%{_datadir}/libtmx/data/
cat > %{buildroot}%{_datadir}/libtmx/test.cpp <<'CPP'
#include <tmx.h>
int main(void) { tmx_map* map = tmx_load("map.tmx"); return 0; }
CPP
cat > %{buildroot}%{_datadir}/libtmx/consumer.c <<'C'
#include <tmx.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int reader(void *f, char *buffer, int len) {
    size_t n = fread(buffer, 1, (size_t)len, (FILE *)f);
    return ferror((FILE *)f) ? -1 : (int)n;
}
static char *read_file(const char *name, int *length) {
    FILE *f = fopen(name, "rb");
    assert(f && fseek(f, 0, SEEK_END) == 0);
    long n = ftell(f);
    assert(n > 0 && n < 1000000 && fseek(f, 0, SEEK_SET) == 0);
    char *data = malloc((size_t)n);
    assert(data && fread(data, 1, (size_t)n, f) == (size_t)n);
    assert(fclose(f) == 0);
    *length = (int)n;
    return data;
}
static tmx_layer *verify_map(tmx_map *map) {
    assert(map && map->width == 28 && map->height == 18);
    assert(map->tile_width == 32 && map->tile_height == 32 && map->orient == O_ORT);
    tmx_layer *layer = tmx_find_layer_by_id(map, 3);
    assert(layer && layer->type == L_LAYER && layer->content.gids);
    assert(tmx_find_layer_by_name(map, "Layer") == layer);
    assert(layer->content.gids[0] == 5 && layer->content.gids[1] == 3);
    assert(layer->content.gids[503] == 5);
    tmx_property *p = tmx_get_property(map->properties, "bool_true");
    assert(p && p->type == PT_BOOL && p->value.boolean == 1);
    p = tmx_get_property(map->properties, "xml");
    assert(p && p->type == PT_STRING && !strcmp(p->value.string, "libxml2"));
    tmx_tileset_list *ts = tmx_find_tileset_by_name(map, "base");
    assert(ts && ts->firstgid == 1 && ts->tileset && ts->tileset->tilecount == 9);
    assert(map->tilecount == 10 && map->tiles && map->tiles[1]);
    tmx_object *text = tmx_find_object_by_id(map, 5);
    assert(text && text->obj_type == OT_TEXT && text->content.text);
    assert(!strcmp(text->content.text->text, "Hello World"));
    return layer;
}
int main(void) {
    tmx_map *maps[5];
    int len;
    char *data = read_file("b64zlib.tmx", &len);
    maps[0] = tmx_load("b64zlib.tmx");
    maps[1] = tmx_load_buffer(data, len);
    int fd = open("b64zlib.tmx", O_RDONLY);
    assert(fd >= 0);
    maps[2] = tmx_load_fd(fd);
    assert(close(fd) == 0);
    FILE *f = fopen("b64zlib.tmx", "rb");
    assert(f);
    maps[3] = tmx_load_callback(reader, f);
    assert(fclose(f) == 0);
    maps[4] = tmx_load("csv.tmx");
    free(data);
    tmx_layer *reference = verify_map(maps[0]);
    for (int i = 1; i < 5; ++i) {
        tmx_layer *layer = verify_map(maps[i]);
        assert(!memcmp(reference->content.gids, layer->content.gids, 504 * sizeof(uint32_t)));
    }
    for (int i = 0; i < 5; ++i) tmx_map_free(maps[i]);

    tmx_resource_manager *manager = tmx_make_resource_manager();
    assert(manager && tmx_load_tileset(manager, "tileset.tsx") == 1);
    assert(tmx_load_template(manager, "pointtemplate.tx") == 1);
    assert(tmx_load_template(manager, "tiletemplate.tx") == 1);
    tmx_map *objects = tmx_rcmgr_load(manager, "objecttemplates.tmx");
    verify_map(objects);
    tmx_object *point = tmx_find_object_by_id(objects, 12);
    tmx_object *tile = tmx_find_object_by_id(objects, 7);
    assert(point && point->obj_type == OT_POINT && point->template_ref);
    assert(tile && tile->obj_type == OT_TILE && tile->template_ref);
    tmx_map_free(objects);
    tmx_free_resource_manager(manager);
    tmx_col_bytes color = tmx_col_to_bytes(0x80402010);
    assert(color.a == 128 && color.r == 64 && color.g == 32 && color.b == 16);
    assert(tmx_load_buffer("<not-map/>", 10) == NULL);
    assert(tmx_errno != E_NONE && tmx_strerr() && *tmx_strerr());
    puts("PASS downstream map-load-apis=4 maps=6 compared-gids=2016 templates=2 colors=1 invalid-inputs=1 skips=0");
    return 0;
}
C
cat > %{buildroot}%{_datadir}/libtmx/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
base="$root/usr/share/libtmx"
(cd "$base"; sha256sum -c SHA256SUMS)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
mkdir "$work/dumper"
cp "$base/dumper.c" "$base/CMakeLists.txt" "$work/dumper/"
# Rebuild the unchanged upstream CMake consumer against the installed export.
cmake -S "$work/dumper" -B "$work/build" -Dtmx_DIR="$root/usr/lib/cmake/tmx" -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS_RELEASE='-O2 -UNDEBUG'
cmake --build "$work/build" --parallel 2
(
  cd "$base/data"
  # These are the two complete original upstream CI command lines.
  "$work/build/dumper" b64zlib.tmx > "$work/upstream-map.log"
  "$work/build/dumper" --use-rc-mgr --fd tileset.tsx --callback pointtemplate.tx --buffer tiletemplate.tx objecttemplates.tmx > "$work/upstream-resources.log"
)
cat "$work/upstream-map.log" "$work/upstream-resources.log"
for log in "$work/upstream-map.log" "$work/upstream-resources.log"; do
  grep -q 'height=18' "$log"
  grep -q 'width=28' "$log"
  grep -q "text='Hello World'" "$log"
done
# Preserve the original C++ header compilation check; do not execute its dummy path.
c++ -I"$root/usr/include" -c "$base/test.cpp" -o "$work/header.o"
read -r -a cflags <<< "$(pkgconf --cflags libxml-2.0 zlib)"
read -r -a libs <<< "$(pkgconf --libs libxml-2.0 zlib)"
gcc -std=c99 -O2 -UNDEBUG -I"$root/usr/include" "${cflags[@]}" "$base/consumer.c" "$root/usr/lib64/libtmx.a" "${libs[@]}" -o "$work/consumer"
(cd "$base/data"; "$work/consumer")
printf 'PASS upstream-ci-dumper-commands=2 cpp-compile=1 downstream-consumers=1 skips=0\n'
SH
chmod 0755 %{buildroot}%{_datadir}/libtmx/run-tests.sh
(cd %{buildroot}%{_datadir}/libtmx; sha256sum dumper.c CMakeLists.txt test.cpp consumer.c data/*) > %{buildroot}%{_datadir}/libtmx/SHA256SUMS

%check
# Upstream defines no CTest suite: retain its actual CI behavioral checks.
bash %{buildroot}%{_datadir}/libtmx/run-tests.sh "%{buildroot}"

%files
%license COPYING
%doc README.md
%{_libdir}/libtmx.a
%{_includedir}/tmx.h
# This literal upstream CMake configuration location is intentionally preserved.
%{_prefix}/lib/cmake/tmx/
%{_datadir}/libtmx/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.1-1
- Preserve default static/zlib build, CMake exports and complete upstream CI checks.
