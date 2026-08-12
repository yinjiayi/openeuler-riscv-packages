# SPDX-License-Identifier: Apache-2.0
Name:           jo
Version:        1.9
Release:        1%{?dist}
Summary:        Create JSON objects from the shell
License:        GPL-2.0-or-later AND MIT AND LicenseRef-Public-Domain
URL:            https://github.com/jpmens/jo
Source0:        jo-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed

%description
jo is a small command-line utility that creates JSON objects and arrays from
shell arguments, files, standard input, and pipelines.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/jo
%{_datadir}/bash-completion/completions/jo.bash
%{_datadir}/zsh/site-functions/_jo
%{_mandir}/man1/jo.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9-1
- Initial openEuler RISC-V package with all 27 upstream TAP tests.
