# SPDX-License-Identifier: Apache-2.0
Name:           hstr
Version:        3.2
Release:        1%{?dist}
Summary:        Bash and Zsh shell history suggest box - easily view, navigate, search and manage your command history.
License:        Apache-2.0
URL:            https://github.com/dvorka/hstr
Source0:        hstr-3.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Bash and Zsh shell history suggest box - easily view, navigate, search and manage your command history.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-1
- Initial openEuler RISC-V package from the full package inventory.
