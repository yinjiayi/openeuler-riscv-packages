# SPDX-License-Identifier: Apache-2.0
Name:           xtensor-io
Version:        0.13.0
Release:        1%{?dist}
Summary:        xtensor plugin to read and write images, audio files, numpy (compressed) npz and HDF5
License:        BSD-3-Clause
URL:            https://github.com/xtensor-stack/xtensor-io
Source0:        xtensor-io-0.13.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
xtensor plugin to read and write images, audio files, numpy (compressed) npz and HDF5

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-1
- Initial openEuler RISC-V package from the full package inventory.
