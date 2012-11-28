%define _name signon
Name: libsignon
Version: 8.43
Release: 1
Summary: Single Sign On framework
Group: System/Libraries
License: LGPLv2.1
URL: http://gitorious.org/accounts-sso/signon
Source0: http://accounts-sso.googlecode.com/files/%{_name}-%{version}.tar.bz2
BuildRequires: doxygen
#BuildRequires: graphviz
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libcryptsetup)
BuildRequires: pkgconfig(accounts-qt)
BuildRequires: fdupes
# TODO: - check if it makes sense to have signoncrypto-functionality (encrypted
#         dbus messages); if so, we'd need to reintroduce the functionality in
#         signon, as it has been removed recently
#BuildRequires: pkgconfig(libsignoncrypto-qt)
#BuildRequires: pkgconfig(libcrypto)
#       - add support for pacrunner (NEMO#524)
#       - check if we have usable testcases
Patch0: 0001-include-QDebug-to-remotepluginprocess.patch

%description
%{summary}.

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/dbus-1/services/*
# is in exampleplugin
%exclude %{_bindir}/signonclient
%config %{_sysconfdir}/signond.conf
%{_libdir}/signon/extensions/libcryptsetup.so


%package testplugin
Summary: Single Sign On test plugins
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description testplugin
%{summary}

%files testplugin
%defattr(-,root,root,-)
%{_libdir}/%{_name}/libssotest*.so


%package passwordplugin
Summary: Plain Password plugin for Single Sign On
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description passwordplugin
%{summary}

%files passwordplugin
%defattr(-,root,root,-)
%{_libdir}/%{_name}/libpasswordplugin.so


%package exampleplugin
Summary: Single Sign On example client
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description exampleplugin
%{summary}

%files exampleplugin
%defattr(-,root,root,-)
%{_libdir}/%{_name}/libexampleplugin.so
%{_bindir}/signonclient


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
%{_docdir}/libsignon-qt-dev/*


%prep
%setup -q -n %{_name}-%{version}
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
