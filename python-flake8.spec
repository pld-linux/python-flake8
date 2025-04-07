#
# Conditional build:
%bcond_with	tests	# pytest tests
%bcond_without	doc	# Sphinx documentation

Summary:	The modular source code checker: pycodestyle, pyflakes and co.
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pycodestyle, pyflakes itp.
Name:		python-flake8
# Keep version < 4.x here as it is last version with python2 support
Version:	3.9.2
Release:	6
License:	MIT
Group:		Development/Tools
#Source0Download: https://pypi.org/simple/flake8/
Source0:	https://files.pythonhosted.org/packages/source/f/flake8/flake8-%{version}.tar.gz
# Source0-md5:	5c102972d3d0f35255c56a20613fcec5
Patch0:		flake8-duplicate.patch
URL:		https://gitlab.com/pycqa/flake8
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:30
%if %{with tests}
BuildRequires:	python-configparser
BuildRequires:	python-enum34
BuildRequires:	python-functools32
BuildRequires:	python-importlib_metadata
%endif
BuildRequires:	python-mccabe >= 0.6.0
BuildRequires:	python-mccabe < 0.7.0
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-pycodestyle >= 2.7.0
BuildRequires:	python-pycodestyle < 2.8.0
BuildRequires:	python-pyflakes >= 2.3.0
BuildRequires:	python-pyflakes < 2.4.0
BuildRequires:	python-pytest
BuildRequires:	python-typing
%if %{with doc}
BuildRequires:	python-sphinx-prompt
BuildRequires:	sphinx-pdg-2 >= 1.3
%endif
Requires:   python-mccabe >= 0.6.0
Requires:   python-mccabe < 0.7.0
Requires:   python-modules >= 1:2.7
Requires:   python-pycodestyle >= 2.7.0
Requires:   python-pycodestyle < 2.8.0
Requires:   python-pyflakes >= 2.3.0
Requires:   python-pyflakes < 2.4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pycodestyle
- Ned Batchelder's McCabe script

%description -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pycodestyle
- skrypt McCabe autorstwa Neda Batcheldera

%package apidocs
Summary:	API documentation for Python flake8 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona flake8
Group:		Documentation

%description apidocs
API documentation for Python flake8 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona flake8.

%prep
%setup -q -n flake8-%{version}
%patch -P 0 -p1

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest -rw tests
%endif

%if %{with doc}
cd docs/source
PYTHONPATH=$(pwd)/../../src \
sphinx-build-2 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/flake8{,-2}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst
%attr(755,root,root) %{_bindir}/flake8-2
%{py_sitescriptdir}/flake8
%{py_sitescriptdir}/flake8-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/source/_build/html/{_modules,_static,internal,plugin-development,release-notes,user,*.html,*.js}
%endif
