# SPDX-License-Identifier: MIT
Name:           libjson
Version:        0.8
Release:        1%{?dist}
Summary:        Small streaming JSON parser and printer in C
License:        LGPL-2.1-only OR LGPL-3.0-only
URL:            https://github.com/vincenthz/libjson
Source0:        https://codeload.github.com/vincenthz/libjson/tar.gz/2bbe73f129ebf3eafd9b194f960536c146e680c2#/libjson-0.8.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt#/LGPL-2.1.txt
Source2:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/GPL-2.0.txt
Source3:        https://www.gnu.org/licenses/lgpl-3.0.txt#/LGPL-3.0.txt
Source4:        https://www.gnu.org/licenses/gpl-3.0.txt#/GPL-3.0.txt
Patch0:         patches/0001-support-multilib-and-pkgconfig.patch
Patch1:         patches/0002-add-installed-interface-checks.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  pkgconf
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  patch
Requires:       /sbin/ldconfig

%description
Streaming C JSON parser and printer with callbacks and a DOM helper. Includes
the original jsonlint command and preserves upstream comment-handling defaults.
This old upstream release is not certified as a security or conformance layer.

%package devel
Summary:        Development files and installed-interface checks for libjson
License:        (LGPL-2.1-only OR LGPL-3.0-only) AND MIT
Requires:       %{name} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       grep

%description devel
Original header, static archive, linker symlinks and pkg-config file, plus the
complete original 33 test fixtures and runner, original command source and a
separate downstream installed-interface consumer.

%prep
%setup -q -n libjson-2bbe73f129ebf3eafd9b194f960536c146e680c2
%patch0 -p1
%patch1 -p1
cp %{SOURCE1} LGPL-2.1.txt
cp %{SOURCE2} GPL-2.0.txt
cp %{SOURCE3} LGPL-3.0.txt
cp %{SOURCE4} GPL-3.0.txt
sed -n '1,12p' json.h > COPYRIGHT

%build
%make_build CC=gcc CFLAGS="%{optflags} -fPIC -Wall" LDFLAGS="%{build_ldflags} -L." PREFIX=%{_prefix} LIBDIR=lib64

%install
%make_install CC=gcc CFLAGS="%{optflags} -fPIC -Wall" LDFLAGS="%{build_ldflags} -L." PREFIX=%{_prefix} LIBDIR=lib64
install -d %{buildroot}%{_datadir}/libjson/tests
cp -R tests/good tests/bad %{buildroot}%{_datadir}/libjson/tests/
install -m 0755 tests/runtest %{buildroot}%{_datadir}/libjson/tests/runtest
install -m 0644 jsonlint.c downstream/consumer.c %{buildroot}%{_datadir}/libjson/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/libjson/run-tests.sh
(
    cd %{buildroot}%{_datadir}/libjson
    find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)

%check
# Run the exact original target and keep its log; its shell runner masks errors.
make tests CC=gcc CFLAGS="%{optflags} -fPIC -Wall" LDFLAGS="%{build_ldflags} -L." PREFIX=%{_prefix} LIBDIR=lib64 > original-tests.log 2>&1
cat original-tests.log
if grep -F FAILED original-tests.log; then exit 1; fi
test "$(grep -c SUCCESS original-tests.log)" -eq 33
bash %{buildroot}%{_datadir}/libjson/run-tests.sh %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYRIGHT LGPL-2.1.txt GPL-2.0.txt LGPL-3.0.txt GPL-3.0.txt
%doc README documentation
%{_bindir}/jsonlint
%{_libdir}/libjson.so.0.8.0

%files devel
%license downstream/LICENSE.MIT
%{_includedir}/json.h
%{_libdir}/libjson.a
%{_libdir}/libjson.so
%{_libdir}/libjson.so.0
%{_libdir}/libjson.so.0.8
%{_libdir}/pkgconfig/libjson.pc
%{_datadir}/libjson/

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.8-1
- Package fixed official v0.8; retain all default products and original tests.
