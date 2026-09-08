# SPDX-License-Identifier: Apache-2.0
Name:           rapidobj
Version:        1.1
Release:        2%{?dist}
Summary:        A fast, header-only, C++17 library for parsing Wavefront .obj files.
License:        MIT
URL:            https://github.com/guybrush77/rapidobj
Source0:        rapidobj-1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast, header-only, C++17 library for parsing Wavefront .obj files.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DRAPIDOBJ_BuildExamples=ON \
  -DRAPIDOBJ_BuildTests=OFF \
  -DRAPIDOBJ_BuildTools=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
cat > rapidobj-smoke.obj <<'EOF'
v 0 0 0
v 1 0 0
v 0 1 0
f 1 2 3
EOF
%{_vpath_builddir}/example/readobj/readobj rapidobj-smoke.obj | \
  grep -Fx 'Triangles: 1'

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-2
- Use the openEuler out-of-source CMake macro and exercise the parser example.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package from the full package inventory.
