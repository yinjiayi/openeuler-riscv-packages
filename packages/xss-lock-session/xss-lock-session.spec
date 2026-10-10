# SPDX-License-Identifier: Apache-2.0
Name:           xss-lock-session
Version:        0.3.0
Release:        1%{?dist}
Summary:        Forked version of xss lock that allows specifying a session
License:        MIT
URL:            https://github.com/xdbob/xss-lock
Source0:        xss-lock-session-0.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Forked version of xss lock that allows specifying a session

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
