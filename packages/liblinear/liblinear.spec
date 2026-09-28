# SPDX-License-Identifier: Apache-2.0
Name:           liblinear
Version:        2.50
Release:        1%{?dist}
%global upstream_commit 491c9f1188b97ba70847c70a68be363d186ddf9d
Summary:        Linear classification and regression library
License:        BSD-3-Clause
URL:            https://www.csie.ntu.edu.tw/~cjlin/liblinear/
Source0:        liblinear-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
LIBLINEAR implements large-scale linear classification, regression, and
outlier detection. This package includes the shared library and the upstream
training and prediction command-line tools under unambiguous names.

%package devel
Summary:        Development files for LIBLINEAR
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
The public C API header, unversioned linker name, and pkg-config metadata
for applications using LIBLINEAR.

%prep
%autosetup -n liblinear-%{upstream_commit} -p1

%build
# Upstream's Makefile fixes optimization flags. Override them with the target
# RPM flags while retaining its bundled PIC BLAS implementation and SONAME.
%make_build all lib CFLAGS='%{optflags} -fPIC' \
  SHARED_LIB_FLAG='-shared %{build_ldflags} -Wl,-soname,liblinear.so.6'
ln -s liblinear.so.6 liblinear.so

%install
install -Dpm0755 liblinear.so.6 %{buildroot}%{_libdir}/liblinear.so.6
ln -s liblinear.so.6 %{buildroot}%{_libdir}/liblinear.so
install -Dpm0644 linear.h %{buildroot}%{_includedir}/linear.h
install -Dpm0755 train %{buildroot}%{_bindir}/liblinear-train
install -Dpm0755 predict %{buildroot}%{_bindir}/liblinear-predict
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/liblinear.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: liblinear
Description: Linear classification and regression library
Version: %{version}
Libs: -L${libdir} -llinear
Cflags: -I${includedir}
EOF

%check
# Upstream ships no registered test target. Exercise its documented sample
# workflow, a five-fold cross-validation pass, and the shared C API.
./train -s 0 -c 1 heart_scale heart_scale.model
./predict heart_scale heart_scale.model heart_scale.predictions
awk 'NR == FNR { expected[NR] = $1; n = NR; next }
     { if ($1 == expected[FNR]) good++; m = FNR }
     END { if (n != 270 || m != n || good < 200) exit 1 }' \
  heart_scale heart_scale.predictions
./train -s 0 -v 5 heart_scale
cat > liblinear-api-check.cpp <<'EOF'
#include <linear.h>
int main() {
    if (LIBLINEAR_VERSION != 250 || liblinear_version != 250) return 1;
    model *trained = load_model("heart_scale.model");
    if (!trained) return 2;
    int ok = get_nr_feature(trained) > 0 && get_nr_class(trained) == 2;
    free_and_destroy_model(&trained);
    return ok ? 0 : 3;
}
EOF
g++ %{optflags} -I. liblinear-api-check.cpp -L. -Wl,-rpath,$PWD \
  -llinear -o liblinear-api-check
./liblinear-api-check

%files
%license COPYRIGHT
%doc README
%{_libdir}/liblinear.so.6
%{_bindir}/liblinear-train
%{_bindir}/liblinear-predict

%files devel
%license COPYRIGHT
%{_includedir}/linear.h
%{_libdir}/liblinear.so
%{_libdir}/pkgconfig/liblinear.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.50-1
- Initial openEuler RISC-V package with training, prediction, and API checks.
