# SPDX-License-Identifier: Apache-2.0
Name:           libfind-lib-perl
Version:        1.04
Release:        1%{?dist}
Summary:        Locate Perl library paths relative to the running script
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Find-Lib
Source0:        Find-Lib-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(lib)
BuildRequires:  perl(vars)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(File::Spec)
Requires:       perl(Cwd)
Requires:       perl(lib)
Requires:       perl(vars)

%description
Find::Lib lets a Perl application locate its own private libraries using
paths relative to the running script.

%prep
%autosetup -n Find-Lib-%{version} -p1
test -f lib/Find/Lib.pm
test ! -e Lib/Find/Lib.pm
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Find/Lib.pm
test -f %{buildroot}%{_mandir}/man3/Find::Lib.3pm
test ! -e %{buildroot}%{_mandir}/man3/Find::Lib::Find::Lib.3pm

%check
# Legacy tests require the bundled t/testutils.pl through @INC. Add only the
# verified source root for this command, not a global current-directory path.
PERL5LIB="$(pwd -P)" make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Find/Lib.pm
%{_mandir}/man3/Find::Lib.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package the official release with unchanged tests and one canonical manpage.
