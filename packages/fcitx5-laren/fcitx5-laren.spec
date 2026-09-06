# SPDX-License-Identifier: Apache-2.0
Name:           fcitx5-laren
Version:        0.3.5
Release:        2%{?dist}
Summary:        Arabizi to Arabic transliteration engine for Fcitx5
License:        GPL-3.0-or-later
URL:            https://github.com/mmaher88/laren
Source0:        fcitx5-laren-0.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Arabizi to Arabic transliteration engine for Fcitx5

%prep
%autosetup -n laren-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.5-2
- Use the upstream laren archive root during source preparation.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
