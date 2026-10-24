# SPDX-License-Identifier: Apache-2.0
Name:           qat-zstd-plugin
Version:        1.0.0
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology ZSTD Plugin
License:        BSD-3-Clause
URL:            https://github.com/intel/QAT-ZSTD-Plugin
Source0:        qat-zstd-plugin-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Intel QuickAssist Technology ZSTD Plugin

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
%license LICENSE.ZSTD
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
