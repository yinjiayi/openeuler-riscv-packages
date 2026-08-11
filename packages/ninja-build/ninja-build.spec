# SPDX-License-Identifier: Apache-2.0
Name:           ninja-build
Version:        1.13.2
Release:        1%{?dist}
Summary:        Small build system focused on speed
License:        Apache-2.0
URL:            https://ninja-build.org
Source0:        ninja-build-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Ninja is a small build system designed to execute build graphs quickly while
leaving high-level project generation to tools such as CMake and Meson.

%prep
%autosetup -n ninja-%{version} -p1

%build
%cmake_conf \
  -DBUILD_TESTING=ON \
  -DNINJA_BUILD_BINARY=ON
%cmake_build

%install
%cmake_install
install -Dpm0644 misc/bash-completion \
  %{buildroot}%{_datadir}/bash-completion/completions/ninja
install -Dpm0644 misc/zsh-completion \
  %{buildroot}%{_datadir}/zsh/site-functions/_ninja

%check
# SetWithLots intentionally creates 1025 concurrent children to exercise the
# ppoll path.  Under user-mode QEMU each guest child consumes host thread/PID
# capacity, so GitHub-hosted runners can exhaust the cgroup limit even though
# RLIMIT_NOFILE is high.  Cap that limit so the test's own guarded skip path is
# used; every other upstream GTest case still runs.
ulimit -n 1024
%ctest -- -j1

%files
%license COPYING
%doc README.md
%{_bindir}/ninja
%{_datadir}/bash-completion/completions/ninja
%{_datadir}/zsh/site-functions/_ninja

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13.2-1
- Initial openEuler RISC-V package based on Fedora 44 and corroborating release evidence.
