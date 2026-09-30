# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-WordDiff
Version:        0.09
Release:        1%{?dist}
Summary:        Generate word-oriented text diffs in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-WordDiff
Source0:        Text-WordDiff-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Algorithm::Diff) >= 1.19
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Algorithm::Diff) >= 1.19
Requires:       perl(HTML::Entities)
Requires:       perl(Term::ANSIColor)

%description
Text::WordDiff generates word-oriented diffs and includes HTML and ANSI
color formatters for rendering changes in narrative text.

%prep
%autosetup -n Text-WordDiff-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all five default upstream tests, including HTML, ANSI and POD.
./Build test

%files
%license LICENSE
%doc README.md Changes eg/word_diff.css
%{perl_vendorlib}/Text/WordDiff.pm
%{perl_vendorlib}/Text/WordDiff/*.pm
%{_mandir}/man3/Text::WordDiff*.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package official CPAN release with all default tests and installed smoke.
