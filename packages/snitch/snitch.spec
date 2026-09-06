# SPDX-License-Identifier: Apache-2.0
Name:           snitch
Version:        1.3.2
Release:        1%{?dist}
Summary:        Lightweight C++20 testing framework
License:        BSL-1.0
URL:            https://github.com/snitch-org/snitch
Source0:        snitch-1.3.2.tar.gz
Source1:        doctest-2.4.9.tar.gz
Patch0:         0001-tests-accept-release-version.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Lightweight C++20 testing framework

%prep
%autosetup -p1 -a 1

%build
export CXXFLAGS="%{optflags} -ffile-prefix-map=$PWD=/usr/src/snitch"
%cmake_conf \
  -DSNITCH_DO_TEST=ON \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_DOCTEST="$PWD/doctest-2.4.9"
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{__cmake} --build %{_vpath_builddir} --target snitch_runtime_tests_run
%{__cmake} --build %{_vpath_builddir} --target snitch_runtime_tests_self_run
%{__cmake} --build %{_vpath_builddir} --target snitch_approval_tests_run

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
