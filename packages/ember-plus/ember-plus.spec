# SPDX-License-Identifier: Apache-2.0
Name:           ember-plus
Version:        1.8.2.2
Release:        1%{?dist}
Summary:        Ember+ control protocol - Slick and free for all!
License:        BSL-1.0
URL:            https://github.com/Lawo/ember-plus
Source0:        ember-plus-1.8.2.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Ember+ control protocol - Slick and free for all!

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
%license LICENSE.TXT
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
