# SPDX-License-Identifier: Apache-2.0
Name:           pcr-oracle
Version:        0.6.5
Release:        1%{?dist}
Summary:        Predict TPM PCR values
License:        GPL-2.0-or-later
URL:            https://github.com/openSUSE/pcr-oracle
Source0:        pcr-oracle-0.6.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Predict TPM PCR values

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.5-1
- Initial openEuler RISC-V package from the full package inventory.
