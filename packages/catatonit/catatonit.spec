# SPDX-License-Identifier: Apache-2.0
Name:           catatonit
Version:        0.2.1
Release:        1%{?dist}
Summary:        A minimal container init process
License:        GPL-2.0-or-later
URL:            https://github.com/openSUSE/catatonit
Source0:        catatonit.tar.xz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make


%description
A minimal container init process

%prep
%autosetup -p1 -n catatonit-%{version}

%build
./autogen.sh
%configure
%make_build

%install
%make_install
install -Dpm0644 COPYING %{buildroot}%{_datadir}/licenses/%{name}/COPYING

%check
./catatonit -V | grep -F 'tini version 0.2.1_catatonit'
./catatonit -h 2>&1 | grep -F 'usage: catatonit'

%files
%license %{_datadir}/licenses/%{name}/COPYING
%doc README.md CHANGELOG.md
%{_bindir}/catatonit

%changelog
* Sat Aug 22 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Package upstream catatonit with Autotools bootstrap and CLI checks.
