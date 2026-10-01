# SPDX-License-Identifier: Apache-2.0
Name:           rtrlib
Version:        0.8.0
Release:        5%{?dist}
Summary:        RPKI-RTR client library
License:        MIT
URL:            https://github.com/rtrlib/rtrlib
Source0:        rtrlib-0.8.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  libssh-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
RPKI-RTR client library

%prep
%autosetup -p1

%build
%cmake_conf \
  -DRTRLIB_TRANSPORT_SSH=ON \
  -DUNIT_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
# brp-compress changes manual-page suffixes after installation, so keep them out
# of the generated file list and match their final compressed names below.
sed -i '\|^/usr/share/man/|d' %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} -N | grep -F -- 'Total Tests: 10'
# These two integration tests require the public
# rpki-validator.realmv6.org:8283 service.  The remaining eight registered
# tests are deterministic and exercise the local library implementation.
ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --no-tests=error \
  -E '^(test_live_validation|test_dynamic_groups)$'

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG
%{_mandir}/man1/rpki-rov.1*
%{_mandir}/man1/rtrclient.1*

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-5
- Avoid expanding an RPM section macro from a SPEC comment.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-4
- Match manual pages after the RPM brp-compress suffix transformation.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-3
- Run all eight deterministic tests and identify the two external-service tests.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-2
- Use the openEuler out-of-source CMake workflow, retain SSH, and enable tests.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
