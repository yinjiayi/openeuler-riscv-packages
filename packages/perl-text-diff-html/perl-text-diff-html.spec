# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-diff-html
Version:        0.08
Release:        1%{?dist}
Summary:        Generate HTML markup from Perl Text::Diff comparisons
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Diff-HTML
Source0:        Text-Diff-HTML-0.08.tar.gz
Patch0:         0001-retain-module-build-compat-notice.patch
BuildArch:      noarch
BuildRequires:  patch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.2701
BuildRequires:  perl(Test::More) >= 0.17
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Text::Diff) >= 0.11
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(HTML::Entities)
Requires:       perl(Text::Diff) >= 0.11

%description
Text::Diff::HTML adds a style to Text::Diff that renders differences as
HTML markup and escapes input text for display.

%prep
%autosetup -p1

%build
perl Build.PL --installdirs vendor
./Build

%install
./Build install --destdir "%{buildroot}"

%check
./Build test --verbose

%files
%license LICENSE MODULE-BUILD-COMPAT-NOTICE
%doc README.md Changes
%{perl_vendorlib}/Text/Diff/HTML.pm
%{_mandir}/man3/Text::Diff::HTML.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package Text::Diff::HTML 0.08 with the original behavior and POD tests.
