# SPDX-License-Identifier: Apache-2.0
Name:           bin2cpp
Version:        3.1.1
Release:        1%{?dist}
Summary:        bin2cpp: The easiest way to embed small files into a c++ executable. bin2cpp converts text or binary files to C++ files (*.h, *.cpp) for easy access within
License:        MIT
URL:            https://github.com/end2endzone/bin2cpp
Source0:        bin2cpp-3.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
bin2cpp: The easiest way to embed small files into a c++ executable. bin2cpp converts text or binary files to C++ files (*.h, *.cpp) for easy access within

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
