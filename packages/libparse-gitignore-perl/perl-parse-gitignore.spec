# SPDX-License-Identifier: Apache-2.0
Name:           perl-parse-gitignore
Version:        1.0
Release:        1%{?dist}
Summary:        Read Git ignore rules from Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Parse-Gitignore
Source0:        Parse-Gitignore-1.0.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Slurper) >= 0.010
BuildRequires:  perl(File::Spec) >= 3.40
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(FindBin)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(File::Slurper) >= 0.010
Requires:       perl(File::Spec) >= 3.40
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Parse::Gitignore reads ignore files and identifies paths matched by
their filename and directory patterns.

%prep
%autosetup -n Parse-Gitignore-%{version} -p1
# Copy the original copyright and license grant without changing its bytes.
%{__perl} -0777 -ne 'print $1 if /(^=head1 COPYRIGHT & LICENCE\n.*\z)/ms' \
    lib/Parse/Gitignore.pod > LICENSE
test -s LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Parse/Gitignore.pm
%{perl_vendorlib}/Parse/Gitignore.pod
%{_mandir}/man3/Parse::Gitignore.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Package Parse::Gitignore with the original tests and POD license.
