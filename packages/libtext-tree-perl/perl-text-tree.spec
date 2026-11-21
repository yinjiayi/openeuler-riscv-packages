# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-tree
Version:        1.0
Release:        1%{?dist}
Summary:        Render Perl tree data as ASCII diagrams
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Tree
Source0:        Text-Tree-1.0.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(vars)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(vars)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Text::Tree formats a hierarchy of strings into a plain or boxed
ASCII tree diagram.

%prep
%autosetup -n Text-Tree-%{version} -p1
# Preserve the complete original three-author copyright and grant.
%{__perl} -0777 -ne 'print $1 if /(^=head1 COPYRIGHT AND LICENSE\n.*\z)/ms' \
    lib/Text/Tree.pm > LICENSE
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
%doc README CHANGELOG
%{perl_vendorlib}/Text/Tree.pm
%{_mandir}/man3/Text::Tree.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Package Text::Tree with original tests and the verbatim source grant.
