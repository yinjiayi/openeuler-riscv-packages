# SPDX-License-Identifier: Apache-2.0
Name:           dictpopup
Version:        0.3.2
Release:        8%{?dist}
Summary:        A Japanese popup dictionary working on mouse selection with Anki integration
License:        GPL-3.0-or-later
URL:            https://github.com/Ajatt-Tools/dictpopup
Source0:        dictpopup-0.3.2.tar.gz
Patch0:         0001-cmake-do-not-force-native-architecture.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  gtk3-devel
BuildRequires:  libcurl-devel
BuildRequires:  lmdb-devel
BuildRequires:  libnotify-devel
BuildRequires:  libzip-devel
BuildRequires:  make
BuildRequires:  mecab-devel

%description
A Japanese popup dictionary working on mouse selection with Anki integration

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
sed -i '\|^%{_mandir}/man1/|d' %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md
%{_mandir}/man1/dictpopup*.1*

%changelog
* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-8
- List man pages after RPM's compression step instead of using stale generated names.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-7
- Regenerate the architecture-flags patch with strict GNU patch context.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-6
- Preserve the openEuler RVA23 target flags instead of forcing build-host native tuning.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-5
- Add the gperf generator required during CMake configuration.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-4
- Add the MeCab development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-3
- Add the LMDB development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-2
- Add the official libcurl development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the GTK 3 development files required by pkg-config.
- Add the libnotify development files required by pkg-config.
