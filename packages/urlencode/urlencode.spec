# SPDX-License-Identifier: Apache-2.0
Name:           urlencode
Version:        1.6.0
Release:        1%{?dist}
Summary:        base64-like encoder/decoder for URL percent-encoding
License:        GPL-3.0-or-later
URL:            https://github.com/AquilaIrreale/urlencode
Source0:        urlencode-1.6.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
base64-like encoder/decoder for URL percent-encoding

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
