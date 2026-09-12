# SPDX-License-Identifier: Apache-2.0
Name:           hashrat
Version:        1.25
Release:        1%{?dist}
Summary:        Hashing tool supporting md5,sha1,sha256,sha512,whirlpool,jh and hmac versions of these. Includes recursive file hashing and other features.
License:        GPL-3.0-or-later
URL:            https://github.com/ColumPaget/Hashrat
Source0:        hashrat-1.25.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Hashing tool supporting md5,sha1,sha256,sha512,whirlpool,jh and hmac versions of these. Includes recursive file hashing and other features.

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
%doc README.md
%doc CHANGELOG

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.25-1
- Initial openEuler RISC-V package from the full package inventory.
