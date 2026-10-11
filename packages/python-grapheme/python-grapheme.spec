# SPDX-License-Identifier: Apache-2.0
Name:           python-grapheme
Version:        0.6.0
Release:        1%{?dist}
Summary:        Unicode grapheme cluster helpers for Python
License:        MIT AND Unicode-DFS-2016
URL:            https://github.com/alvinlindstam/grapheme
Source0:        grapheme-%{version}.tar.gz
Source1:        grapheme-0.6.0-original-suite.tar.gz
Source2:        LICENSE-Unicode-data.txt

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-coverage

%description
Unicode grapheme cluster boundaries and string helpers using Unicode13 data.
Official final PyPI release supplemented with the unchanged original test suite.

%package -n python3-grapheme
Summary:        Unicode grapheme cluster helpers for Python 3
Provides:       python-grapheme = %{version}-%{release}
Requires:       python3
Requires:       python3-pytest
Requires:       python3-coverage

%description -n python3-grapheme
Unicode grapheme cluster helpers with RPM-owned original conformance tests.
Pytest and coverage are retained to repeat the complete installed-package suite.

%prep
%autosetup -p1 -n grapheme-%{version}
mkdir ../grapheme-original-suite
tar -xzf %{SOURCE1} --strip-components=1 -C ../grapheme-original-suite
for file in setup.py README.rst grapheme/__init__.py grapheme/api.py grapheme/finder.py grapheme/grapheme_property_group.py grapheme/data/grapheme_break_property.json; do
    cmp "$file" "../grapheme-original-suite/$file"
done
cp -p ../grapheme-original-suite/LICENSE LICENSE
cp -a ../grapheme-original-suite/tests ../grapheme-original-suite/unicode-data .
cp -p %{SOURCE2} LICENSE-Unicode-data.txt

%build
%py3_build

%install
%py3_install
mkdir -p %{buildroot}%{_datadir}/python-grapheme/tests
cp -a tests unicode-data %{buildroot}%{_datadir}/python-grapheme/tests/
install -m 0644 ../grapheme-original-suite/.travis.yml %{buildroot}%{_datadir}/python-grapheme/tests/upstream-travis.yml

%check
# Whole default Travis suite twice; target py.test and pytest module share console_main.
%{__python3} -m pytest
%{__python3} -m coverage run --source=grapheme -m pytest

%files -n python3-grapheme
%license LICENSE LICENSE-Unicode-data.txt
%doc README.rst
%{python3_sitelib}/grapheme/
%{python3_sitelib}/grapheme-%{version}-py*.egg-info
%{_datadir}/python-grapheme/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Onboard official release with complete original pytest and Unicode13 data suite.
- Preserve full MIT and Unicode data notices; no library or test patch.
