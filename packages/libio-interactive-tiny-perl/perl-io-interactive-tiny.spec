# SPDX-License-Identifier: Apache-2.0
Name:           perl-io-interactive-tiny
Version:        0.2
Release:        1%{?dist}
Summary:        Check whether a Perl process is connected to an interactive terminal
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IO-Interactive-Tiny
Source0:        IO-Interactive-Tiny-0.2.tar.gz
Patch0:         0001-retain-io-interactive-notice.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  util-linux
Requires:       perl

%description
IO::Interactive::Tiny checks whether the selected Perl output handle and
input are connected to a terminal, without the larger module's dependencies.

%prep
%autosetup -n IO-Interactive-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1
# Run the same original test in a PTY for the terminal assertions that
# the default non-interactive harness skips.
/usr/bin/script -q -e -c '%{__perl} -Mblib t/01.is_interactive.t' /dev/null </dev/null

%files
%license README IO-INTERACTIVE-NOTICE
%doc Changes
%{perl_vendorlib}/IO/Interactive/Tiny.pm
%{perl_vendorlib}/IO/Interactive/Tiny.pod
%{_mandir}/man3/IO::Interactive::Tiny.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Package IO::Interactive::Tiny with its original terminal and non-terminal tests.
