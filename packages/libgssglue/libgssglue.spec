# SPDX-License-Identifier: Apache-2.0
Name:           libgssglue
Version:        0.9
Release:        1%{?dist}
Summary:        Multi-mechanism GSS-API glue library
License:        BSD-3-Clause AND HPND-sell-variant AND HPND-export-US-modify AND X11 AND FSFAP AND FSFUL AND LicenseRef-GNU-build-helper-exceptions AND MIT
URL:            https://gitlab.com/gsasl/libgssglue
Source0:        libgssglue-0.9.tar.gz
Source1:        gpl-2.0.txt
Source2:        gpl-3.0.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  krb5-libs
Requires:       bash
Requires:       coreutils
Requires:       krb5-libs

%description
A multi-mechanism GSS-API glue library with the original MIT Kerberos backend
configuration. Preserve default shared/static libraries and the unchanged
original generic test. Additional local API checks make no authentication,
credential, privileged-operation, security-certification or timing claim.

%prep
%autosetup -n libgssglue-0.9 -p1
# Preserve all 79 original members before configure regenerates anything.
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r original; do
    mkdir -p "license-notices/${original%/*}"
    cp -p "$original" "license-notices/$original.notice"
done
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
cp -p %{SOURCE2} license-notices/GPL-3.0.txt
(cd license-notices; find . -type f -exec sha256sum {} + | LC_ALL=C sort) > notice-checksums
cp notice-checksums license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
test "$(find license-notices -type f | wc -l)" -eq 82
cat > api-smoke.c <<'LIBGSSGLUE_API_EOF'
/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 openEuler RISC-V package contributors.
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the Software),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 * Independent package regression driver; not an authentication/security test.
 */
#include <gssapi/gssapi.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    OM_uint32 minor = 0;
    gss_OID_set set = GSS_C_NO_OID_SET;
    unsigned char encoded[] = {0x2a, 0x03};
    gss_OID_desc oid = {sizeof(encoded), encoded};
    int present = -1, equal = -1;
    gss_name_t original = GSS_C_NO_NAME, duplicate = GSS_C_NO_NAME;
    char name[] = "oe-rva23-local-user";
    gss_buffer_desc input = {sizeof(name) - 1, name};
    gss_buffer_desc display = GSS_C_EMPTY_BUFFER;

    assert(gss_create_empty_oid_set(&minor, &set) == GSS_S_COMPLETE);
    assert(set != GSS_C_NO_OID_SET && set->count == 0);
    puts("PASS: empty OID set");
    assert(gss_add_oid_set_member(&minor, &oid, &set) == GSS_S_COMPLETE);
    assert(gss_test_oid_set_member(&minor, &oid, set, &present) == GSS_S_COMPLETE);
    assert(present == 1 && set->count == 1);
    assert(gss_release_oid_set(&minor, &set) == GSS_S_COMPLETE);
    assert(set == GSS_C_NO_OID_SET);
    puts("PASS: custom OID membership and ownership");

    /* Unregistered private test name type: exercise generic union-name
       ownership without Kerberos realm/DNS or credentials. */
    assert(gss_import_name(&minor, &input, &oid, &original) == GSS_S_COMPLETE);
    assert(gss_display_name(&minor, original, &display, NULL) == GSS_S_COMPLETE);
    assert(display.length == input.length && memcmp(display.value, name, input.length) == 0);
    assert(gss_release_buffer(&minor, &display) == GSS_S_COMPLETE);
    assert(display.length == 0 && display.value == NULL);
    puts("PASS: local name import and exact display");
    assert(gss_duplicate_name(&minor, original, &duplicate) == GSS_S_COMPLETE);
    assert(gss_compare_name(&minor, original, duplicate, &equal) == GSS_S_COMPLETE && equal == 1);
    assert(gss_release_name(&minor, &original) == GSS_S_COMPLETE && original == GSS_C_NO_NAME);
    assert(gss_display_name(&minor, duplicate, &display, NULL) == GSS_S_COMPLETE);
    assert(display.length == input.length && memcmp(display.value, name, input.length) == 0);
    assert(gss_release_buffer(&minor, &display) == GSS_S_COMPLETE);
    assert(gss_release_name(&minor, &duplicate) == GSS_S_COMPLETE && duplicate == GSS_C_NO_NAME);
    puts("PASS: independent duplicate name lifetime");
    assert(gss_import_name(&minor, GSS_C_NO_BUFFER, &oid, &original) == GSS_S_BAD_NAME);
    assert(original == GSS_C_NO_NAME);
    assert(gss_import_name(NULL, &input, &oid, &original) == GSS_S_CALL_INACCESSIBLE_WRITE);
    puts("PASS: exact invalid-input status");
    assert(gss_indicate_mechs(&minor, &set) == GSS_S_COMPLETE);
    assert(set != GSS_C_NO_OID_SET && set->count >= 1);
    assert(gss_release_oid_set(&minor, &set) == GSS_S_COMPLETE && set == GSS_C_NO_OID_SET);
    puts("PASS: configured local mechanism discovery");
    puts("libgssglue API cases: 6/6");
    return 0;
}
LIBGSSGLUE_API_EOF

%build
# Do not disable shared/static libraries or default linker-script detection.
%configure
%make_build
gcc %{optflags} -UNDEBUG -Isrc/gssglue api-smoke.c -Lsrc/.libs -lgssglue -ldl -o api-smoke
# Separate installed replay uses the unchanged original test, without a
# build-tree libtool wrapper or build-directory RPATH.
gcc %{optflags} -Isrc/gssglue tests/generic.c -Lsrc/.libs -lgssglue -ldl -o original-generic

%install
%make_install
rm -f %{buildroot}%{_libdir}/libgssglue.la
install -Dpm0644 doc/gssapi_mech.conf %{buildroot}%{_sysconfdir}/gssapi_mech.conf
install -Dpm0755 api-smoke %{buildroot}%{_libexecdir}/libgssglue-tests/api-smoke
install -Dpm0755 original-generic %{buildroot}%{_libexecdir}/libgssglue-tests/generic
install -Dpm0644 api-smoke.c %{buildroot}%{_libexecdir}/libgssglue-tests/api-smoke.c

%check
export GSSAPI_MECH_CONF="$PWD/doc/gssapi_mech.conf"
# The original Automake TESTS=generic entry point is retained byte-for-byte.
make check
test -f src/.libs/libgssglue.a
test -f src/.libs/libgssglue.so.1.0.0
(cd license-notices; sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD/src/.libs" ./api-smoke
# Bind packaged driver bytes after install-post stripping.
(cd %{buildroot}%{_libexecdir}/libgssglue-tests; sha256sum api-smoke api-smoke.c generic > SHA256SUMS)

%files
%license COPYING license-notices
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/gssapi_mech.conf
%{_includedir}/gssglue
%{_libdir}/libgssglue.so*
%{_libdir}/libgssglue.a
%{_libdir}/pkgconfig/libgssglue.pc
%{_libexecdir}/libgssglue-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9-1
- Preserve original defaults, generic test and all 79 original source notices.
- Add six local API regressions and strict installed same-file bindings.
