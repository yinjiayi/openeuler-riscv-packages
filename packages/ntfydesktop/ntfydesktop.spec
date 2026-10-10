# SPDX-License-Identifier: Apache-2.0
Name:           ntfydesktop
Version:        1.6.0
Release:        1%{?dist}
Summary:        Subscribe to topics from any ntfy server and receive notifications natively on the desktop.
License:        GPL-3.0-or-later
URL:            https://github.com/emmaexe/ntfyDesktop
Source0:        ntfydesktop-1.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Subscribe to topics from any ntfy server and receive notifications natively on the desktop.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
