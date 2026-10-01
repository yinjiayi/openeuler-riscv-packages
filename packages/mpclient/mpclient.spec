# SPDX-License-Identifier: Apache-2.0
Name:           mpclient
Version:        0.35
Release:        1%{?dist}
Summary:        A minimalist command line interface to MPD
License:        GPL-2.0-or-later
URL:            https://github.com/MusicPlayerDaemon/mpc
Source0:        mpclient-0.35.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A minimalist command line interface to MPD

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
%license COPYING
%doc README.rst
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.35-1
- Initial openEuler RISC-V package from the full package inventory.
