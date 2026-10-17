# SPDX-License-Identifier: Apache-2.0
Name:           python-text-unidecode
Version:        1.3
Release:        1%{?dist}
Summary:        Basic Unicode transliteration for Python
License:        Artistic-1.0-Perl
URL:            https://github.com/kmike/text-unidecode
Source0:        text-unidecode-1.3.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 40.8.0
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-pytest
BuildArch:      noarch

%description
Text-Unidecode is a basic Python port of Text::Unidecode. It transliterates
Unicode text using the unmodified data table shipped by the official release.
The complete original test suite and source/default configuration are retained.

%prep
%autosetup -n text-unidecode-a0005d7a0b43a6aa21ce8a63f1da48c6c44f03e1

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
python3 setup.py bdist_wheel

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/text_unidecode-%{version}-py2.py3-none-any.whl
# Preserve exactly all twelve original Git blobs, not generated build outputs.
install -d %{buildroot}%{_datadir}/%{name}/source/src/text_unidecode
install -m 0644 .gitignore .travis.yml LICENSE MANIFEST.in README.rst _dump.pl setup.cfg setup.py test_unidecode.py tox.ini %{buildroot}%{_datadir}/%{name}/source/
install -m 0644 src/text_unidecode/__init__.py src/text_unidecode/data.bin %{buildroot}%{_datadir}/%{name}/source/src/text_unidecode/

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME
# Original tox command is py.test []: [] means empty posargs in supplied tox
# 4.11.1. Execute the effective complete default against the built library.
# Only target Python 3.11 is tested, not upstream's historical interpreter matrix.
PYTHONPATH="$PWD/build/lib" py.test

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/text_unidecode/
%{python3_sitelib}/text_unidecode-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Pin the complete official release, retain original data and whole default tests.
