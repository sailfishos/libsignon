Name:    signon-qt5
Version: 8.61
Release: 1
Summary: Single Sign On framework
License: LGPLv2
URL:     https://github.com/sailfishos/libsignon
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}.privileges

Patch1:  0001-disable-multilib.patch
Patch2:  0002-fix-documentation-path.patch
Patch3:  0003-Install-tests-add-tests-definition.patch
Patch4:  0004-Set-permissions-on-config-dir-correctly.patch
Patch5:  0005-Guard-PendingCall-against-deletion-by-connected-slot.patch
Patch6:  0006-Always-use-P2P-DBus-if-enabled.-Contributes-to-JB-42.patch
Patch7:  0007-Use-p2p-dbus-for-signon-ui-flows.-Contributes-to-JB-.patch
Patch8:  0008-Initialize-secrets-db-on-start.-Fixes-JB-34557.patch
Patch9:  0009-Treat-empty-ACL-as-synonym-for-.-Contributes-to-JB-2.patch
Patch10: 0010-Use-P2P-DBus-server-for-tests-if-built-in-ENABLE_P2P.patch
Patch11: 0011-Increase-maximum-token-storage-size.patch

BuildRequires: doxygen
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libcryptsetup) >= 1.4.0
BuildRequires: pkgconfig(accounts-qt5)
BuildRequires: pkgconfig(libproxy-1.0)
BuildRequires: pkgconfig(qt5-boostable)
BuildRequires: fdupes
Requires: mapplauncherd-qt5

%description
%{summary}.

%package -n libsignon-qt5
Summary: Single Sign On Qt library
Requires: %{name} = %{version}-%{release}

%description -n libsignon-qt5
%{summary}.

%package testplugin
Summary: Single Sign On test plugins
Requires: %{name} = %{version}-%{release}

%description testplugin
%{summary}.

%package exampleplugin
Summary: Single Sign On example client
Requires: %{name} = %{version}-%{release}

%description exampleplugin
%{summary}.

%package devel
Summary: Development files for signon
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%package -n libsignon-qt5-devel
Summary: Development files for libsignon-qt
Requires: libsignon-qt5 = %{version}-%{release}

%description -n libsignon-qt5-devel
%{summary}.

%package doc
Summary: Documentation for signon

%description doc
Doxygen-generated HTML documentation for the signon.

%package -n libsignon-qt5-doc
Summary: Documentation for signon-qt

%description -n libsignon-qt5-doc
Doxygen-generated HTML documentation for the signon-qt

%package tests
Summary: Tests for signon
Requires: %{name} = %{version}-%{release}
Requires: %{name}-testplugin = %{version}-%{release}

%description tests
This package contains tests for signon


%prep
%autosetup -p1 -n %{name}-%{version}/upstream

chmod +x tests/create-tests-definition.sh

%build
%qmake5 TESTDIR=/opt/tests/signon CONFIG+=install_tests CONFIG+=enable-p2p
%make_build

%install
%qmake5_install
rm -f %{buildroot}/%{_docdir}/libsignon-qt/html/installdox
rm -f %{buildroot}/%{_docdir}/signon/html/installdox
rm -f %{buildroot}/%{_docdir}/signon-plugins/html/installdox
rm -f %{buildroot}/%{_docdir}/saslplugin/html/installdox
%fdupes %{buildroot}/%{_docdir}

mkdir -p %{buildroot}%{_datadir}/mapplauncherd/privileges.d
install -m 644 -p %{SOURCE1} %{buildroot}%{_datadir}/mapplauncherd/privileges.d/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n libsignon-qt5 -p /sbin/ldconfig
%postun -n libsignon-qt5 -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/*
%{_libdir}/libsignon-extension.so.*
%{_libdir}/libsignon-plugins-common.so.*
%{_libdir}/libsignon-plugins.so.*
%{_datadir}/dbus-1/services/com.google.code.AccountsSSO.SingleSignOn.service
%{_datadir}/dbus-1/services/com.nokia.SingleSignOn.Backup.service
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.AuthService.xml
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.AuthSession.xml
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.Identity.xml
%{_datadir}/mapplauncherd/privileges.d/*
%config %{_sysconfdir}/signond.conf
# Own to signon library directory
%dir %{_libdir}/signon
%{_libdir}/signon/libpasswordplugin.so
%attr(4710, root, privileged) %{_libexecdir}/signon-storage-perm

%files -n libsignon-qt5
%license COPYING
%{_libdir}/libsignon-qt5.so.*

%files testplugin
%{_libdir}/signon/libssotest*.so

%files exampleplugin
%{_libdir}/signon/libexampleplugin.so

%files devel
%{_includedir}/signond
%{_includedir}/signon-extension
%{_includedir}/signon-plugins
%{_libdir}/libsignon-extension.so
%{_libdir}/libsignon-plugins-common.so
%{_libdir}/libsignon-plugins.so
%{_libdir}/pkgconfig/signond.pc
%{_libdir}/pkgconfig/signon-plugins.pc
%{_libdir}/pkgconfig/signon-plugins-common.pc
%{_libdir}/pkgconfig/SignOnExtension.pc
%{_libdir}/cmake/SignOnQt5
%{_datadir}/dbus-1/interfaces/*

%files -n libsignon-qt5-devel
%{_includedir}/signon-qt5
%{_libdir}/libsignon-qt5.so
%exclude %{_libdir}/libsignon-qt5.a
%{_libdir}/pkgconfig/libsignon-qt5.pc

%files doc
%{_docdir}/signon
%{_docdir}/signon-plugins-dev
%{_docdir}/signon-plugins

%files -n libsignon-qt5-doc
%{_docdir}/libsignon-qt5

%files tests
/opt/tests/signon
