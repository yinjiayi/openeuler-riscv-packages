# SPDX-License-Identifier: Apache-2.0
Name:           tree
Version:        2.3.2
Release:        1%{?dist}
Summary:        Display directory contents in a tree-like format
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://oldmanprogrammer.net/source.php?dir=projects/tree
Source0:        tree-%{version}.tgz

BuildRequires:  gcc
BuildRequires:  make

%description
Tree recursively lists directory contents and renders the hierarchy as text,
JSON, XML, HTML, or other supported output formats.

%package help
Summary:        Documentation for tree
BuildArch:      noarch

%description help
The tree manual page and upstream release documentation.

%prep
%autosetup -p1

%build
%make_build \
  CFLAGS="%{optflags} -std=c11 -Wpedantic -Wall -Wextra -Wstrict-prototypes -Wshadow -Wconversion -Wdiscarded-qualifiers" \
  CPPFLAGS="-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" \
  LDFLAGS="%{build_ldflags}"

%install
%make_install \
  DESTDIR=%{buildroot}%{_bindir} \
  MANDIR=%{buildroot}%{_mandir}

%check
./tree --version | grep -F 'tree v2.3.2'
check_dir=$(mktemp -d)
mkdir -p "$check_dir/alpha/beta"
printf 'RVA23\n' >"$check_dir/alpha/beta/payload.txt"
./tree -afi --noreport "$check_dir" >"$check_dir/result.txt"
grep -F "$check_dir/alpha/beta/payload.txt" "$check_dir/result.txt"
rm -rf "$check_dir"

%files
%license LICENSE
%{_bindir}/tree

%files help
%license LICENSE
%doc CHANGES README
%{_mandir}/man1/tree.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.2-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
