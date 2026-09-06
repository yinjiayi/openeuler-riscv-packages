# SPDX-License-Identifier: Apache-2.0
Name:           apulse
Version:        0.1.14
Release:        1%{?dist}
Summary:        PulseAudio emulation for ALSA
License:        MIT
URL:            https://github.com/i-rinat/apulse
Source0:        apulse-0.1.14.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
PulseAudio emulation for ALSA

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
%license LICENSE.MIT
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.14-1
- Initial openEuler RISC-V package from the full package inventory.
