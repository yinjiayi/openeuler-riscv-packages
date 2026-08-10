# SPDX-License-Identifier: Apache-2.0
Name:           cli11
Version:        2.7.2
Release:        1%{?dist}
Summary:        Header-only command-line parser for C++11 and newer
License:        BSD-3-Clause
URL:            https://github.com/CLIUtils/CLI11
Source0:        cli11-2.7.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make


%description
CLI11 is a header-only command-line parser for C++11 and newer.

%prep
%autosetup -p1 -n CLI11-%{version}

%build
%cmake_conf \
  -DCLI11_BUILD_TESTS=OFF \
  -DCLI11_BUILD_EXAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
cat > cli11-smoke.cpp <<'CPP'
#include <CLI/CLI.hpp>
int main(int argc, char **argv) {
  CLI::App app{"cli11 build smoke"};
  int value = 0;
  app.add_option("--value", value)->required();
  CLI11_PARSE(app, argc, argv);
  return value == 42 ? 0 : 1;
}
CPP
g++ -std=c++14 -Iinclude cli11-smoke.cpp -o cli11-smoke
./cli11-smoke --value 42

%files
%license LICENSE
%doc README.md
%{_includedir}/CLI/
%{_datadir}/cmake/CLI11/
%{_datadir}/pkgconfig/CLI11.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.2-1
- Initial openEuler RISC-V package.
