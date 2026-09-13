# SPDX-License-Identifier: Apache-2.0
Name:           tree-sitter-wikitext
Version:        0.1.1
Release:        1%{?dist}
Summary:        RPMspec grammar for tree-sitter
License:        MIT
URL:            https://github.com/santhoshtr/tree-sitter-wikitext
Source0:        tree-sitter-wikitext-0.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
RPMspec grammar for tree-sitter

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
