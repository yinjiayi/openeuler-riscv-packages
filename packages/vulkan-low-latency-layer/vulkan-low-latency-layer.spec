# SPDX-License-Identifier: Apache-2.0
Name:           vulkan-low-latency-layer
Version:        0.2.0
Release:        1%{?dist}
Summary:        Implicit Vulkan layer that reduces click-to-photon latency for AMD and NVidia.
License:        MIT
URL:            https://github.com/Korthos-Software/low_latency_layer
Source0:        vulkan-low-latency-layer-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Implicit Vulkan layer that reduces click-to-photon latency for AMD and NVidia.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
