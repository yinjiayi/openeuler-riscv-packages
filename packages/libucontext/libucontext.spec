# SPDX-License-Identifier: Apache-2.0
Name:           libucontext
Version:        1.5.2
Release:        1%{?dist}
Summary:        Userspace context switching with RISC-V support
License:        ISC AND LicenseRef-libucontext-test-public-domain
URL:            https://github.com/kaniini/libucontext
Source0:        libucontext-1.5.2.tar.gz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Userspace context switching with the upstream RISC-V RV64 port, shared and
static libraries, public headers and the default POSIX compatibility library.

%prep
%autosetup -n libucontext-49e671dd52ff6791295d8161ad3b6da7dc5f6f9d -p1
# Preserve complete original per-file notices before build products exist.
mkdir license-notices
cp -a arch license-notices/
cp libucontext_posix.c test_libucontext.c test_libucontext_posix.c \
    examples/cooperative_threading.c license-notices/
test "$(head -n 1 VERSION)" = '%{version}'

%build
# Keep FREESTANDING=no, EXPORT_UNPREFIXED=yes and BUILD_POSIX=yes defaults.
%make_build ARCH=riscv64 CC=gcc CFLAGS="%{optflags}" \
    LDFLAGS="%{?build_ldflags}" prefix=%{_prefix} libdir=%{_libdir} \
    pkgconfigdir=%{_libdir}/pkgconfig
%make_build ARCH=riscv64 CC=gcc CFLAGS="%{optflags}" \
    LDFLAGS="%{?build_ldflags}" prefix=%{_prefix} libdir=%{_libdir} \
    pkgconfigdir=%{_libdir}/pkgconfig \
    test_libucontext test_libucontext_posix test_libucontext_bare_posixabi

%install
%make_install ARCH=riscv64 CC=gcc CFLAGS="%{optflags}" \
    LDFLAGS="%{?build_ldflags}" prefix=%{_prefix} libdir=%{_libdir} \
    pkgconfigdir=%{_libdir}/pkgconfig
# The upstream install target omits this development linker symlink.
ln -s libucontext_posix.so.1 %{buildroot}%{_libdir}/libucontext_posix.so
for test_program in test_libucontext test_libucontext_posix test_libucontext_bare_posixabi; do
    install -Dm755 "$test_program" \
        "%{buildroot}%{_libexecdir}/libucontext-tests/$test_program"
done

%check
set -eu
export LC_ALL=C
# Original check target includes all three unchanged test programs.
%make_build check ARCH=riscv64 CC=gcc CFLAGS="%{optflags}" \
    LDFLAGS="%{?build_ldflags}" prefix=%{_prefix} libdir=%{_libdir} \
    pkgconfigdir=%{_libdir}/pkgconfig
for test_program in test_libucontext test_libucontext_posix test_libucontext_bare_posixabi; do
    test -x "$test_program"
    test -x "%{buildroot}%{_libexecdir}/libucontext-tests/$test_program"
done
(
    # Hash installed files after normal RPM brp/strip processing, not the
    # pre-install unstripped build-tree bytes.
    cd %{buildroot}%{_libexecdir}/libucontext-tests
    sha256sum test_libucontext test_libucontext_posix test_libucontext_bare_posixabi > SHA256SUMS
)

%files
%license LICENSE license-notices
%doc README.md NEWS doc/libucontext.scd
%{_libdir}/libucontext.so
%{_libdir}/libucontext.so.1
%{_libdir}/libucontext.a
%{_libdir}/libucontext_posix.so
%{_libdir}/libucontext_posix.so.1
%{_libdir}/libucontext_posix.a
%{_libdir}/pkgconfig/libucontext.pc
%{_includedir}/libucontext
%{_libexecdir}/libucontext-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.2-1
- Preserve upstream defaults and all three original check variants.
