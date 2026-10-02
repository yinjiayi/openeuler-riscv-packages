# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-MediawikiFormat
Version:        1.04
Release:        1%{?dist}
Summary:        Render MediaWiki-style markup with Perl
License:        GPL-2.0-only OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-MediawikiFormat
Source0:        Text-MediawikiFormat-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(CGI)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(HTML::Tagset)
BuildRequires:  perl(Scalar::Util) >= 1.14
BuildRequires:  perl(Test::More) >= 0.3
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(version) >= 0.74
Requires:       perl(CGI)
Requires:       perl(HTML::Parser)
Requires:       perl(HTML::Tagset)
Requires:       perl(Scalar::Util) >= 1.14
Requires:       perl(URI)
Requires:       perl(URI::Escape)

%description
Text::MediawikiFormat converts MediaWiki-style text to HTML and exposes
block-formatting classes for callers that need to customize the output.

%prep
%autosetup -n Text-MediawikiFormat-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 14 original upstream default t/*.t files and their TODO cases.
%make_build test

%files
%license ARTISTIC GPL
%doc README Changes
%{perl_vendorlib}/Text/MediawikiFormat.pm
%{perl_vendorlib}/Text/MediawikiFormat/Block.pm
%{perl_vendorlib}/Text/MediawikiFormat/Blocks.pm
%{_mandir}/man3/Text::MediawikiFormat.3*
%{_mandir}/man3/Text::MediawikiFormat::Block.3*
%{_mandir}/man3/Text::MediawikiFormat::Blocks.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package official CPAN source and retain all default upstream tests.
