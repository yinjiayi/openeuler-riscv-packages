# SPDX-License-Identifier: Apache-2.0
Name:           xbanish
Version:        1.8
Release:        1%{?dist}
Summary:        Hide the X11 mouse cursor while typing
License:        ISC
URL:            https://github.com/jcs/xbanish
Source0:        xbanish-1.8.tar.gz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  make

%description
xbanish hides the X11 mouse cursor while the keyboard is in use and restores
it when the pointer moves.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{optflags} -Wall -Wunused -Wmissing-prototypes -Wstrict-prototypes' \
  X11BASE=%{_prefix}

%install
%make_install \
  PREFIX=%{_prefix} \
  MANDIR=%{_mandir}/man1 \
  X11BASE=%{_prefix} \
  INSTALL_PROGRAM='install -m 0755'

%check
test -x xbanish

%files
%license LICENSE
%doc README.md
%{_bindir}/xbanish
%{_mandir}/man1/xbanish.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package.

