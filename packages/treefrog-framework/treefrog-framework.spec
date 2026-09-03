# SPDX-License-Identifier: Apache-2.0
Name:           treefrog-framework
Version:        2.12.0
Release:        7%{?dist}
Summary:        High-speed C++ MVC Framework for Web Application
License:        BSD-3-Clause
URL:            https://github.com/treefrogframework/treefrog-framework
Source0:        treefrog-framework-2.12.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  liburing-devel
BuildRequires:  make
BuildRequires:  memcached
BuildRequires:  mongo-c-driver-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  redis

%description
High-speed C++ MVC Framework for Web Application

%prep
%autosetup -p1

%build
%set_build_flags
./configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir}/treefrog \
  --datadir=%{_datadir}/treefrog \
  --enable-shared-mongoc
%make_build -C src
(
  cd tools
  qmake6 -recursive \
    CONFIG+=release \
    target.path="%{_bindir}" \
    header.path="$PWD/../include" \
    datadir="%{_datadir}/treefrog" \
    lib.path="$PWD/../src"
)
%make_build -C tools

%install
%make_install -C src
%make_install -C tools
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
mkdir -p .test-services
redis-server \
  --bind 127.0.0.1 \
  --protected-mode no \
  --save "" \
  --appendonly no \
  --daemonize yes \
  --pidfile "$PWD/.test-services/redis.pid"
memcached \
  -u root \
  -l 127.0.0.1 \
  -p 11211 \
  -d \
  -P "$PWD/.test-services/memcached.pid"
cleanup_services() {
  for pid_file in "$PWD/.test-services/"*.pid; do
    test -s "$pid_file" || continue
    xargs kill < "$pid_file" || :
  done
}
trap cleanup_services EXIT
sleep 1
for pid_file in "$PWD/.test-services/"*.pid; do
  test -s "$pid_file"
  xargs kill -0 < "$pid_file"
done
export LD_LIBRARY_PATH="$PWD/src${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
./src/test/testall.sh
(
  cd tools/tmake/test
  qmake6 tmaketest.pro
  %make_build
  ./tmaketest.sh
)

%files -f %{name}.files
%license copyright
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-7
- Build the command-line tools against the just-built framework headers and library.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-6
- Allow the complete TreeFrog build and test suites 180 minutes under QEMU.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-5
- Build and install the src and tools projects, then run the upstream test suites.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-4
- Use the repository MongoDB C driver instead of rebuilding the bundled copy.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-3
- Add the Qt 6 QML development module required by TreeFrog's qmake project.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-2
- Use TreeFrog's supported configure interface and declare its build tools.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-1
- Initial openEuler RISC-V package from the full package inventory.
