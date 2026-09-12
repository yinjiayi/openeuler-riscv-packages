# SPDX-License-Identifier: Apache-2.0
Name:           pnmixer
Version:        0.7.2
Release:        1%{?dist}
Summary:        GTK volume mixer applet that runs in the system tray.
License:        GPL-3.0-or-later
URL:            https://github.com/nicklan/pnmixer
Source0:        pnmixer-0.7.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
GTK volume mixer applet that runs in the system tray.

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
%license COPYING
%doc README.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.2-1
- Initial openEuler RISC-V package from the full package inventory.
