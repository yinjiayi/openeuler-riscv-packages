# SPDX-License-Identifier: Apache-2.0
Name:           perl-convert-nls-date-format
Version:        0.06
Release:        1%{?dist}
Summary:        Convert Oracle and POSIX date format strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Convert-NLS_DATE_FORMAT
Source0:        Convert-NLS_DATE_FORMAT-0.06.tar.gz
Source1:        Minilla-v3.0.1-LICENSE.txt
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl >= 5.8.1
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Build::Tiny) >= 0.035
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Exporter)

%description
Convert Oracle NLS_DATE_FORMAT strings to POSIX strftime format strings and
back. The module converts format strings, not dates or times.

%prep
%autosetup -n Convert-NLS_DATE_FORMAT-%{version} -p1
cp -p %{SOURCE1} .
cat <<'DONOR_NOTICE' > SOURCE-DONOR-NOTICE
Build.PL was generated from the ModuleBuildTiny template of Minilla v3.0.1
(copyright 2013 tokuhirom). Its full Perl dual-license terms and notice
are in Minilla-v3.0.1-LICENSE.txt.
Reference: https://github.com/tokuhirom/Minilla/blob/f85f27fadaee5f7af9a3007c8894a10bef6a232b/lib/Minilla/ModuleMaker/ModuleBuildTiny.pm

The format tokenizers in Convert/NLS_DATE_FORMAT.pm attribute expressions
to DateTime and Date::Format:
- DateTime 0.28, copyright 2003-2005 David Rolsky.
  https://metacpan.org/release/DROLSKY/DateTime-0.28/source/lib/DateTime.pm
- Date::Format in TimeDate 1.16, copyright 1995-1999 Graham Barr.
  https://metacpan.org/release/GBARR/TimeDate-1.16/source/lib/Date/Format.pm
Both donors allow redistribution under the same terms as Perl itself;
the full GPL version 1 or later / Artistic License terms are in LICENSE.
DONOR_NOTICE

%build
%{__perl} ./Build.PL --installdirs vendor
%{__perl} ./Build build

%install
%{__perl} ./Build install --destdir "%{buildroot}"
find "%{buildroot}" -type f -path '*/auto/Convert/NLS_DATE_FORMAT/.packlist' -delete

%check
%{__perl} ./Build test --verbose

%files
%license LICENSE Minilla-v3.0.1-LICENSE.txt SOURCE-DONOR-NOTICE
%doc README.md Changes
%{perl_vendorlib}/Convert/NLS_DATE_FORMAT.pm
%{_mandir}/man3/Convert::NLS_DATE_FORMAT.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package the pinned CPAN release with original tests and donor notices.
