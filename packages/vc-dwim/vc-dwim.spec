# SPDX-License-Identifier: Apache-2.0
Name:           vc-dwim
Version:        1.10
Release:        1%{?dist}
Summary:        GNU utilities for version control and maintaining changelog files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/vc-dwim/
Source0:        vc-dwim-1.10.tar.xz
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  make
BuildRequires:  man-db
BuildRequires:  ctags


%description
GNU utilities for version control and maintaining changelog files

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
export GIT_AUTHOR_NAME='openEuler RISC-V CI'
export GIT_AUTHOR_EMAIL='noreply@example.invalid'
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
export GIT_ALLOW_PROTOCOL=file
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10-1
- Initial openEuler RISC-V package from the full package inventory.
