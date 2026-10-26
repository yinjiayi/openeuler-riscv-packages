# SPDX-License-Identifier: ISC
Name:           libroxml
Version:        3.0.2
Release:        2%{?dist}
Summary:        Small C XML parser with XPath and editing support
License:        LicenseRef-libroxml-LGPL-2.1-or-later-static-linking-exception AND GPL-2.0-or-later AND ISC
URL:            https://libroxml.net/
Source0:        https://api.github.com/repos/blunderer/libroxml/tarball/refs/tags/3.0.2#/libroxml-3.0.2.tar.gz
Source1:        https://raw.githubusercontent.com/gcc-mirror/gcc/c9cd41fba9ebd288c4f101e4b99da934bcb96a11/COPYING#/gpl-2.0.txt
Patch0:         0001-declare-shared-state-extern.patch
BuildRequires:  bash binutils coreutils diffutils findutils gawk gcc glibc-devel grep make sed tar gzip autoconf automake libtool pkgconf-pkg-config
Requires:       bash binutils coreutils diffutils gawk grep

%description
libroxml is a C XML library with XPath, read/write tree operations, roxml and
rocat tools. This recipe preserves its ordinary autotools default configuration.

%prep
%setup -q -n blunderer-libroxml-ec1f915
# Snapshot all 82 originals BEFORE the package-local patch and autoreconf.
# Verified archive members contain no control characters/newlines/unsafe paths.
find . -type f -print | LC_ALL=C sort > ../libroxml-original-members.list
test "$(wc -l < ../libroxml-original-members.list)" -eq 82
mkdir source-notices
while IFS= read -r original; do
    relative=${original#./}
    destination="source-notices/$relative.notice"
    mkdir -p "$(dirname "$destination")"
    cp -p "$original" "$destination"
done < ../libroxml-original-members.list
( cd source-notices
  find . -type f -print | LC_ALL=C sort | while IFS= read -r notice; do sha256sum "$notice"; done
) > ../libroxml-original-SHA256SUMS
cp ../libroxml-original-SHA256SUMS source-notices/SHA256SUMS
cp -p %{SOURCE1} gpl-2.0.txt
%autopatch -p1
cat > api-smoke.c <<'LIBROXML_API_EOF'
/* Copyright (c) 2026 openEuler RISC-V packaging contributors.
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <roxml.h>

static node_t *(*volatile load_buffer)(char *) = roxml_load_buf;
static node_t *(*volatile child)(node_t *, char *, int) = roxml_get_chld;
static char *(*volatile name_of)(node_t *, char *, int) = roxml_get_name;
static char *(*volatile content_of)(node_t *, char *, int, int *) = roxml_get_content;
static node_t **(*volatile query)(node_t *, char *, int *) = roxml_xpath;
static void (*volatile close_doc)(node_t *) = roxml_close;

int main(void)
{
    char xml[] = "<root><item id=\"a\">alpha</item><item id=\"b\">beta</item></root>";
    char root_name[] = "root", item_name[] = "item", attr_name[] = "id";
    char buffer[128];
    int length = 0;
    node_t *doc = load_buffer(xml);
    assert(doc != NULL);
    assert(name_of(doc, buffer, sizeof buffer) == buffer);
    assert(strcmp(buffer, "documentRoot") == 0);
    node_t *root = child(doc, root_name, 0);
    assert(root != NULL && roxml_get_chld_nb(root) == 2);
    assert(name_of(root, buffer, sizeof buffer) == buffer);
    assert(strcmp(buffer, "root") == 0);
    puts("ok 1 parse-navigation");

    node_t *first = child(root, item_name, 0);
    /* A non-NULL name selects by name; nth applies to a NULL-name lookup. */
    node_t *second = child(root, NULL, 1);
    assert(first && second && first != second);
    assert(content_of(first, buffer, sizeof buffer, &length) == buffer);
    assert(strcmp(buffer, "alpha") == 0 && length == 6);
    node_t *attr = roxml_get_attr(second, attr_name, 0);
    assert(attr != NULL);
    assert(content_of(attr, buffer, sizeof buffer, &length) == buffer);
    assert(strcmp(buffer, "b") == 0 && length == 2);
    puts("ok 2 content-attribute");

    char xpath[] = "/root/item[@id='b']";
    int count = -1;
    node_t **answer = query(doc, xpath, &count);
    assert(answer != NULL && count == 1 && answer[0] == second);
    roxml_release(answer);
    puts("ok 3 xpath-ownership");
    close_doc(doc);

    char new_root_name[] = "root", new_item_name[] = "item", text[] = "value";
    node_t *created = roxml_add_node(NULL, 0, ROXML_ELM_NODE, new_root_name, NULL);
    assert(created != NULL);
    node_t *inserted = roxml_add_node(created, 0, ROXML_ELM_NODE, new_item_name, text);
    assert(inserted != NULL);
    char *serialized = NULL;
    static const char expected[] = "<root><item>value</item></root>";
    int bytes = roxml_commit_buffer(created, &serialized, 0);
    assert(serialized != NULL && bytes == (int)strlen(expected));
    assert(memcmp(serialized, expected, sizeof expected) == 0);
    puts("ok 4 edit-serialize");

    char filename[] = "./libroxml-api-XXXXXX";
    int fd = mkstemp(filename);
    assert(fd >= 0);
    size_t offset = 0;
    while (offset < (size_t)bytes) {
        ssize_t written = write(fd, serialized + offset, (size_t)bytes - offset);
        assert(written > 0);
        offset += (size_t)written;
    }
    assert(close(fd) == 0);
    doc = roxml_load_doc(filename);
    assert(doc != NULL);
    root = child(doc, root_name, 0);
    assert(root != NULL);
    first = child(root, item_name, 0);
    assert(first != NULL);
    assert(content_of(first, buffer, sizeof buffer, &length) == buffer);
    assert(strcmp(buffer, "value") == 0 && length == 6);
    close_doc(doc);
    assert(unlink(filename) == 0);
    free(serialized);
    close_doc(created);
    puts("ok 5 file-roundtrip");

    assert(name_of(NULL, buffer, sizeof buffer) == NULL);
    assert(content_of(NULL, buffer, sizeof buffer, &length) == NULL);
    assert(child(NULL, NULL, 0) == NULL);
    assert(roxml_commit_buffer(NULL, NULL, 0) == 0);
    puts("ok 6 null-boundaries");
    puts("libroxml API: 6/6 passed");
    return 0;
}
LIBROXML_API_EOF

%build
# Official Git tag has no generated configure; use upstream's own bootstrap.
sh ./autogen.sh
%configure
%make_build
gcc %{optflags} -UNDEBUG api-smoke.c -Isrc -L.libs -lroxml %{build_ldflags} -o api-smoke

%install
%make_install
install -D -m0755 api-smoke %{buildroot}%{_libexecdir}/libroxml/api-smoke
install -D -m0644 api-smoke.c %{buildroot}%{_datadir}/libroxml-tests/api-smoke.c
install -d %{buildroot}%{_datadir}/libroxml-tests/original
cp -p unittest/roxml.test.xml* %{buildroot}%{_datadir}/libroxml-tests/original/

%check
# Original default make check registers no runtime tests; preserve it unchanged.
%make_build check
( cd source-notices; sha256sum -c SHA256SUMS )
# Same original source tree ensures configure's relative unittest source probe
# and every original fixture path work. Default artifacts are already installed;
# this opt-in QA configuration does not replace/disable the shipped defaults.
%configure --enable-tests
%make_build
for program in roxml.unitC roxml.tiny.unitC roxml.perf roxml.mem; do test -x "unittest/$program"; done
for program in roxml.unitC roxml.tiny.unitC; do
    # Original runner --list deliberately returns34, not0.
    # Suspend RPM shell tracing BEFORE redirection; retain real program stderr.
    set +x
    if (cd unittest; "./$program" --list) >"$program.list" 2>"$program.list.err"; then
        status=0
    else
        status=$?
    fi
    set -x
    cat "$program.list"; cat "$program.list.err" >&2
    test "$status" -eq 34
    test "$(wc -l < "$program.list")" -eq 34
    test ! -s "$program.list.err"
    set +x
    if (cd unittest; "./$program") >"$program.log" 2>"$program.err"; then
        status=0
    else
        status=$?
    fi
    set -x
    cat "$program.log"; cat "$program.err" >&2
    if test "$status" -ne 0; then exit "$status"; fi
    test ! -s "$program.err"
    test "$(grep -c '^OK:' "$program.log")" -eq 34
    if grep -E '^(ERROR|FAILED)' "$program.log"; then exit 1; fi
    printf 'original %s: 34/34 passed\n' "$program"
done
mkdir -p api-work
set +x
if (cd api-work; LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}%{_libexecdir}/libroxml/api-smoke) > api.log 2>api.err; then
    status=0
else
    status=$?
fi
set -x
cat api.log; cat api.err >&2
if test "$status" -ne 0; then exit "$status"; fi
test ! -s api.err
cat > api.expected <<'LIBROXML_EXPECTED_EOF'
ok 1 parse-navigation
ok 2 content-attribute
ok 3 xpath-ownership
ok 4 edit-serialize
ok 5 file-roundtrip
ok 6 null-boundaries
libroxml API: 6/6 passed
LIBROXML_EXPECTED_EOF
cmp api.expected api.log
# RPM install-post stripping has already completed before %check: bind final
# installed driver bytes, source and all original installed fixture bytes.
(cd %{buildroot}; sha256sum ./usr/libexec/libroxml/api-smoke ./usr/share/libroxml-tests/api-smoke.c ./usr/share/libroxml-tests/original/*) > %{buildroot}%{_datadir}/libroxml-tests/SHA256SUMS

%files
%license License.txt gpl-2.0.txt source-notices
%doc debian/README
%{_bindir}/roxml
%{_bindir}/rocat
%{_libdir}/libroxml.so.0.0.0
%{_libdir}/libroxml.so.0
%{_libdir}/libroxml.so
%{_libdir}/libroxml.a
%{_libdir}/libroxml.la
%{_includedir}/roxml.h
%{_libdir}/pkgconfig/libroxml.pc
%{_libexecdir}/libroxml
%{_datadir}/libroxml-tests

%changelog
* Mon Oct 26 2026 openEuler RISC-V packaging contributors - 3.0.2-2
- Isolate program stderr from RPM shell xtrace without weakening QA gates.

* Mon Oct 26 2026 openEuler RISC-V packaging contributors - 3.0.2-1
- Preserve autotools defaults and original optional normal/tiny test suites.
- Declare shared state extern for modern GCC without relaxing -fno-common.
