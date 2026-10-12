# SPDX-License-Identifier: Apache-2.0
Name:           mdtoc
Version:        0.2.2
Release:        1%{?dist}
Summary:        Command line Markdown viewer/editor/toc generator.
License:        GPL-3.0-or-later
URL:            https://github.com/bfoersterling/mdtoc
Source0:        mdtoc-0.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Command line Markdown viewer/editor/toc generator.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
