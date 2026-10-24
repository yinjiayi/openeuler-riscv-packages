# SPDX-License-Identifier: Apache-2.0
Name:           ember-plus
Version:        1.8.2.2
Release:        4%{?dist}
Summary:        Ember+ control protocol - Slick and free for all!
License:        BSL-1.0
URL:            https://github.com/Lawo/ember-plus
Source0:        ember-plus-1.8.2.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt5-qtbase-devel

%description
Ember+ control protocol - Slick and free for all!

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir}
%cmake_build

# The aggregate project does not add libember's test programs. Configure
# libember as a top-level project so all four upstream self-tests are built.
%cmake -S libember -B %{_vpath_builddir}-libember-tests
%{__cmake} --build %{_vpath_builddir}-libember-tests %{?_smp_mflags} --verbose

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
for test in \
  libember-test-streambuffer \
  libember-test-static_encode_decode \
  libember-test-dynamic_encode_decode \
  libember-test-glow_value; do
  "%{_vpath_builddir}-libember-tests/Tests/${test}"
done

%files -f %{name}.files
%license LICENSE.TXT
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2.2-4
- Allow 120 minutes for both the aggregate build and all four upstream self-tests.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2.2-3
- Use the explicit out-of-source directory consumed by the RPM CMake macros.
- Build and execute all four upstream libember self-test programs.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2.2-2
- Add the Qt 5 development dependency required by the TinyEmber applications.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
