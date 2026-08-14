# SPDX-License-Identifier: Apache-2.0
Name:           which
Version:        2.25
Release:        1%{?dist}
Summary:        Display the full path of commands
License:        GPL-3.0-or-later
URL:            https://savannah.gnu.org/projects/which/
Source0:        which-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  readline-devel
Requires:       coreutils

%description
GNU Which searches PATH and prints the full pathname of each requested
executable. It can also inspect aliases and shell functions supplied on
standard input.

%package help
Summary:        Documentation for GNU Which
BuildArch:      noarch

%description help
The GNU Which manual page, Info document, and usage examples.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%{_bindir}/which

%files help
%license COPYING
%doc AUTHORS EXAMPLES NEWS README README.alias
%{_infodir}/which.info*
%{_mandir}/man1/which.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.25-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
