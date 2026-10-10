# SPDX-License-Identifier: Apache-2.0
Name:           l-smash
Version:        2.14.5
Release:        1%{?dist}
Summary:        MP4 muxer and other tools
License:        ISC
URL:            https://github.com/l-smash/l-smash
Source0:        l-smash-2.14.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
MP4 muxer and other tools

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.14.5-1
- Initial openEuler RISC-V package from the full package inventory.
