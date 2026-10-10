# SPDX-License-Identifier: Apache-2.0
# Pinned target Python 3.11 uses upstream's optional-C fallback, with no ELF
# payload; an automatic debuginfo subpackage would have an empty files list.
%global debug_package %{nil}
Name:           python-frozendict
Version:        2.4.7
Release:        1%{?dist}
Summary:        Immutable hashable Python dictionary with functional updates
License:        LGPL-3.0-only AND Python-2.0
URL:            https://github.com/Marco-Sulla/python-frozendict
Source0:        frozendict-2.4.7.tar.gz
Source1:        GPL-3.0.txt
Source2:        CPython-3.10.2-LICENSE
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-coverage
BuildRequires:  python3-mypy
BuildRequires:  python3-typing-extensions

%description
Frozendict is an immutable hashable dictionary with functional update methods.
The original backend attempts its optional C extension by default and provides
its documented pure Python fallback. Neither choice is forced by this recipe.

%package -n python3-frozendict
Summary:        Immutable hashable Python dictionary with functional updates
Provides:       python-frozendict = %{version}-%{release}

%description -n python3-frozendict
Python 3 immutable dictionaries, deep freezing and type information.

%prep
%autosetup -p1 -n python-frozendict-d4ee7590e2b507fd68124cd8a593778ce3c1158b
# Supplement complete notices without deleting or changing upstream files.
cp %{SOURCE1} GPL-3.0.txt
cp %{SOURCE2} CPython-3.10.2-LICENSE

%build
# No CIBUILDWHEEL or FROZENDICT_PURE_PY override: keep upstream optional-C policy.
%{__python3} setup.py bdist_wheel

%install
set -- dist/*.whl
test "$#" -eq 1
test -f "$1"
%{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} "$1"

%check
# Preserve complete target-3.11 upstream sdist defaults, including 100% branch
# coverage and the original checker. C-wheel debug.py is gated out of 3.11 by
# upstream CIBW_SKIP=cp31[!0]{t,}-*; do not count that gate as a passed C test.
export PYTHONPATH=%{buildroot}%{python3_sitearch}
export MYPYPATH="$PYTHONPATH"
export COVERAGE_FILE="$PWD/.coverage-rpm-check"
%{__python3} -m pytest --cov=frozendict --cov-report=term-missing --cov-branch --cov-fail-under=100
%{__python3} test/run_type_checker.py

%files -n python3-frozendict
%license LICENSE.txt GPL-3.0.txt CPython-3.10.2-LICENSE
%doc README.md
%{python3_sitearch}/frozendict/
%{python3_sitearch}/frozendict-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.7-1
- Onboard official immutable source without changing default backend or tests.
- Restore full LGPL companion and conservative copied-CPython notices.
