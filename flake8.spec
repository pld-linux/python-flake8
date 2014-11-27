Summary:	The modular source code checker: pep8, pyflakes and co
Name:		flake8
Version:	2.2.5
Release:	1
License:	MIT
Group:		Development/Tools
Source0:	https://pypi.python.org/packages/source/f/flake8/%{name}-%{version}.tar.gz
# Source0-md5:	6dea927949b94c9d9495ab24bcdf9cf0
URL:		https://pypi.python.org/pypi/flake8
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
Requires:	python3-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pep8
- Ned Batchelder's McCabe script

%prep
%setup -q

%build
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} setup.py \
		build --build-base build-3 \
		install --skip-build \
		--optimize=2 \
		--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt README.rst
%attr(755,root,root) %{_bindir}/flake8
%{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}-%{version}-py*.egg-info
