# SPDX-License-Identifier: Apache-2.0
Name:           parzip
Version:        1.4.0
Release:        1%{?dist}
Summary:        Parallel ZIP creation and extraction tools
License:        GPL-3.0-or-later AND LicenseRef-parzip-public-domain
URL:            https://github.com/jpakkane/parzip
Source0:        parzip-1.4.0.tar.xz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gtk3-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  sed
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
Requires:       bash
Requires:       coreutils
Requires:       python3

%description
Parallel ZIP creation and extraction tools

%prep
%autosetup -p1
# Preserve original bytes before any compiler, install hook or RPM helper runs.
mkdir original-notices
find . -type f ! -path './original-notices/*' -exec cp --parents -t original-notices -- {} +
find original-notices -type f -exec chmod 0644 {} +
(cd original-notices && find . -type f -exec sha256sum {} + | LC_ALL=C sort -k2) > original-notices.sha256

%build
%set_build_flags
pkg-config --exists gtk+-3.0 zlib liblzma
meson setup build --prefix=%{_prefix} --libdir=%{_lib} --buildtype=plain --wrap-mode=nofallback
ninja -C build -v

%install
DESTDIR=%{buildroot} meson install -C build --no-rebuild
install -Dpm0755 build/test/bytequeue_test %{buildroot}%{_libexecdir}/parzip-tests/bytequeue_test
install -d %{buildroot}%{_datadir}/parzip-tests/test %{buildroot}%{_datadir}/parzip-tests/testdata
install -pm0644 test/unziptest.py test/ziptest.py %{buildroot}%{_datadir}/parzip-tests/test/
install -pm0644 testdata/*.zip %{buildroot}%{_datadir}/parzip-tests/testdata/
find %{buildroot}%{_datadir}/parzip-tests -type f -name '*.py' -exec chmod 0644 {} +
(cd %{buildroot}%{_datadir}/parzip-tests && find test testdata -type f -exec sha256sum {} + | LC_ALL=C sort -k2) > %{buildroot}%{_datadir}/parzip-tests/original-tests.sha256

%check
# Unfiltered original Meson defaults: bytequeue_test, unzip test, zip test.
meson test -C build --no-rebuild --print-errorlogs
(cd original-notices && sha256sum -c ../original-notices.sha256)

%files
%license COPYING original-notices original-notices.sha256
%doc README.md
%{_bindir}/parzip
%{_bindir}/parunzip
%{_mandir}/man1/parzip.1*
%{_mandir}/man1/parunzip.1*
%{_libexecdir}/parzip-tests/
%{_datadir}/parzip-tests/

%changelog
* Fri Oct 23 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Package fixed official release with original defaults, complete notices and installed original test replay.
