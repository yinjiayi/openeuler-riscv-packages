# SPDX-License-Identifier: Apache-2.0
Name:           perl-return-multilevel
Version:        0.08
Release:        1%{?dist}
Summary:        Return from nested Perl calls
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Return-MultiLevel
Source0:        Return-MultiLevel-0.08.tar.gz
Source1:        Dist-Zilla-6.024.tar.gz
Source2:        Dist-Zilla-PluginBundle-Author-Plicease-2.69.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Config)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Return::MultiLevel supplies a callback that returns values across
multiple levels of Perl calls.

%prep
%autosetup -n Return-MultiLevel-%{version} -p1
# Keep the complete notices for the already generated files.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.024/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-PluginBundle-Author-Plicease-2.69/LICENSE > LICENSE.Plicease
test -s LICENSE.Dist-Zilla && test -s LICENSE.Plicease

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE LICENSE.Dist-Zilla LICENSE.Plicease
%doc README Changes
%{perl_vendorlib}/Return/MultiLevel.pm
%{_mandir}/man3/Return::MultiLevel.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package Return::MultiLevel with its original tests and full notices.
