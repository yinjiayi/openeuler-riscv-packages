# SPDX-License-Identifier: Apache-2.0
Name:           timeprefix
Version:        3.1.2
Release:        1
Summary:        Prefix input lines with boot-time and UTC text
License:        ISC
URL:            https://codeberg.org/maandree/timeprefix
Source0:        https://codeberg.org/maandree/timeprefix/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  diffutils

%description
Prefix each input line with boot-time and UTC text.

%package tests
Summary:        Original timeprefix source for installed functional replays
Requires:       %{name} = %{version}-%{release}
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       sed
Requires:       diffutils
Requires:       /bin/sh

%description tests
Checksum-bound whole source archive and unchanged original functional pipeline.

%prep
%autosetup -n timeprefix

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/timeprefix/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/timeprefix/qa/timeprefix-%{version}.tar.gz

%check
make check CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"
run_installed_tests() (
    set -eux
    root=$1
    tool="$root/usr/bin/timeprefix"
    archive="$root/usr/share/timeprefix/qa/timeprefix-3.1.2.tar.gz"
    echo 'c473c23d46ad44947de33a5dc4a8cda3331594fe2c927d6125cb8dfbc1c40585  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cd "$work"
    # Exactly the original check pipeline, using the staged/installed command.
    test "$(printf '%%s\n' a b c d e | "$tool" | sed 's/[0-9]/0/g' | md5sum | tr -Cd '[:xdigit:]\n')" = '3f1efed82f846e18973bd016fe5aeba4'
    strip_prefix() {
        sed -E 's/^\[[0-9]{10,}\.[0-9]{4} [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC\] //'
    }
    printf 'first line\n\n spaces \t remain\n' > input
    { printf '%%s\n' '--- Program started ---'; cat input; printf '%%s\n' '--- Program exited ---'; } > expected
    "$tool" < input > actual 2> stderr.log
    test ! -s stderr.log
    strip_prefix < actual > stripped
    cmp -- expected stripped
    "$tool" -- < input > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    printf '%%05000d\n' 0 > input
    { printf '%%s\n' '--- Program started ---'; cat input; printf '%%s\n' '--- Program exited ---'; } > expected
    "$tool" < input > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    printf '%%s\n' '--- Program started ---' '--- Program exited ---' > expected
    "$tool" < /dev/null > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    if "$tool" unexpected > stdout.log 2> stderr.log; then actual_status=0; else actual_status=$?; fi
    test "$actual_status" -eq 1
    test ! -s stdout.log
    test -s stderr.log
    echo 'PASS timeprefix original normalized pipeline and installed payload/usage formatting checks'
)
run_installed_tests '%{buildroot}'

%files
%license LICENSE
%doc README
%{_bindir}/timeprefix
%{_mandir}/man1/timeprefix.1*

%files tests
%license LICENSE
%{_datadir}/timeprefix/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 3.1.2-1
- Preserve original default check and add functional payload/format replay; no native clock claim.
