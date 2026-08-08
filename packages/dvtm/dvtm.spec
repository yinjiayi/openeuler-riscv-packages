# SPDX-License-Identifier: Apache-2.0
Name:           dvtm
Version:        0.15
Release:        1%{?dist}
Summary:        Dynamic virtual terminal manager
License:        MIT AND ISC
URL:            https://brain-dump.org/projects/dvtm
Source0:        dvtm-0.15.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
dvtm is a tiling window manager for the console. It manages multiple virtual
terminals in one terminal session using an ncurses interface.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{optflags} -std=c99 -I. -DVERSION=\"%{version}\" -DNDEBUG -D_POSIX_C_SOURCE=200809L -D_XOPEN_SOURCE=700 -D_XOPEN_SOURCE_EXTENDED' \
  LDFLAGS='-lutil -lncursesw'

%install
%make_install \
  PREFIX=%{_prefix} \
  STRIP=: \
  TERMINFO=%{buildroot}%{_datadir}/terminfo

%check
./dvtm -v | grep -F 'dvtm-%{version}'

%files
%license LICENSE
%doc README.md
%{_bindir}/dvtm
%{_bindir}/dvtm-status
%{_mandir}/man1/dvtm.1*
%{_datadir}/terminfo/*/dvtm*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Initial openEuler RISC-V package.
