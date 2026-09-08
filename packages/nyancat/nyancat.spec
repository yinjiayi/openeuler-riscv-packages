# SPDX-License-Identifier: Apache-2.0
Name:           nyancat
Version:        1.5.2
Release:        1%{?dist}
Summary:        Nyan Cat animation rendered in a terminal
License:        NCSA
URL:            https://github.com/klange/nyancat
Source0:        nyancat-1.5.2.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
nyancat renders the Nyan Cat animation with ANSI color sequences in a terminal.

%prep
%autosetup -p1

%build
%make_build CC=%{__cc} CFLAGS='%{optflags} -Wall -Wextra -std=c99 -pedantic'

%install
install -Dpm0755 src/nyancat %{buildroot}%{_bindir}/nyancat
install -Dpm0644 nyancat.1 %{buildroot}%{_mandir}/man1/nyancat.1

%check
%make_build check
./src/nyancat -h 2>&1 | grep -i 'usage'

%files
%license src/nyancat.c
%doc CHANGELOG README.md
%{_bindir}/nyancat
%{_mandir}/man1/nyancat.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.2-1
- Initial openEuler RISC-V package.

