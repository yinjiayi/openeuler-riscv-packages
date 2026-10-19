# SPDX-License-Identifier: Apache-2.0
Name:           makeenv
Version:        1.0.3
Release:        1
Summary:        Run make with environment loaded from .makeenv
License:        ISC
URL:            https://codeberg.org/maandree/makeenv
Source0:        https://codeberg.org/maandree/makeenv/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
Load options, macros and targets from .makeenv, then invoke make.

%package tests
Summary:        Official source archive for downstream makeenv validation
Requires:       %{name} = %{version}-%{release}
Requires:       make
Requires:       /bin/sh
Requires:       coreutils
Requires:       diffutils

%description tests
Unchanged checksum-bound whole source archive; upstream has no test driver.

%prep
%autosetup -n makeenv

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/makeenv/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/makeenv/qa/makeenv-%{version}.tar.gz

%check
run_installed_tests() (
    set -eux
    root=$1
    tool="$root/usr/bin/makeenv"
    archive="$root/usr/share/makeenv/qa/makeenv-1.0.3.tar.gz"
    echo '4076b9b6b76dd63b4b9d2ab7070a6576c43149b390985e0b5ba0394c27933f23  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    cd "$work"
    cat > capture <<'SH'
#!/bin/sh
printf '<%%s>\n' "$@"
printf 'GREETING=<%%s>\n' "$GREETING"
SH
    chmod 755 capture
    printf '<%%s>\n' '-unknown' 'A=hello world' 'target' '--' > expected
    printf 'GREETING=<>\n' >> expected
    env -i PATH=/usr/bin:/bin LC_ALL=C MAKEENV_MAKE="$work/capture" "$tool" -unknown 'A=hello world' target -- > actual
    cmp -- expected actual
    printf '%%s\n' '# comment' ' -k ' ' GREETING = hello world ' 'filetarget' > .makeenv
    printf '<%%s>\n' '-k' '-s' '--' 'GREETING=hello world' 'CLI=override' 'filetarget' 'clitarget' > expected
    printf 'GREETING=<hello world>\n' >> expected
    env -i PATH=/usr/bin:/bin LC_ALL=C MAKEENV_MAKE="$work/capture" "$tool" -s CLI=override clitarget > actual
    cmp -- expected actual
    check_status() {
        expected_status=$1
        shift
        if env -i PATH=/usr/bin:/bin LC_ALL=C "$@" > stdout.log 2> stderr.log; then got=0; else got=$?; fi
        test "$got" -eq "$expected_status"
        test ! -s stdout.log
        test -s stderr.log
    }
    check_status 125 MAKEENV_MAKE="$work/capture" "$tool" -Z
    check_status 125 MAKEENV_MAKE="$work/capture" "$tool" -f
    check_status 127 MAKEENV_MAKE="$work/absent" "$tool"
    printf 'not executable\n' > nonexec
    chmod 644 nonexec
    check_status 126 MAKEENV_MAKE="$work/nonexec" "$tool"
    printf '%%s\n' ' GREETING = hello world ' > .makeenv
    printf 'all:\n\t@printf '\''%%%%s\\n'\'' "$(GREETING):$(VALUE)" > result\n' > Makefile
    env -i PATH=/usr/bin:/bin LC_ALL=C MAKEENV_MAKE=/usr/bin/make "$tool" VALUE=cli
    printf 'hello world:cli\n' > expected
    cmp -- expected result
    echo 'PASS makeenv downstream argument ordering, environment, real make and 125/126/127 statuses'
)
run_installed_tests '%{buildroot}'

%files
%license LICENSE
%doc README
%{_bindir}/makeenv
%{_mandir}/man1/makeenv.1*
%{_mandir}/man5/makeenv.5*

%files tests
%license LICENSE
%{_datadir}/makeenv/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0.3-1
- Preserve default build and add downstream installed functional checks.
