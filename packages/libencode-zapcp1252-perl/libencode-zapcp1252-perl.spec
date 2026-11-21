# SPDX-License-Identifier: Apache-2.0
Name:           libencode-zapcp1252-perl
Version:        0.40
Release:        1%{?dist}
Summary:        Convert Windows-1252 punctuation to UTF-8 or ASCII in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Encode-ZapCP1252
Source0:        Encode-ZapCP1252-0.40.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        Module-Build-Compat-0.4229.pm
BuildArch:      noarch
BuildRequires:  sed
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Test::More) >= 0.17
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(constant)
BuildRequires:  perl(utf8)
Requires:       perl
Requires:       perl(Encode)
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(vars)
Requires:       perl(constant)

%description
Convert Windows-1252 punctuation to UTF-8 or ASCII in Perl

%prep
%autosetup -n Encode-ZapCP1252-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
sed -n '/^=head1 COPYRIGHT$/,/^=head1 SEE ALSO$/p' %{SOURCE3} | sed '/^=head1 /d' > Module-Build-Compat-NOTICE.txt
test -s Module-Build-Compat-NOTICE.txt

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --create_packlist=0 --destdir=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Encode/ZapCP1252.pm
test -f %{buildroot}%{_mandir}/man3/Encode::ZapCP1252.3pm

%check
%{__perl} Build test --verbose 1

%files
%license README.md Artistic-1.0-Perl.txt GPL-1.0.txt Module-Build-Compat-NOTICE.txt
%doc Changes
%{perl_vendorlib}/Encode/ZapCP1252.pm
%{_mandir}/man3/Encode::ZapCP1252.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.40-1
- Package verified source and original tests with full Perl license notices.
