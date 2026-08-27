# SPDX-License-Identifier: Apache-2.0
Name:           ibdev2netdev
Version:        0.2.0
Release:        1%{?dist}
Summary:        List netdevs with their associated RDMA interface (IPoIB, RoCE, iWarp)
License:        GPL-3.0-or-later
URL:            https://github.com/nmorey/ibdev2netdev
Source0:        ibdev2netdev-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
List netdevs with their associated RDMA interface (IPoIB, RoCE, iWarp)

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
