# SPDX-License-Identifier: Apache-2.0
Name:           python-dicttoxml
Version:        1.7.16
Release:        1%{?dist}
Summary:        Convert native Python data into XML
License:        GPL-2.0-only
URL:            https://github.com/quandyfactory/dicttoxml
Source0:        dicttoxml-1.7.16.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 61
BuildRequires:  python3-wheel

%description
Dicttoxml converts native Python dictionaries, lists, strings, numbers and
date/time values into XML, with optional roots, type attributes and CDATA.

%package -n python3-dicttoxml
Summary:        Convert native Python data into XML
Provides:       python-dicttoxml = %{version}-%{release}

%description -n python3-dicttoxml
Dicttoxml's pure Python XML conversion module installed for Python 3.

%prep
%autosetup -p1 -n dicttoxml-%{version}

%build
# Preserve upstream setup.py, the documented source installation interface.
%py3_build

%install
%py3_install

%check
# The fixed upstream tag and sdist have no suite or default test command.
# Additive offline README API checks are not an upstream full-suite claim.
%{__python3} - <<'PY'
import datetime
import decimal
import xml.etree.ElementTree as ET
import dicttoxml

assert dicttoxml.__version__ == '1.7.16'
obj = {'mylist': ['foo', 'bar', 'baz'], 'mydict': {'foo': 'bar', 'baz': 1}, 'ok': True}
encoded = dicttoxml.dicttoxml(obj)
assert isinstance(encoded, bytes)
root = ET.fromstring(encoded)
assert root.tag == 'root'
assert [x.text for x in root.findall('mylist/item')] == ['foo', 'bar', 'baz']
assert root.find('mydict/baz').text == '1'
assert root.find('ok').text == 'true'
assert root.find('ok').get('type') == 'bool'
assert ET.fromstring(dicttoxml.dicttoxml(obj, custom_root='example')).tag == 'example'
assert 'type=' not in dicttoxml.dicttoxml(obj, attr_type=False).decode()
snippet = dicttoxml.dicttoxml(obj, root=False)
assert not snippet.startswith(b'<?xml')
assert ET.fromstring(b'<wrapper>' + snippet + b'</wrapper>').find('ok').text == 'true'
assert not dicttoxml.dicttoxml(obj, xml_declaration=False).startswith(b'<?xml')
assert isinstance(dicttoxml.dicttoxml(obj, return_bytes=False), str)
root = ET.fromstring(dicttoxml.dicttoxml({'bad key': '<&>', '^bad': None, 'n': decimal.Decimal('1.25'), 'date': datetime.date(2020, 1, 2)}))
assert root.find('bad_key').text == '<&>'
assert root.find('key').get('name') == '^bad'
assert root.find('key').get('type') == 'null'
assert root.find('n').text == '1.25'
assert root.find('date').text == '2020-01-02'
root = ET.fromstring(dicttoxml.dicttoxml({'values': ['<&>', ']]>']}, cdata=True, item_func=lambda _: 'value'))
assert [x.text for x in root.findall('values/value')] == ['<&>', ']]>']
root = ET.fromstring(dicttoxml.dicttoxml({'values': [1, 2, 3]}, ids=True))
ids = [x.get('id') for x in root.iter() if x.get('id')]
assert len(ids) == 4 and len(set(ids)) == len(ids)
try:
    dicttoxml.dicttoxml(object())
except TypeError:
    pass
else:
    raise AssertionError('unsupported types must raise TypeError')
PY

%files -n python3-dicttoxml
%license LICENCE.txt
%doc README.md
%{python3_sitelib}/dicttoxml.py
%{python3_sitelib}/__pycache__/dicttoxml.*
%{python3_sitelib}/dicttoxml-%{version}-py*.egg-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.16-1
- Onboard the official source release without bundled historical binaries.
- Preserve original sources and add offline README API regression checks.
