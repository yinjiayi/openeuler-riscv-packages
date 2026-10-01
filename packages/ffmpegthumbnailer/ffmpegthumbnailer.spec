# SPDX-License-Identifier: Apache-2.0
Name:           ffmpegthumbnailer
Version:        2.3.0
Release:        1%{?dist}
Summary:        fast and lightweight video thumbnailer FFmpegthumbnailer is a lightweight video thumbnailer that can be used by file managers to create thumbnails for your
License:        GPL-2.0-or-later
URL:            https://github.com/dirkvdb/ffmpegthumbnailer
Source0:        ffmpegthumbnailer-2.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
fast and lightweight video thumbnailer FFmpegthumbnailer is a lightweight video thumbnailer that can be used by file managers to create thumbnails for your

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
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
