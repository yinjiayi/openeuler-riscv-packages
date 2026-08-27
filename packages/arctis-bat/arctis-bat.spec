# SPDX-License-Identifier: Apache-2.0
Name:           arctis-bat
Version:        0.2.1
Release:        1%{?dist}
Summary:        CLI tool for checking SteelSeries Arctis headsets battery on linux
License:        Apache-2.0
URL:            https://github.com/jewlexx/arctis-bat
Source0:        arctis-bat-0.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
CLI tool for checking SteelSeries Arctis headsets battery on linux

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
