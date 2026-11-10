# SPDX-License-Identifier: Apache-2.0
Name:           perl-time-human
Version:        1.03
Release:        1%{?dist}
Summary:        Render local time as approximate spoken English in Perl
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Time-Human
Source0:        Time-Human-1.03.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Render local time as approximate spoken English in Perl

%prep
%autosetup -n Time-Human-%{version}
sed -n '/^=head1 COPYRIGHT$/,/^=head1 SEE ALSO$/p' Human.pm | sed '1d;$d' > COPYRIGHT
test -s COPYRIGHT
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license COPYRIGHT Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Time/Human.pm
%{_mandir}/man3/Time::Human.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the fixed upstream release with its original default tests.
