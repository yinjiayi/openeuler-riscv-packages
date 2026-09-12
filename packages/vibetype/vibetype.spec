# SPDX-License-Identifier: Apache-2.0
Name:           vibetype
Version:        0.1.4
Release:        1%{?dist}
Summary:        Voice-to-text input method backend and CLI (standalone, no input method frontend)
License:        MIT
URL:            https://github.com/lingzolabs/vibetype
Source0:        vibetype-0.1.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Voice-to-text input method backend and CLI (standalone, no input method frontend)

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
