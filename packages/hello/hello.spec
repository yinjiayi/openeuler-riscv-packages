# SPDX-License-Identifier: Apache-2.0
Name:           hello
Version:        2.12.3
Release:        1%{?dist}
Summary:        A Friendly Greeting Program
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/hello/
Source0:        hello-2.12.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  texinfo


%description
GNU Hello prints a familiar greeting and provides the standard GNU Hello
command-line example program.

%prep
%autosetup -n hello-%{version} -p1

%build
%configure --disable-nls
%make_build

%install
%make_install
# install-info owns this generated directory index; individual RPMs must not.
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/hello
%{_infodir}/hello.info*
%{_mandir}/man1/hello.1*

%changelog
* Sun Aug 23 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.3-1
- Package GNU Hello 2.12.3 for openEuler RISC-V.
