# SPDX-License-Identifier: Apache-2.0
Name:           python-easydict
Version:        1.13
Release:        1%{?dist}
Summary:        Access dictionary values as attributes recursively
License:        LGPL-3.0-only
URL:            https://github.com/makinacorpus/easydict
Source0:        easydict-1.13-fixed.tar.gz
Source1:        GPL-3.0.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-ruff

%description
Access dictionary values as attributes recursively.

%package -n python3-easydict
Summary:        %{summary}
Requires:       python3
Provides:       python-easydict = %{version}-%{release}

%description -n python3-easydict
Access dictionary values as attributes recursively.

%prep
%autosetup -n easydict-6df258e9bbeb2414bcb747b1691a6fbf5dfb7769 -p1
cp -p %{SOURCE1} GPL-3.0.txt

%build
%py3_build

%install
%py3_install

%check
# Preserve upstream's unconfigured Ruff defaults, not ancestor repo settings.
# A unique writable cache prevents inheriting /workspace's read-only cache.
# The cache belongs to this isolated target check and is not reused.
ruff_cache_dir=$(mktemp -d /tmp/easydict-ruff.XXXXXX)
ruff check --isolated --cache-dir "$ruff_cache_dir"
%{__python3} easydict/__init__.py -v
# The original script ignores testmod's failure count; the unchanged full
# doctest CLI supplies an explicit nonzero failure gate without dropping cases.
%{__python3} -m doctest -v easydict/__init__.py

%files -n python3-easydict
%license LICENSE GPL-3.0.txt
%doc README.rst CHANGES
%{python3_sitelib}/easydict/
%{python3_sitelib}/easydict-*.egg-info/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13-1
- Initial package retaining original Ruff and all module doctests.
