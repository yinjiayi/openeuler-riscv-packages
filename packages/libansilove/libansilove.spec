# SPDX-License-Identifier: Apache-2.0
Name:           libansilove
Version:        1.4.2
Release:        1%{?dist}
Summary:        ANSI and text-art to PNG conversion library
License:        BSD-2-Clause
URL:            https://github.com/ansilove/libansilove
Source0:        libansilove-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gd-devel
BuildRequires:  make

%description
libansilove converts ANSI, ASCII, and other text-art formats to PNG images
using the GD graphics library.

%package devel
Summary:        Header, static library, and linker name for libansilove
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for C applications that use libansilove to render text art.

%prep
%autosetup -p1

%build
%cmake_conf
%cmake_build

%install
%cmake_install

%check
# Upstream has no executable test target. Render a PNG through its public API.
cat > api-check.c <<'EOF'
#include <ansilove.h>

int main(int argc, char **argv) {
  struct ansilove_ctx ctx;
  struct ansilove_options options;
  if (argc != 3 || ansilove_init(&ctx, &options) != 0)
    return 1;
  int ok = ansilove_loadfile(&ctx, argv[1]) == 0 &&
           ansilove_ansi(&ctx, &options) == 0 &&
           ansilove_savefile(&ctx, argv[2]) == 0;
  ansilove_clean(&ctx);
  return ok ? 0 : 1;
}
EOF
%{__cc} %{build_cflags} -Iinclude api-check.c -L%{_vpath_builddir} -lansilove %{build_ldflags} -o api-check
printf 'Hello, RVA23!\n' > fixture.ans
LD_LIBRARY_PATH=%{_vpath_builddir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} ./api-check fixture.ans fixture.png
test "$(od -An -tx1 -N8 fixture.png | tr -d ' \n')" = 89504e470d0a1a0a

%files
%license LICENSE
%doc AUTHORS ChangeLog README.md THANKS
%{_libdir}/libansilove.so.1*

%files devel
%license LICENSE
%{_includedir}/ansilove.h
%{_libdir}/libansilove.so
%{_libdir}/libansilove-static.a
%{_mandir}/man3/libansilove.3*
%{_mandir}/man3/ansilove_*.3*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial package from the official release with a PNG rendering check.
