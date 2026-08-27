# SPDX-License-Identifier: Apache-2.0
Name:           libchronoid
Version:        1.0.2
Release:        1%{?dist}
Summary:        C11 toolkit for time-ordered IDs: KSUID (segmentio wire-compat) + UUIDv7 (RFC 9562)
License:        LGPL-3.0-or-later
URL:            https://github.com/semantic-reasoning/libchronoid
Source0:        libchronoid-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
C11 toolkit for time-ordered IDs: KSUID (segmentio wire-compat) + UUIDv7 (RFC 9562)

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%license LICENSE.MIT
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
