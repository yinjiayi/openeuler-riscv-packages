# SPDX-License-Identifier: Apache-2.0
Name:           specgram
Version:        0.9.3
Release:        1%{?dist}
Summary:        Small program that computes and plots spectrograms, either in a live window or to disk, with support for stdin input.
License:        MIT
URL:            https://github.com/rimio/specgram
Source0:        specgram-0.9.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Small program that computes and plots spectrograms, either in a live window or to disk, with support for stdin input.

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.3-1
- Initial openEuler RISC-V package from the full package inventory.
