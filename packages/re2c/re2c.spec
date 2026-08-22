# SPDX-License-Identifier: Apache-2.0
Name:           re2c
Version:        4.5.1
Release:        1%{?dist}
Summary:        Lexer generator for multiple programming languages
License:        LicenseRef-re2c-Public-Domain
URL:            https://re2c.org/
Source0:        re2c-%{version}.tar.xz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  re2-devel
BuildRequires:  sed

%description
re2c generates fast lexical analyzers from regular expressions. This build
ships upstream's C, D, Go, Haskell, Java, JavaScript, OCaml, Python, Rust,
Swift, V, and Zig frontends together with their standard syntax definitions.

%prep
%autosetup -p1

%build
%configure --disable-libs --disable-benchmarks
%make_build

%install
%make_install

%check
%make_build check
tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT
cat > "$tmpdir/fixture.re" <<'EOF'
#include <stdio.h>
typedef unsigned char YYCTYPE;
static int scan(const YYCTYPE *YYCURSOR) {
    const YYCTYPE *YYMARKER;
    /*!re2c
        re2c:yyfill:enable = 0;
        "RVA23" { return 0; }
        * { return 1; }
    */
}
int main(void) { static const YYCTYPE input[] = "RVA23"; return scan(input); }
EOF
./re2c -o "$tmpdir/fixture.c" "$tmpdir/fixture.re"
%{__cc} %{build_cflags} %{build_ldflags} "$tmpdir/fixture.c" -o "$tmpdir/fixture"
"$tmpdir/fixture"

%files
%license LICENSE
%doc CHANGELOG NO_WARRANTY README.md
%{_bindir}/re2*
%{_datadir}/re2c/
%{_mandir}/man1/re2*.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.1-1
- Initial openEuler RISC-V package with all available frontends and full tests.
