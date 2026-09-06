# SPDX-License-Identifier: Apache-2.0
Name:           simple-sc
Version:        0.1.2
Release:        2%{?dist}
Summary:        A simple PipeWire screen recording utility for Linux
License:        MIT
URL:            https://github.com/directmusic/simple-sc
Source0:        simple-sc-0.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  dbus-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libportal-devel
BuildRequires:  make
BuildRequires:  pipewire-devel
BuildRequires:  pkgconf
BuildRequires:  zlib-devel

%description
A simple PipeWire screen recording utility for Linux

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

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-2
- Add the pkg-config, PipeWire, D-Bus, portal, FFmpeg, and zlib build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
