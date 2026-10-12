# SPDX-License-Identifier: Apache-2.0
Name:           formula-vst3
Version:        1.2.2
Release:        2%{?dist}
Summary:        Open-source audio effects as code editor VST3 plugin and standalone application.
License:        BSL-1.0
URL:            https://github.com/soundspear/formula
Source0:        formula-vst3-1.2.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Open-source audio effects as code editor VST3 plugin and standalone application.

%prep
%autosetup -n formula-%{version} -p1

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-2
- Use the source archive's actual formula-version root directory.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
