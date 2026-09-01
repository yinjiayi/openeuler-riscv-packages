# SPDX-License-Identifier: Apache-2.0
Name:           simplearchiver
Version:        3.5.0
Release:        3%{?dist}
Summary:        An alternative to tar
License:        ISC
URL:            https://github.com/Stephen-Seo/SimpleArchiver
Source0:        simplearchiver-3.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
An alternative to tar

%prep
%autosetup -n SimpleArchiver-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DSDSA_OVERRIDE_VERSION_STRING=%{version}
%cmake_build

%install
install -Dpm 0755 %{_vpath_builddir}/simplearchiver %{buildroot}%{_bindir}/simplearchiver
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/test_datastructures
%{_vpath_builddir}/test_simplearchiver

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.0-3
- Install the built executable explicitly because upstream defines no CMake install rule.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.0-2
- Use the verified upstream archive root and explicit CMake build directory.
- Set the release version without relying on unavailable Git metadata.
- Run both upstream unit-test executables directly because they are not registered with CTest.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
