# SPDX-License-Identifier: Apache-2.0
Name:           amqp-cpp
Version:        4.3.27
Release:        1%{?dist}
Summary:        C++ library for asynchronous non-blocking communication with RabbitMQ
License:        Apache-2.0
URL:            https://github.com/CopernicaMarketingSoftware/AMQP-CPP
Source0:        amqp-cpp-4.3.27.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ library for asynchronous non-blocking communication with RabbitMQ

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3.27-1
- Initial openEuler RISC-V package from the full package inventory.
