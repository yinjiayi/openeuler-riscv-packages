# SPDX-License-Identifier: Apache-2.0
Name:           libecoli
Version:        0.11.8
Release:        1%{?dist}
Summary:        Extensible command line parsing library
License:        BSD-3-Clause AND LicenseRef-Public-Domain
URL:            https://github.com/rjarry/libecoli
Source0:        libecoli-0.11.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  libedit-devel
BuildRequires:  libyaml-devel
BuildRequires:  readline-devel
BuildRequires:  doxygen
BuildRequires:  doxygen2man
BuildRequires:  libxml2
BuildRequires:  graphviz
BuildRequires:  clang
BuildRequires:  python3
BuildRequires:  jq
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
Requires:       gcc
Requires:       pkgconf
Requires:       libedit-devel
Requires:       libyaml-devel
Requires:       readline-devel
Requires:       clang
Requires:       python3
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       grep

%description
Grammar graphs, parsing, completion and interactive command-line support.
Includes the default shared library, public headers, YAML and editline support,
all five examples, upstream HTML/man documentation and unchanged unit sources.

%prep
%setup -q -n libecoli-642e5a5c7224894a72ede66608a72e6fea2de39a
# Retain original copyright lines in binary distributions too.
find include src test examples doc -type f \( -name '*.c' -o -name '*.h' \) -exec grep -H 'Copyright' {} + > COPYRIGHT-NOTICES

%build
# Preserve all auto features (upstream CI enables them too), werror/assertions.
export CFLAGS="%{optflags} -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
meson setup build --prefix=%{_prefix} --libdir=lib64 --buildtype=debugoptimized --wrap-mode=nodownload --auto-features=enabled -Db_ndebug=false
ninja -C build

%install
DESTDIR=%{buildroot} meson install -C build --no-rebuild
# Complete the original shell entry point's documented installation.
install -m 0755 build/examples/parse-yaml/ecoli-parse-yaml %{buildroot}%{_bindir}/ecoli-parse-yaml
install -d %{buildroot}%{_libexecdir}/libecoli %{buildroot}%{_datadir}/libecoli/test
for demo in simple-editline pool-editline extension-editline readline; do
  install -m 0755 build/examples/$demo/ecoli-$demo %{buildroot}%{_libexecdir}/libecoli/
done
install -m 0644 libshell/libecoli.sh %{buildroot}%{_datadir}/libecoli/ecoli.sh
install -m 0644 test/*.c test/*.h %{buildroot}%{_datadir}/libecoli/test/
install -m 0644 examples/parse-yaml/test.yaml %{buildroot}%{_datadir}/libecoli/test.yaml
install -m 0644 devtools/gen_sym_check.py %{buildroot}%{_datadir}/libecoli/gen_sym_check.py
cat > %{buildroot}%{_datadir}/libecoli/consumer.c <<'C'
#include <ecoli.h>
#include <string.h>
int main(void) {
    if (ec_init() != 0) return 1;
    struct ec_node *n = ec_node_str("downstream", "hello");
    if (!n) return 2;
    struct ec_pnode *p = ec_parse(n, "hello");
    if (!p || !ec_pnode_matches(p)) return 3;
    const struct ec_strvec *v = ec_pnode_get_strvec(p);
    if (!v || ec_strvec_len(v) != 1 || strcmp(ec_strvec_val(v, 0), "hello")) return 4;
    ec_pnode_free(p);
    p = ec_parse(n, "different");
    if (!p || ec_pnode_matches(p)) return 5;
    ec_pnode_free(p);
    ec_node_free(n);
    ec_exit();
    return 0;
}
C
cat > %{buildroot}%{_datadir}/libecoli/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail
stage=initialization
trap 'status=$?; printf "FAIL downstream stage=%s line=%s exit=%s\n" "$stage" "$LINENO" "$status" >&2; exit "$status"' ERR
root=${1:-}
base="$root/usr/share/libecoli"
stage=input-integrity
printf 'BEGIN downstream stage=%s\n' "$stage"
(cd "$base"; sha256sum -c SHA256SUMS)
printf 'PASS downstream stage=%s\n' "$stage"
stage=workspace
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
export LD_LIBRARY_PATH="$root/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="$root/usr/lib64/pkgconfig"
stage=pkgconf-cflags
read -r -a cflags <<< "$(pkgconf --define-variable=prefix="$root/usr" --cflags libecoli)"
stage=pkgconf-libs
read -r -a libs <<< "$(pkgconf --define-variable=prefix="$root/usr" --libs libecoli)"
count=0
for source in "$base"/test/*.c; do
  name=$(basename "$source" .c)
  if [[ $name == test ]]; then continue; fi
  stage="unit-compile:$name"
  printf 'BEGIN downstream stage=%s\n' "$stage"
  gcc -std=gnu99 -D_GNU_SOURCE -O2 -UNDEBUG "${cflags[@]}" -I"$base/test" \
    "$source" "$base/test/test.c" "${libs[@]}" -o "$work/$name"
  stage="unit-run:$name"
  printf 'BEGIN downstream stage=%s\n' "$stage"
  "$work/$name"
  count=$((count+1))
  printf 'PASS downstream stage=%s completed=%s\n' "$stage" "$count"
done
stage=unit-count
printf 'CHECK downstream stage=%s observed=%s required=33\n' "$stage" "$count"
[[ $count == 33 ]]
stage=consumer-compile
printf 'BEGIN downstream stage=%s\n' "$stage"
gcc -std=gnu99 -D_GNU_SOURCE -O2 -UNDEBUG "${cflags[@]}" "$base/consumer.c" "${libs[@]}" -o "$work/consumer"
stage=consumer-run
printf 'BEGIN downstream stage=%s\n' "$stage"
"$work/consumer"
printf 'PASS downstream stage=%s\n' "$stage"
# The original generator ignores /usr system headers. A private copy of the
# installed headers prevents an empty, misleading public-symbol check.
stage=private-headers
printf 'BEGIN downstream stage=%s\n' "$stage"
mkdir "$work/include"
cp "$root/usr/include/ecoli.h" "$work/include/"
cp -R "$root/usr/include/ecoli" "$work/include/"
stage=symbol-generator
printf 'BEGIN downstream stage=%s\n' "$stage"
python3 "$base/gen_sym_check.py" "$work/include" > "$work/symbols.c"
stage=symbol-count
symbols=$(grep -Ec '^[[:space:]]*\(void \*\)&?ec_' "$work/symbols.c")
printf 'CHECK downstream stage=%s observed=%s required=positive\n' "$stage" "$symbols"
[[ $symbols -gt 0 ]]
stage=symbol-link
printf 'BEGIN downstream stage=%s\n' "$stage"
gcc -std=gnu99 -D_GNU_SOURCE -Wno-deprecated-declarations "${cflags[@]}" "$work/symbols.c" "${libs[@]}" -o "$work/symbols"
stage=symbol-run
printf 'BEGIN downstream stage=%s\n' "$stage"
"$work/symbols" > "$work/symbols.log"
stage=symbol-output-count
python3 - "$work/symbols.c" "$work/symbols.log" "$symbols" <<'PY'
"""Draft package-only oracle for unchanged gen_sym_check.py emitted references."""
import re

def verify_symbol_output(source, output, expected_ec_count):
    assert isinstance(expected_ec_count, int) and expected_ec_count > 0
    assert len(source) < 1000000 and len(output) < 1000000
    arrays = list(re.finditer(r'^static void \*syms\[\] = \{\n(.*?)^\};$', source, re.M | re.S))
    assert len(arrays) == 1, 'Expected exactly one original symbol array'
    refs = []
    for line in arrays[0][1].splitlines():
        match = re.fullmatch(r'[ \t]*\(void \*\)(&?)([A-Za-z][A-Za-z_0-9]*),[ \t]*', line)
        assert match is not None, 'Malformed symbol reference'
        refs.append(match[2])
    assert refs and len(refs) == len(set(refs)), 'Empty or duplicate symbol references'
    ec_count = sum(name.startswith('ec_') for name in refs)
    lines = output.splitlines()
    print(f'CHECK downstream symbol-output-count ec={ec_count} total={len(refs)} lines={len(lines)}')
    assert ec_count == expected_ec_count, 'Original nonempty ec_ reference count changed'
    assert len(lines) == len(refs), 'Printed pointer count differs from complete reference array'
    for line in lines:
        assert re.fullmatch(r'0x[0-9a-fA-F]+', line) and int(line, 16) != 0, 'Malformed or null symbol address'
    return dict(ec_references=ec_count, total_references=len(refs), printed_addresses=len(lines))

if __name__ == '__main__':
    import sys
    from pathlib import Path
    counts = verify_symbol_output(Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text(), int(sys.argv[3]))
    print(f"PASS downstream symbol-output-count ec={counts['ec_references']} total={counts['total_references']} lines={counts['printed_addresses']}")
PY
printf 'PASS downstream stage=%s symbols=%s\n' "$stage" "$symbols"
stage=cli-help
printf 'BEGIN downstream stage=%s\n' "$stage"
"$root/usr/bin/ecoli-parse-yaml" --help > "$work/help.log" 2>&1
stage=cli-help-assert
grep -q -- '--input-file' "$work/help.log"
stage=cli-completion
printf 'BEGIN downstream stage=%s\n' "$stage"
"$root/usr/bin/ecoli-parse-yaml" --complete --input-file "$base/test.yaml" --output-file "$work/out.sh" -- hello '' > "$work/completions"
stage=cli-completion-sort
LC_ALL=C sort "$work/completions" > "$work/actual"
printf 'john\nmike\n' > "$work/expected"
stage=cli-completion-assert
diff -u "$work/expected" "$work/actual"
printf 'PASS downstream original-units=%s public-symbols=%s consumers=1 cli-completions=2 skips=0\n' "$count" "$symbols"
SH
chmod 0755 %{buildroot}%{_datadir}/libecoli/run-tests.sh
(cd %{buildroot}%{_datadir}/libecoli; sha256sum test/*.c test/*.h consumer.c ecoli.sh test.yaml gen_sym_check.py) > %{buildroot}%{_datadir}/libecoli/SHA256SUMS

%check
# Complete original suite and original public-symbol linker contract.
meson test -C build --print-errorlogs
python3 - <<'PY'
import json
from pathlib import Path
rows = [json.loads(line) for line in Path('build/meson-logs/testlog.json').read_text().splitlines()]
assert len(rows) == 33, len(rows)
assert all(row['result'] == 'OK' for row in rows), rows
print('PASS upstream original-units=33 skips=0')
PY
make check-symbols BUILDDIR=build CC=gcc
bash %{buildroot}%{_datadir}/libecoli/run-tests.sh "%{buildroot}"

%files
%license LICENSE COPYRIGHT-NOTICES include/ecoli/murmurhash.h
%doc README.md
%{_libdir}/libecoli.so*
%{_libdir}/pkgconfig/libecoli.pc
%{_includedir}/ecoli.h
%{_includedir}/ecoli/
%{_bindir}/ecoli-parse-yaml
%{_bindir}/ecoli-parse-yaml.sh
%{_libexecdir}/libecoli/
%{_datadir}/libecoli/
%{_docdir}/libecoli/html/
%{_mandir}/man3/*.3*

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11.8-1
- Preserve all upstream auto features, units, examples, docs and symbol checks.
