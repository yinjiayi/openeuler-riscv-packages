# SPDX-License-Identifier: Apache-2.0
Name:           ocaml-spawn
Version:        0.17.0
Release:        1%{?dist}
Summary:        A small OCaml library for spawning sub-processes
License:        MIT
URL:            https://github.com/janestreet/spawn
Source0:        ocaml-spawn-0.17.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A small OCaml library for spawning sub-processes

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17.0-1
- Initial openEuler RISC-V package from the full package inventory.
