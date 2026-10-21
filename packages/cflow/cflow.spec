# SPDX-License-Identifier: Apache-2.0
Name:           cflow
Version:        1.8
Release:        1%{?dist}
Summary:        Analyze C source files and print call graphs
License:        GPL-3.0-or-later AND GFDL-1.2-or-later
URL:            https://www.gnu.org/software/cflow/
Source0:        cflow-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  emacs-filesystem
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  texinfo
Requires:       emacs-filesystem

%description
GNU cflow analyzes C source files and prints direct or reverse call graphs.
It supports GNU and POSIX output formats and optional preprocessing.

%prep
%autosetup -p1

%build
EMACS=no %configure
%make_build

%install
%make_install
install -Dpm 0644 elisp/cflow-mode.el \
  %{buildroot}%{_datadir}/emacs/site-lisp/cflow-mode.el
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/cflow
%{_datadir}/%{name}/
%{_datadir}/emacs/site-lisp/cflow-mode.el
%{_infodir}/cflow.info*
%{_mandir}/man1/cflow.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
