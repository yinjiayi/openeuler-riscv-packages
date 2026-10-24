# SPDX-License-Identifier: Apache-2.0
Name:           plasma6-runners-emojirunner
Version:        3.0.5
Release:        1%{?dist}
Summary:        Search for emojis in Krunner and copy/paste them
License:        GPL-3.0-or-later
URL:            https://github.com/alex1701c/EmojiRunner
Source0:        plasma6-runners-emojirunner-3.0.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Search for emojis in Krunner and copy/paste them

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
