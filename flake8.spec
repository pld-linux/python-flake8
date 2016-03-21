#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# do not perform "make test"

Summary:	The modular source code checker: pep8, pyflakes and co
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pep8, pyflakes itp.
Name:		flake8
Version:	2.5.4
Release:	1
License:	MIT
Group:		Development/Tools
#Source0Download: https://pypi.python.org/simple/flake8/
Source0:	https://pypi.python.org/packages/source/f/flake8/%{name}-%{version}.tar.gz
# Source0-md5:	a4585b3569b95c3f66acb8294a7f06ef
URL:		https://pypi.python.org/pypi/flake8
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mccabe >= 0.2.1
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-pep8 >= 1.5.7
BuildRequires:	python-pyflakes >= 0.8.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mccabe >= 0.2.1
BuildRequires:	python3-nose
BuildRequires:	python3-pep8 >= 1.5.7
BuildRequires:	python3-pyflakes >= 0.8.1
%endif
%endif
%if %{with python3}
Requires:	python3-flake8 = %{version}-%{release}
%else
Requires:	python-flake8 = %{version}-%{release}
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pep8
- Ned Batchelder's McCabe script

%description -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pep8
- skrypt McCabe autorstwa Neda Batcheldera

%package -n python-flake8
Summary:	The modular source code checker: pep8, pyflakes and co
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pep8, pyflakes itp.
Group:		Libraries/Python
Requires:	python-modules

%description -n python-flake8
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pep8
- Ned Batchelder's McCabe script

%description -n python-flake8 -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pep8
- skrypt McCabe autorstwa Neda Batcheldera

%package -n python3-flake8
Summary:	The modular source code checker: pep8, pyflakes and co
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pep8, pyflakes itp.
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-flake8
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pep8
- Ned Batchelder's McCabe script

%description -n python3-flake8 -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pep8
- skrypt McCabe autorstwa Neda Batcheldera

%prep
%setup -q

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
mv $RPM_BUILD_ROOT%{_bindir}/flake8{,-2}
%py_postclean
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/flake8{,-3}
%endif

ln -s flake-%{!?with_python3:2}%{?with_python3:3} $RPM_BUILD_ROOT%{_bindir}/flake8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE README.rst
%attr(755,root,root) %{_bindir}/flake8

%if %{with python2}
%files -n python-flake8
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flake8-2
%{py_sitescriptdir}/flake8
%{py_sitescriptdir}/flake8-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-flake8
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flake8-3
%{py3_sitescriptdir}/flake8
%{py3_sitescriptdir}/flake8-%{version}-py*.egg-info
%endif
