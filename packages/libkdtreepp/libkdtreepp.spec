# SPDX-License-Identifier: Apache-2.0
Name:           libkdtree++
Version:        0.7.5
Release:        1%{?dist}
Summary:        Header-only C++ kd-tree container
License:        Artistic-2.0
URL:            https://github.com/nvmd/libkdtree
Source0:        libkdtreepp-0.7.5.tar.gz
Patch0:         0001-guard-empty-example-tree.patch
Patch1:         0002-preserve-installed-header-directory.patch
BuildArch:      noarch
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  grep
BuildRequires:  patch
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       grep

%description
A header-only C++ template container for kd-tree sorting, nearest-neighbor
and box-range queries. Includes original example/test sources and an offline
installed-header validation runner. Python bindings remain upstream-default OFF.

%prep
%setup -q -n libkdtree-9b0cbb264393cbd40641256668393ef5bdbfe242
mkdir upstream-original
cp -p examples/test_hayne.cpp examples/test_kdtree.cpp examples/test_find_within_range.cpp upstream-original/
%patch0 -p1
%patch1 -p1

%build
cmake -S . -B build \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS:STRING="%{optflags} -UNDEBUG"
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libkdtreepp/examples %{buildroot}%{_datadir}/libkdtreepp/upstream-original
install -m 0644 examples/test_hayne.cpp examples/test_kdtree.cpp examples/test_find_within_range.cpp %{buildroot}%{_datadir}/libkdtreepp/examples/
install -m 0644 upstream-original/*.cpp %{buildroot}%{_datadir}/libkdtreepp/upstream-original/
cat > %{buildroot}%{_datadir}/libkdtreepp/consumer.cpp <<'EOF'
#include <kdtree++/kdtree.hpp>
#include <array>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <vector>
static void require(bool ok, const char *why) {
  if (!ok) { std::cerr << why << '\n'; std::exit(1); }
}
int main() {
  typedef std::array<double,2> Point;
  typedef KDTree::KDTree<2,Point> Tree;
  Tree t;
  Point q={{2,4}};
  require(t.empty() && t.find_nearest(q).first == t.end(), "empty-tree sentinel");
  Point p0={{0,0}}, p1={{3,4}}, p2={{10,0}}, p3={{-3,-4}};
  t.insert(p0); t.insert(p1); t.insert(p2); t.insert(p3); t.optimise();
  require(t.size()==4 && !t.empty(), "insert count");
  require(t.find_exact(p1)!=t.end() && *t.find_exact(p1)==p1, "exact lookup");
  std::pair<Tree::const_iterator,double> n=t.find_nearest(q);
  require(n.first!=t.end() && *n.first==p1 && n.second==1.0, "nearest point/distance");
  require(t.find_nearest(q,0.5).first==t.end(), "bounded miss");
  n=t.find_nearest(p2,0.0);
  require(n.first!=t.end() && *n.first==p2 && n.second==0.0, "zero-radius hit");
  std::vector<Point> found;
  t.find_within_range(p0,4.0,std::back_inserter(found));
  require(found.size()==3 && t.count_within_range(p0,4.0)==3, "inclusive box range");
  Tree copy(t), assigned; assigned=t;
  require(copy.size()==4 && assigned.size()==4, "copy/assignment count");
  t.erase_exact(p1); t.optimise();
  require(t.size()==3 && t.find_exact(p1)==t.end(), "erase exact");
  require(copy.find_exact(p1)!=copy.end() && assigned.find_exact(p1)!=assigned.end(), "copy independence");
  size_t forward=0, backward=0;
  for (Tree::const_iterator i=t.begin();i!=t.end();++i) ++forward;
  for (Tree::const_reverse_iterator i=t.rbegin();i!=t.rend();++i) ++backward;
  require(forward==3 && backward==3, "bidirectional iteration");
  t.clear(); require(t.empty() && t.begin()==t.end(), "clear");
  std::cout << "libkdtreepp downstream consumer passed\n";
}
EOF
cat > %{buildroot}%{_datadir}/libkdtreepp/run-tests.sh <<'EOF'
#!/bin/bash
set -euo pipefail
root=${1:-/}
root=${root%%/}
data="$root/usr/share/libkdtreepp"
include="$root/usr/include"
cd "$data"
sha256sum --check SHA256SUMS
(cd "$include" && sha256sum --check "$data/HEADERS.SHA256SUMS")
work=$(mktemp -d)
trap 'rmdir "$work" 2>/dev/null || true' EXIT
for name in test_hayne test_kdtree test_find_within_range; do
  "${CXX:-g++}" ${CXXFLAGS:--O2 -g} -UNDEBUG -I"$include" "examples/$name.cpp" -o "$work/$name"
  "$work/$name" > "$work/$name.log" 2>&1
  if grep -E 'SHOULD NOT HAVE FOUND|^fail,|^ERROR|^Error:' "$work/$name.log"; then
    cat "$work/$name.log"; exit 1
  fi
  if test "$name" = test_hayne; then
    grep -F 'THIS IS THE BUG TRIGGER' "$work/$name.log"
    grep -F '  find() double-check passed.' "$work/$name.log"
    test "$(grep -c ' : Deleting ' "$work/$name.log")" -eq 255
  fi
  if test "$name" = test_kdtree; then
    test "$(grep -c 'iterator walked through 6 nodes in total' "$work/$name.log")" -eq 8
  fi
  rm "$work/$name" "$work/$name.log"
done
"${CXX:-g++}" ${CXXFLAGS:--O2 -g} -UNDEBUG -I"$include" consumer.cpp -o "$work/consumer"
"$work/consumer"
rm "$work/consumer"
printf '%s\n' 'libkdtreepp original three programs and downstream consumer passed'
EOF
chmod 0755 %{buildroot}%{_datadir}/libkdtreepp/run-tests.sh
(cd %{buildroot}%{_datadir}/libkdtreepp && sha256sum examples/*.cpp upstream-original/*.cpp consumer.cpp run-tests.sh > SHA256SUMS)
(cd %{buildroot}%{_includedir} && sha256sum kdtree++/*.hpp > %{buildroot}%{_datadir}/libkdtreepp/HEADERS.SHA256SUMS)

%check
for name in test_hayne test_kdtree test_find_within_range; do
  build/examples/$name > "build/$name.log" 2>&1
done
%{buildroot}%{_datadir}/libkdtreepp/run-tests.sh %{buildroot}

%files
%license COPYING
%doc README.md AUTHORS NEWS ChangeLog doc/index.txt
%dir %{_includedir}/kdtree++
%{_includedir}/kdtree++/*.hpp
%{_datadir}/libkdtreepp

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.7.5-1
- Import fixed official source, retain default examples, and correct example sentinel/install path.
