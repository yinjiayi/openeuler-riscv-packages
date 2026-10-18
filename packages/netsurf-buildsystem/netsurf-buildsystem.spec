# SPDX-License-Identifier: Apache-2.0
# Only makefiles/scripts/data are installed; test executables stay disposable.
%global debug_package %{nil}
Name:           netsurf-buildsystem
Version:        1.10
Release:        1
Summary:        Shared makefiles and test tools for NetSurf libraries
License:        MIT AND NCSA AND LicenseRef-Sorttable-2007
URL:            https://source.netsurf-browser.org/buildsystem
Source0:        buildsystem-%{version}.tar.gz
ExclusiveArch:  riscv64
BuildRequires:  make gcc binutils perl pkgconfig tar gzip coreutils diffutils which
Requires:       make gcc binutils perl pkgconfig tar gzip coreutils diffutils which

%description
Shared makefile fragments and test tools used by the independently released
NetSurf libraries. The unchanged source archive is included for installed-tool
regression checks. This does not package the NetSurf browser or enable LLVM
analysis tooling that upstream's normal install target does not install.

%prep
%autosetup -n buildsystem-%{version}

%build
%make_build

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -Dpm0644 %{SOURCE0} %{buildroot}%{_datadir}/netsurf-buildsystem/qa/buildsystem-%{version}.tar.gz

%check
set -euo pipefail
run_installed_defaults() {
    local root=$1 work shared archive file driver
    shared="$root/usr/share/netsurf-buildsystem"
    archive="$shared/qa/buildsystem-1.10.tar.gz"
    printf '%s  %s\n' 3d3e39d569e44677c4b179129bde614c65798e2b3e6253160239d1fd6eae4d79 "$archive" | sha256sum -c -
    work=$(mktemp -d)
    (
        trap 'rm -rf -- "$work"' EXIT
        tar -xzf "$archive" -C "$work"
        cd "$work/buildsystem-1.10"
        for file in top tools subdir pkgconfig clang gcc norcroft open64; do
            cmp -- "makefiles/Makefile.$file" "$shared/makefiles/Makefile.$file"
        done
        cmp -- testtools/testrunner.pl "$shared/testtools/testrunner.pl"
        cmp -- citools/jenkins-build.sh "$shared/citools/jenkins-build.sh"
        perl -c "$shared/testtools/testrunner.pl"
        bash -n "$shared/citools/jenkins-build.sh"
        # Upstream intentionally defines root test as an empty target.
        make test
        make -C example NSSHARED="$shared" BUILDDIR="$work/example-build" all
        make -C example NSSHARED="$shared" BUILDDIR="$work/example-build" test
        for driver in test test2; do
            gcc -Iexample/src1 "example/$driver/foo.c" "$work/example-build/libfoo.a" -o "$work/$driver"
            test "$("$work/$driver")" = PASS
        done
        printf '%s\n' 'PASS netsurf-buildsystem original defaults and two unchanged example drivers using installed makefiles'
    )
}

run_installed_defaults '%{buildroot}'

%files
%license COPYING llvm/LICENSE.TXT llvm/sorttable.js
%doc README
%{_datadir}/netsurf-buildsystem/

%changelog
* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10-1
- Preserve upstream installation and default tests; replay unchanged examples against installed tools.
