# SPDX-License-Identifier: Apache-2.0
Name:           tree-sitter-svelte
Version:        1.0.2
Release:        1%{?dist}
Summary:        Svelte grammar for tree-sitter
License:        MIT
URL:            https://github.com/tree-sitter-grammars/tree-sitter-svelte
Source0:        tree-sitter-svelte-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Svelte grammar for tree-sitter

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
