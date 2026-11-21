# SPDX-License-Identifier: Apache-2.0
Name:           libdate-jd-perl
Version:        0.006
Release:        1%{?dist}
Summary:        Convert Julian and related day counts in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Date-JD
Source0:        Date-JD-0.006.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Math::BigRat) >= 0.13
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Pod::Find)
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(POSIX)
Requires:       perl
Requires:       perl(Math::BigRat) >= 0.13
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(POSIX)

%description
Convert Julian and related day counts in Perl

%prep
%autosetup -n Date-JD-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --create_packlist=0 --destdir=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Date/JD.pm
test -f %{buildroot}%{_mandir}/man3/Date::JD.3pm

%check
%{__perl} Build test --verbose 1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Date/JD.pm
%{_mandir}/man3/Date::JD.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package verified source with original numeric and POD coverage.
