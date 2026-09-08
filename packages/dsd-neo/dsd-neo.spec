# SPDX-License-Identifier: Apache-2.0
Name:           dsd-neo
Version:        2.5.1
Release:        3%{?dist}
Summary:        Digital Speech Decoder - A modern, modular, and performance enhanced C/C++ decoder for digital voice. DMR, P25, NXDN, YSF, and more.
License:        GPL-3.0-or-later
URL:            https://github.com/arancormonk/dsd-neo
Source0:        dsd-neo-2.5.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libsndfile-devel
BuildRequires:  make
BuildRequires:  mbelib-neo >= 2.0.0
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pulseaudio-libs-devel

%description
Digital Speech Decoder - A modern, modular, and performance enhanced C/C++ decoder for digital voice. DMR, P25, NXDN, YSF, and more.

%prep
%autosetup -p1

%build
%cmake_conf -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYRIGHT
%license LICENSE
%doc README.md

%changelog
* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-3
- Configure in the RPM out-of-source build directory used by later macros.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-2
- Declare the required C++, audio, crypto, terminal, and mbelib build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
