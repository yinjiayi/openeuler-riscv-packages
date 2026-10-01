# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Format
Version:        0.63
Release:        1%{?dist}
Summary:        Format and wrap text in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Format
Source0:        Text-Format-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl-generators

%description
Text::Format supplies configurable text wrapping, justification and related
formatting helpers.

%prep
%autosetup -n Text-Format-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default upstream t/ suites and 15 assertions.
./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Format.pm
%{_mandir}/man3/Text::Format.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.63-1
- Package official CPAN release with all default tests and wrap smoke.
