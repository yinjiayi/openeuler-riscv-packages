# SPDX-License-Identifier: Apache-2.0
Name:           percetto
Version:        0.1.6
Release:        1%{?dist}
Summary:        Minimal C wrapper for Perfetto SDK to enable app tracing
License:        Apache-2.0
URL:            https://github.com/olvaffe/percetto
Source0:        percetto-0.1.6.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Minimal C wrapper for Perfetto SDK to enable app tracing

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.6-1
- Initial openEuler RISC-V package from the full package inventory.
