# SPDX-License-Identifier: Apache-2.0
Name:           cymbal
Version:        0.14.0
Release:        1%{?dist}
Summary:        Language-agnostic code navigation CLI powered by tree-sitter
License:        MIT
URL:            https://github.com/1broseidon/cymbal
Source0:        cymbal-0.14.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Language-agnostic code navigation CLI powered by tree-sitter

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14.0-1
- Initial openEuler RISC-V package from the full package inventory.
