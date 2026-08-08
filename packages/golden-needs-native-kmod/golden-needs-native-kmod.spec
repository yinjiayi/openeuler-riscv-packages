# SPDX-License-Identifier: Apache-2.0
Name:           golden-needs-native-kmod
Version:        1.0
Release:        1%{?dist}
Summary:        Native-kernel validation routing fixture
License:        GPL-2.0-only
URL:            https://github.com/yinjiayi/openeuler-riscv-packages/tree/main/tests/golden
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel

%description
This deterministic out-of-tree kernel module exists only to assert that QEMU
user-mode CI refuses to claim native target-kernel validation.

%prep
%autosetup -p1

%build
%make_build KERNELRELEASE=%{_target_cpu}

%install
install -Dpm0644 golden_native.ko %{buildroot}%{_libdir}/golden-native/golden_native.ko

%check
echo 'Native RISC-V runner must load golden_native.ko and verify its kernel log marker.'
exit 1

%files
%license LICENSE
%doc README.md
%{_libdir}/golden-native/golden_native.ko

%changelog
* Sat Aug 08 2026 Package Automation <noreply@example.invalid> - 1.0-1
- Add native-only routing golden fixture
