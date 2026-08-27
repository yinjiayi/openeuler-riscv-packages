# SPDX-License-Identifier: Apache-2.0
Name:           qrtr
Version:        1.2
Release:        1%{?dist}
Summary:        Userspace reference for net/qrtr in the Linux kernel
License:        BSD-3-Clause
URL:            https://github.com/linux-msm/qrtr
Source0:        qrtr-1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Userspace reference for net/qrtr in the Linux kernel

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Initial openEuler RISC-V package from the full package inventory.
