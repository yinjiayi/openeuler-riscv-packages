# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-ipc-run-safehandles
Version:        0.04
Release:        1%{?dist}
Summary:        Safe standard handles for Perl IPC::Run and IPC::Run3
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IPC-Run-SafeHandles
Source0:        IPC-Run-SafeHandles-0.04.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-List-MoreUtils
BuildRequires:  perl-IPC-Run
BuildRequires:  perl-IPC-Run3
BuildRequires:  perl-Carp
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-List-MoreUtils
Requires:       perl-IPC-Run
Requires:       perl-IPC-Run3
Requires:       perl-Carp

%description
IPC::Run::SafeHandles temporarily provides safe standard handles around IPC::Run
and IPC::Run3 calls in FastCGI or PerlIO-layer environments. It can also restore
the original subprocess functions when its wrappers are no longer needed.

%prep
%setup -q -n IPC-Run-SafeHandles-%{version}
%patch -P 0 -p1

%build
# All dependencies are supplied by RPM; do not let the bundled helper fetch them.
PERL_AUTOINSTALL=--skipdeps %{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README BUNDLED-HELPER-NOTICES
%doc Changes
%{perl_vendorlib}/IPC/Run/SafeHandles.pm
%{_mandir}/man3/IPC::Run::SafeHandles.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Retain original bundled helper notices and all four default test files.
