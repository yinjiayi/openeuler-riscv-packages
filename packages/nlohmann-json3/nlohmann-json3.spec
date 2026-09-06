# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           nlohmann-json3
Version:        3.12.0
Release:        1%{?dist}
Summary:        Header-only JSON library for modern C++
License:        MIT AND CC0-1.0
URL:            https://json.nlohmann.me/
Source0:        nlohmann-json3-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
nlohmann/json provides a header-only C++ JSON implementation with STL-like
containers, JSON Pointer, JSON Patch, and binary serialization formats.

%package devel
Summary:        Development files for nlohmann/json
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Provides:       json-devel = %{version}-%{release}
Provides:       json-static = %{version}-%{release}
Provides:       nlohmann-json-devel = %{version}-%{release}
Provides:       nlohmann-json-static = %{version}-%{release}
Provides:       nlohmann-json3-dev = %{version}-%{release}
Provides:       nlohmann_json-devel = %{version}-%{release}
Provides:       nlohmann_json-static = %{version}-%{release}
Provides:       cmake(nlohmann_json) = %{version}
Provides:       pkgconfig(nlohmann_json) = %{version}
Provides:       bundled(hedley) = 15
Requires:       libstdc++-devel%{?_isa}
Requires:       pkgconf

%description devel
This package contains the multi-header nlohmann/json C++ interface together
with CMake and pkg-config metadata. No runtime library is required.

%prep
%autosetup -p1 -n json

%build
%cmake_conf \
  -DJSON_BuildTests=OFF \
  -DJSON_Install=ON \
  -DJSON_MultipleHeaders=ON
%cmake_build

%install
%cmake_install

%check
hedley_version=$(awk '
/^[[:blank:]]*#[[:blank:]]*define[[:blank:]]+JSON_HEDLEY_VERSION[[:blank:]]/ {
  print $NF
}' include/nlohmann/thirdparty/hedley/hedley.hpp)
test "$hedley_version" = 15

mkdir consumer
cat > consumer/CMakeLists.txt <<'EOF'
cmake_minimum_required(VERSION 3.12)
project(nlohmann_json_consumer LANGUAGES CXX)
find_package(nlohmann_json 3.12.0 EXACT CONFIG REQUIRED)
add_executable(nlohmann-json3-check main.cpp)
target_compile_features(nlohmann-json3-check PRIVATE cxx_std_17)
target_link_libraries(nlohmann-json3-check PRIVATE nlohmann_json::nlohmann_json)
EOF
cat > consumer/main.cpp <<'EOF'
#include <nlohmann/json.hpp>

#include <cstdint>
#include <string>
#include <vector>

int main() {
    using nlohmann::json;
    const json document = json::parse(
        R"({"name":"openEuler","nested":{"value":7},"items":[1,2,3]})");
    const auto pointer = json::json_pointer("/nested/value");
    if (document.at(pointer) != 7 || document.at("items").size() != 3) {
        return 1;
    }

    const json patch = json::parse(
        R"([{"op":"replace","path":"/nested/value","value":23}])");
    const json changed = document.patch(patch);
    const std::vector<std::uint8_t> cbor = json::to_cbor(changed);
    if (json::from_cbor(cbor) != changed || changed.at(pointer) != 23) {
        return 1;
    }

    const json invalid = json::parse("{", nullptr, false);
    return invalid.is_discarded() && changed.dump().find("openEuler") != std::string::npos
               ? 0
               : 1;
}
EOF
cmake -S consumer -B consumer-build \
  -DCMAKE_PREFIX_PATH=%{buildroot}%{_prefix}
cmake --build consumer-build --verbose
consumer-build/nlohmann-json3-check

test "$(PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig \
  pkg-config --modversion nlohmann_json)" = %{version}

%files devel
%license LICENSE.MIT
%{_includedir}/nlohmann/
%{_datadir}/cmake/nlohmann_json/
%{_datadir}/pkgconfig/nlohmann_json.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.12.0-1
- Add the official header-only release with CMake and pkg-config integration.
- Provide compatible nlohmann-json3, json, and nlohmann_json development names.
