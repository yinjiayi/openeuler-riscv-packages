# SPDX-License-Identifier: Apache-2.0
Name:           catimg
Version:        2.8.0
Release:        1%{?dist}
Summary:        Render images in a terminal
License:        MIT
URL:            https://github.com/posva/catimg
Source0:        catimg-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
catimg is a small command-line program that renders JPEG, PNG, ICO, and GIF
images directly in a terminal using ANSI color escape sequences.

%prep
%autosetup -p1

%build
%cmake \
  -DMAN_OUTPUT_PATH=%{_mandir}/man1
%make_build

%install
DESTDIR=%{buildroot} %{__cmake} --install .
install -Dpm0644 completion/_catimg \
  %{buildroot}%{_datadir}/zsh/site-functions/_catimg

%check
./bin/catimg -h | grep -F 'Usage: catimg'
./bin/catimg -r 1 -w 4 test-images/mewtwo-front.png > rendered.txt
test -s rendered.txt
grep -F $'\033[' rendered.txt

%files
%license LICENSE
%doc README.md
%{_bindir}/catimg
%{_mandir}/man1/catimg.1*
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_catimg

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.0-1
- Initial openEuler RISC-V package.
