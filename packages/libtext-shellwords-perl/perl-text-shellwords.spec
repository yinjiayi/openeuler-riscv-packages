# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-shellwords
Version:        1.08
Release:        1%{?dist}
Summary:        Compatibility wrapper for parsing shell-style tokens in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Shellwords
Source0:        Text-Shellwords-1.08.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test)
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  sed
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(Text::ParseWords)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Text::Shellwords preserves the legacy namespace for callers that parse
shell-style tokens. It delegates parsing to Text::ParseWords and does not
execute the resulting tokens.

%prep
%autosetup -n Text-Shellwords-%{version}
sed -n '/^=head1 AUTHOR$/,/^=cut/p' Shellwords.pm > LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Shellwords.pm
%{_mandir}/man3/Text::Shellwords.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.08-1
- Package Text::Shellwords 1.08 with the original grant and unchanged tests.
