# SPDX-License-Identifier: Apache-2.0
Name:           perl-html-quoted
Version:        0.05
Release:        1%{?dist}
Summary:        Extract quotation structure from HTML email
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/BPS/HTML-Quoted-0.05
Source0:        HTML-Quoted-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.8.0
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.59
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTML::Parser) >= 3.0
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(HTML::Parser) >= 3.0

%description
HTML::Quoted extracts nested quotation structure from HTML email and
can recombine the parsed hunks. It preserves the original HTML and is
not an HTML sanitizer.

%prep
%autosetup -n HTML-Quoted-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat > VENDORED-INSTALLER-NOTICE <<'NOTICE'
HTML::Quoted is attributed to Ruslan Zakirov <ruz@bestpractical.com>.
The eight original bundled Module::Install files match Module-Install 1.06:
Copyright 2002 - 2011 Brian Ingerson, Audrey Tang and Adam Kennedy.
The original inc/Module/Install.pm additionally retains the notice
Copyright 2008 - 2012 Adam Kennedy.
Origin: https://metacpan.org/release/ADAMK/Module-Install-1.06

The original bundled Module::Install::ReadmeFromPod matches release 0.20:
Copyright (c) 2012 by Chris Williams.
Origin: https://metacpan.org/release/BINGOS/Module-Install-ReadmeFromPod-0.20

Both are available under the same terms as Perl itself: GPL version 1
or later, or the Perl Artistic License. See the accompanying full texts.
Original files and notices are retained in the source RPM.
NOTICE

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/HTML/Quoted.pm
test -f %{buildroot}%{_mandir}/man3/HTML::Quoted.3pm

%check
make test TEST_VERBOSE=1

%files
%license Artistic-1.0-Perl.txt GPL-1.0.txt VENDORED-INSTALLER-NOTICE
%doc README Changes
%{perl_vendorlib}/HTML/Quoted.pm
%{_mandir}/man3/HTML::Quoted.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package the fixed CPAN release and preserve all default tests.
