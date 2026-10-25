# SPDX-License-Identifier: Apache-2.0
Name:           fcitx5-vinput
Version:        2.3.5
Release:        1%{?dist}
Summary:        Offline voice input addon for Fcitx5 with optional OpenAI-compatible postprocess
License:        GPL-3.0-or-later
URL:            https://github.com/xifan2333/fcitx5-vinput
Source0:        fcitx5-vinput-2.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Offline voice input addon for Fcitx5 with optional OpenAI-compatible postprocess

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
