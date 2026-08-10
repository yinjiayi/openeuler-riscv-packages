# SPDX-License-Identifier: Apache-2.0
Name:           abduco
Version:        0.6
Release:        1%{?dist}
Summary:        Session attach and detach support for terminal programs
License:        ISC
URL:            https://brain-dump.org/projects/abduco
Source0:        abduco-0.6.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
abduco provides session attach and detach support so a command can keep
running independently from its controlling terminal.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{optflags} -std=c99 -pedantic -Wall -I. -DVERSION=\"%{version}\" -DNDEBUG -D_POSIX_C_SOURCE=200809L -D_XOPEN_SOURCE=700' \
  LDFLAGS='%{__global_ldflags} -lutil'

%install
%make_install PREFIX=%{_prefix} STRIP=:

%check
./abduco -v | grep -F 'abduco-%{version}'

%files
%license LICENSE
%doc README.md
%{_bindir}/abduco
%{_mandir}/man1/abduco.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6-1
- Initial openEuler RISC-V package.
