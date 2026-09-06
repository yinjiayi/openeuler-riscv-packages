# SPDX-License-Identifier: Apache-2.0
Name:           leizi-shell
Version:        1.4.0
Release:        1%{?dist}
Summary:        Modern POSIX-compatible shell with ZSH-style arrays and Powerlevel10k-inspired prompts
License:        GPL-3.0-or-later
URL:            https://github.com/Zixiao-System/leizi-shell
Source0:        leizi-shell-1.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Modern POSIX-compatible shell with ZSH-style arrays and Powerlevel10k-inspired prompts

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
