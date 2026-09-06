# SPDX-License-Identifier: Apache-2.0
Name:           sigutils
Version:        0.3.0
Release:        3%{?dist}
Summary:        Small signal processing utility library
License:        GPL-3.0-or-later
URL:            https://github.com/BatchDrake/sigutils
Source0:        sigutils-0.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(fftw3f) >= 3.0
BuildRequires:  pkgconfig(sndfile) >= 1.0.2

%description
Small signal processing utility library

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
%{_vpath_builddir}/sutest

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc AUTHORS

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-3
- Configure CMake with the same out-of-source build directory used by the
  build, install, and test macros.

* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-2
- Declare the required libsndfile, single-precision FFTW, pkg-config, and
  pthread development closure.
- Run upstream's sutest harness, which invokes all 18 test entries and is not
  registered with CTest. The real-capture entry retains upstream's self-skip
  when its optional sample is absent from the release archive.
- Keep VOLK as the upstream-optional acceleration path because the fixed
  target repository does not provide pkgconfig(volk).

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
