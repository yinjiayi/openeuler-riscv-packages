# SPDX-License-Identifier: Apache-2.0
Name:           ykchalresp-nfc
Version:        0.1.1
Release:        1%{?dist}
Summary:        Perform challenge response using YubiKey via NFC
License:        GPL-3.0-or-later
URL:            https://github.com/Frederick888/ykchalresp-nfc
Source0:        ykchalresp-nfc-0.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Perform challenge response using YubiKey via NFC

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
