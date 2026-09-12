# SPDX-License-Identifier: Apache-2.0
Name:           piper-tts
Version:        1.5.0
Release:        1%{?dist}
Summary:        Fast and local neural text-to-speech engine
License:        GPL-3.0-or-later
URL:            https://github.com/OHF-Voice/piper1-gpl
Source0:        piper-tts-1.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast and local neural text-to-speech engine

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
%license COPYING
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
