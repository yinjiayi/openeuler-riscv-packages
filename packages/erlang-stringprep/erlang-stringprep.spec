# SPDX-License-Identifier: Apache-2.0
Name:           erlang-stringprep
Version:        1.0.33
Release:        1%{?dist}
Summary:        A framework for preparing Unicode strings to help input and comparison
License:        Apache-2.0
URL:            https://github.com/processone/stringprep
Source0:        erlang-stringprep-1.0.33.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A framework for preparing Unicode strings to help input and comparison

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
%license LICENSE.ALL
%license LICENSE.TCL
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.33-1
- Initial openEuler RISC-V package from the full package inventory.
