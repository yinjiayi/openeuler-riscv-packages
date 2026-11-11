# SPDX-License-Identifier: Apache-2.0
Name:           perl-convert-ascii85
Version:        0.01
Release:        1%{?dist}
Summary:        Encode and decode Ascii85 data in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MAUKE/Convert-Ascii85-0.01
Source0:        Convert-Ascii85-0.01.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.22
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Pod::Coverage) >= 0.18
BuildRequires:  perl(Pod::Find)
BuildRequires:  perl(Devel::Symdump)
Requires:       perl(Exporter) >= 5.57

%description
Convert::Ascii85 converts bytes to Ascii85 text and back, with optional
compression of runs of four zero or space bytes.

%prep
%autosetup -n Convert-Ascii85-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Convert/Ascii85.pm
test -f %{buildroot}%{_mandir}/man3/Convert::Ascii85.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Convert/Ascii85.pm
%{_mandir}/man3/Convert::Ascii85.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the pinned release and retain all original default tests, including POD.
