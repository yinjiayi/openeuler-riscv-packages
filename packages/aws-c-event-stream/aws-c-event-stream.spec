# SPDX-License-Identifier: Apache-2.0
Name:           aws-c-event-stream
Version:        0.7.1
Release:        1%{?dist}
Summary:        C99 implementation of the vnd.amazon.eventstream content-type
License:        Apache-2.0
URL:            https://github.com/awslabs/aws-c-event-stream
Source0:        aws-c-event-stream-0.7.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C99 implementation of the vnd.amazon.eventstream content-type

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.1-1
- Initial openEuler RISC-V package from the full package inventory.
