# SPDX-License-Identifier: Apache-2.0
Name:           hyades
Version:        1.0.0
Release:        1%{?dist}
Summary:        Unicode/ASCII mathematical typesetting engine with LaTeX input
License:        MPL-2.0
URL:            https://github.com/apology-is-policy/hyades
Source0:        hyades-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Unicode/ASCII mathematical typesetting engine with LaTeX input

%prep
%autosetup -p1

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
