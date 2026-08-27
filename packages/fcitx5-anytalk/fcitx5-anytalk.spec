# SPDX-License-Identifier: Apache-2.0
Name:           fcitx5-anytalk
Version:        0.5.2
Release:        1%{?dist}
Summary:        Voice input addon for fcitx5 with a Qt6 Aurora overlay
License:        MIT
URL:            https://github.com/yizhisec/fcitx5-anytalk
Source0:        fcitx5-anytalk-0.5.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Voice input addon for fcitx5 with a Qt6 Aurora overlay

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
