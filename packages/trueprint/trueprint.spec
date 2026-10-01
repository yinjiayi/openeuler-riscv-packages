# SPDX-License-Identifier: Apache-2.0
Name:           trueprint
Version:        5.4
Release:        1%{?dist}
Summary:        Convert source code and text files to PostScript
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/trueprint/
Source0:        trueprint-5.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Convert source code and text files to PostScript

%prep
%autosetup -p1
# GCC 14 diagnoses these two omitted declarations as errors.
sed -i '/#include "utils.h"/a #include "debug.h"' src/language.c
sed -i '/#include <stdlib.h>/a #include <string.h>' src/lang_pike.c

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-1
- Initial openEuler RISC-V package from the full package inventory.
