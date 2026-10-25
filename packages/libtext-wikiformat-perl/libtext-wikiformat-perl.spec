# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-WikiFormat
Version:        0.81
Release:        1%{?dist}
Summary:        Translate simple Wiki markup to formatted text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-WikiFormat
Source0:        Text-WikiFormat-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-URI
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-generators
Requires:       perl(URI::Escape) >= 0.01
Requires:       perl(Scalar::Util) >= 1.14

%description
Text::WikiFormat translates simple Wiki markup to HTML or other formats
specified by caller-provided tags. The distribution also provides reusable
block-formatting classes.

%prep
%autosetup -n Text-WikiFormat-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir=%{buildroot}
find %{buildroot} -type f -name .packlist -delete

%check
# Keep all 14 upstream default t/*.t files. Locally, 142 TAP checks passed;
# one known embedded-link case failed under upstream's explicit TODO marker.
# The two t/developer POD files are not in the default upstream test action.
./Build test

%files
%license ARTISTIC GPL
%doc README Changes
%{perl_vendorlib}/Text/WikiFormat.pm
%{perl_vendorlib}/Text/WikiFormat/Blocks.pm
%{_mandir}/man3/Text::WikiFormat.3*
%{_mandir}/man3/Text::WikiFormat::Blocks.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.81-1
- Package official CPAN release with all default upstream tests retained.
