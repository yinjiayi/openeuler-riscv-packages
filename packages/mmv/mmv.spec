# SPDX-License-Identifier: Apache-2.0
Name:           mmv
Version:        2.10
Release:        1%{?dist}
Summary:        Safely move and copy multiple files by wildcard
License:        GPL-3.0-or-later
URL:            https://github.com/rrthomas/mmv
Source0:        mmv-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
mmv moves, copies, or links many files with wildcard source patterns and
capture-based destination patterns while checking the entire operation
before modifying files.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
# The release registers no automated cases; keep make check and verify a
# deterministic wildcard rename in an isolated directory.
%make_build check
check_dir=$(mktemp -d)
trap 'rm -rf "$check_dir"' EXIT
printf 'mmv-riscv64\n' > "$check_dir/old.txt"
mmv_build="$PWD/mmv"
(
  cd "$check_dir"
  "$mmv_build" 'old.*' 'new.#1'
  test ! -e old.txt
  test "$(cat new.txt)" = mmv-riscv64
)

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_bindir}/mmv
%{_bindir}/mcp
%{_bindir}/mln
%{_bindir}/mad
%{_docdir}/mmv/
%{_mandir}/man1/mmv.1*
%{_mandir}/man1/mcp.1*
%{_mandir}/man1/mln.1*
%{_mandir}/man1/mad.1*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.10-1
- Package the official SHA-256-pinned mmv 2.10 release for RVA23.
