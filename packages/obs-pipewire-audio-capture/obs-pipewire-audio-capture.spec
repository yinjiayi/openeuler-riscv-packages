# SPDX-License-Identifier: Apache-2.0
Name:           obs-pipewire-audio-capture
Version:        1.2.1
Release:        1%{?dist}
Summary:        PipeWire audio capturing for OBS Studio
License:        GPL-2.0-or-later
URL:            https://github.com/dimtpap/obs-pipewire-audio-capture
Source0:        obs-pipewire-audio-capture-1.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
PipeWire audio capturing for OBS Studio

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
