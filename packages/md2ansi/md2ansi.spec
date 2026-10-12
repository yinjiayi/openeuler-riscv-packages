# SPDX-License-Identifier: Apache-2.0
Name:           md2ansi
Version:        1.0.2
Release:        1%{?dist}
Summary:        Zero-dependency C11 Markdown-to-ANSI terminal renderer
License:        GPL-3.0-or-later
URL:            https://github.com/Open-Technology-Foundation/md2ansi.c
Source0:        md2ansi-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Zero-dependency C11 Markdown-to-ANSI terminal renderer

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
