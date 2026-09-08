# SPDX-License-Identifier: Apache-2.0
Name:           datamash
Version:        1.9
Release:        1%{?dist}
Summary:        Command-line calculations on tabular data
License:        GPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://www.gnu.org/software/datamash/
Source0:        datamash-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  bash-completion
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  glibc-all-langpacks
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Digest-MD5
BuildRequires:  perl-Digest-SHA
BuildRequires:  perl-MIME-Base64
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  pkgconf
BuildRequires:  sed
BuildRequires:  texinfo
BuildRequires:  valgrind

%description
GNU datamash performs numeric, textual, and statistical operations on
line-oriented tabular data. It also provides the decorate sorting helper.

%prep
%autosetup -p1

%build
%configure --with-bash-completion-dir=global
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check-expensive

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/datamash
%{_bindir}/decorate
%{_datadir}/bash-completion/completions/datamash
%{_datadir}/datamash/
%{_infodir}/datamash.info*
%{_mandir}/man1/datamash.1*
%{_mandir}/man1/decorate.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
