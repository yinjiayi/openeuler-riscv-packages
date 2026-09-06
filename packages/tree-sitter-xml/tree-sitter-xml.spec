# SPDX-License-Identifier: Apache-2.0
Name:           tree-sitter-xml
Version:        0.7.0
Release:        1%{?dist}
Summary:        XML & DTD grammars for tree-sitter
License:        MIT
URL:            https://github.com/tree-sitter-grammars/tree-sitter-xml
Source0:        tree-sitter-xml-0.7.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
XML & DTD grammars for tree-sitter

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
