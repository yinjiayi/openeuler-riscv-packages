# SPDX-License-Identifier: Apache-2.0
Name:           flashmq
Version:        1.26.2
Release:        1%{?dist}
Summary:        FlashMQ is a light-weight MQTT broker/server, designed to take good advantage of multi-CPU environments
License:        OSL-3.0
URL:            https://github.com/halfgaar/FlashMQ
Source0:        flashmq-1.26.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
FlashMQ is a light-weight MQTT broker/server, designed to take good advantage of multi-CPU environments

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.26.2-1
- Initial openEuler RISC-V package from the full package inventory.
