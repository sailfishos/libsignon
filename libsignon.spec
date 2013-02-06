%define _name signon
Name: libsignon
Version: 8.46
Release: 2
Summary: Single Sign On framework
Group: System/Libraries
License: LGPLv2.1
URL: https://code.google.com/p/accounts-sso.signond/
Source: %{_name}-%{version}.tar.bz2
BuildRequires: doxygen
BuildRequires: pkgconfig(QtCore)
BuildRequires: libcreds2-devel
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libcryptsetup)
BuildRequires: pkgconfig(accounts-qt)
BuildRequires: pkgconfig(libproxy-1.0)
BuildRequires: fdupes

Provides: libsignon-passwordplugin = %{version}-%{release}
Obsoletes: libsignon-passwordplugin < %{version}-%{release}

Patch0: 0001-libsignon-disable-multilib.patch

%description
%{summary}.

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/dbus-1/services/*
%config %{_sysconfdir}/signond.conf
%{_libdir}/signon/libpasswordplugin.so

%package testplugin
Summary: Single Sign On test plugins
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description testplugin
%{summary}

%files testplugin
%defattr(-,root,root,-)
%{_libdir}/%{_name}/libssotest*.so


%package exampleplugin
Summary: Single Sign On example client
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description exampleplugin
%{summary}

%files exampleplugin
%defattr(-,root,root,-)
%{_libdir}/%{_name}/libexampleplugin.so


%package devel
Summary: Development files for signon
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/libsignon-plugins.a
%exclude %{_libdir}/libsignon-qt.a
%{_libdir}/pkgconfig/*
%{_datadir}/qt4/mkspecs/*
%{_datadir}/dbus-1/interfaces/*


%package doc
Summary: Documentation for signon
Group: Documentation

%description doc
Doxygen-generated HTML documentation for the signon.

%files doc
%defattr(-,root,root,-)
%{_docdir}/signon/*
%{_docdir}/signon-plugins-dev/*
%{_docdir}/signon-plugins/*


%package qt-doc
Summary: Documentation for signon-qt
Group: Documentation

%description qt-doc
Doxygen-generated HTML documentation for the signon-qt

%files qt-doc
%defattr(-,root,root,-)
%{_docdir}/libsignon-qt/*


%prep
%setup -n %{_name}-%{version}
%patch0 -p1

%build
qmake %{_name}.pro
make


%install
make INSTALL_ROOT=%{buildroot} install
rm -f %{buildroot}/%{_docdir}/libsignon-qt/html/installdox
rm -f %{buildroot}/%{_docdir}/signon/html/installdox
rm -f %{buildroot}/%{_docdir}/signon-plugins/html/installdox
rm -f %{buildroot}/%{_docdir}/saslplugin/html/installdox
%fdupes %{buildroot}/%{_docdir}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
