# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-CaptureOutput
Version:        1.1105
Release:        1%{?dist}
Summary:        Perl capture of standard output and error
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IO-CaptureOutput
Source0:        IO-CaptureOutput-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
IO::CaptureOutput is a deprecated compatibility module for capturing
standard output and error from Perl code and subprocesses.

%prep
%autosetup -n IO-CaptureOutput-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/IO/CaptureOutput.pm
%{_mandir}/man3/IO::CaptureOutput.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1105-1
- Package official CPAN release with original tests.
