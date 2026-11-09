# SPDX-License-Identifier: Apache-2.0
Name:           bats
Version:        1.14.0
Release:        1%{?dist}
Summary:        Bash Automated Testing System
License:        MIT
URL:            https://bats-core.readthedocs.io/
Source0:        bats-core-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  grep
BuildRequires:  ncurses
BuildRequires:  parallel
BuildRequires:  procps-ng
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       ncurses
Requires:       parallel

%description
Bats is a TAP-compliant testing framework for Bash. It provides a simple and
repeatable way to verify that Unix programs behave as expected.

%prep
%autosetup -n bats-core-%{version} -p1

%build
:

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_libexecdir}/bats-core \
  %{buildroot}%{_prefix}/lib/bats-core %{buildroot}%{_mandir}/man1 \
  %{buildroot}%{_mandir}/man7
install -pm0755 bin/bats %{buildroot}%{_bindir}/bats
install -pm0755 libexec/bats-core/* %{buildroot}%{_libexecdir}/bats-core/
install -pm0755 lib/bats-core/* %{buildroot}%{_prefix}/lib/bats-core/
install -pm0644 man/bats.1 %{buildroot}%{_mandir}/man1/
install -pm0644 man/bats.7 %{buildroot}%{_mandir}/man7/

%check
bin/bats --tap test

%files
%license LICENSE.md
%doc AUTHORS README.md docs/CHANGELOG.md
%{_bindir}/bats
%{_libexecdir}/bats-core/
%{_prefix}/lib/bats-core/
%{_mandir}/man1/bats.1*
%{_mandir}/man7/bats.7*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14.0-1
- Update the openEuler RISC-V bats package to upstream bats-core 1.14.0.
