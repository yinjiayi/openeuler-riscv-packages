# SPDX-License-Identifier: Apache-2.0
Name:           scdoc
Version:        1.11.5
Release:        1%{?dist}
Summary:        Generate roff manual pages from a simple markup format
License:        MIT
URL:            https://git.sr.ht/~sircmpwn/scdoc
Source0:        https://git.sr.ht/~sircmpwn/scdoc/archive/1.11.5.tar.gz#/scdoc-1.11.5.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  findutils


%description
Scdoc generates roff manual pages from its documented UTF-8 markup format.

%package tests
Summary:        Offline original Scdoc test-suite replay
Requires:       %{name} = %{version}-%{release}
Requires:       make
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       grep
Requires:       sed
Requires:       findutils
Requires:       bash

%description tests
All nine original test drivers and 56 cases replay against the installed
executable, with explicit detection of upstream's printed FAIL results.

%prep
%autosetup

%build
%make_build CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" PREFIX=%{_prefix} PCDIR=%{_datadir}/pkgconfig

%install
%make_install PREFIX=%{_prefix} PCDIR=%{_datadir}/pkgconfig
install -d %{buildroot}%{_libexecdir}/scdoc-tests
install -m644 %{SOURCE0} %{buildroot}%{_libexecdir}/scdoc-tests/scdoc-1.11.5.tar.gz
install -m755 /dev/null %{buildroot}%{_libexecdir}/scdoc-tests/replay.sh
cat > %{buildroot}%{_libexecdir}/scdoc-tests/replay.sh <<'SCDOC_REPLAY'
#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
run_original_tests() {
    root=$1
    binary="$root/usr/bin/scdoc"
    archive="$root/usr/libexec/scdoc-tests/scdoc-1.11.5.tar.gz"
    test -x "$binary"
    printf '98780bbdf16c1bce89ef3a8c0f537ac6e4ea77087b609e7698857614488a2a62  %%s\n' "$archive" | sha256sum -c -
    scratch=$(mktemp -d)
    trap 'rm -rf -- "$scratch"' EXIT HUP INT TERM
    tar -xzf "$archive" -C "$scratch"
    cd "$scratch/scdoc-1.11.5"
    ln -s -- "$binary" scdoc
    export SOURCE_DATE_EPOCH=0
    make -o scdoc check > "$scratch/default.log" 2>&1
    cat "$scratch/default.log"
    test "$(grep -c '^== test/' "$scratch/default.log")" -eq 9
    test "$(grep -c 'OK$' "$scratch/default.log")" -eq 56
    if grep -q 'FAIL$' "$scratch/default.log"; then exit 1; fi
    "$binary" -v | grep -Fx 'scdoc 1.11.5'
    printf 'PASS scdoc original 9 drivers and 56 cases against packaged executable\n'
}
run_original_tests "${1-}"
SCDOC_REPLAY

%check
make check > default-suite.log 2>&1
cat default-suite.log
test "$(grep -c '^== test/' default-suite.log)" -eq 9
test "$(grep -c 'OK$' default-suite.log)" -eq 56
if grep -q 'FAIL$' default-suite.log; then exit 1; fi
sh %{buildroot}%{_libexecdir}/scdoc-tests/replay.sh "%{buildroot}"

%files
%license COPYING
%doc README.md
%{_bindir}/scdoc
%{_datadir}/pkgconfig/scdoc.pc
%{_mandir}/man1/scdoc.1*
%{_mandir}/man5/scdoc.5*

%files tests
%license COPYING
%{_libexecdir}/scdoc-tests/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.11.5-1
- Package the official fixed source with unchanged default build and tests
