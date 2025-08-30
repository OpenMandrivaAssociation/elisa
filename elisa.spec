#define git 20240218
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define _cmake_skip_rpath %nil

Summary:	A powerful media player for Plasma
Name:		elisa
Version:	25.08.0
Release:	%{?git:0.%{git}.}1
License:	LGPLv2+
Group:		Sound
Url:		https://community.kde.org/Elisa
%if 0%{?git:1}
Source0:	https://invent.kde.org/multimedia/elisa/-/archive/%{gitbranch}/elisa-%{gitbranchd}.tar.bz2#/elisa-%{git}.tar.bz2
%else
Source0:	https://download.kde.org/%{stable}/release-service/%{version}/src/elisa-%{version}.tar.xz
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6Archive)
BuildRequires:	cmake(KF6ConfigWidgets)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6Baloo)
BuildRequires:	cmake(KF6Declarative)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6FileMetaData)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6KirigamiAddons)
BuildRequires:  cmake(KF6Kirigami2)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(KF6QQC2DesktopStyle)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(libvlc)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Multimedia)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6QuickWidgets)
BuildRequires:	pkgconfig(Qt6QuickControls2)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(Qt6QuickTest)
BuildRequires:	pkgconfig(Qt6WebSockets)
BuildRequires:	pkgconfig(Qt6Widgets)
# libvlc5 is not pulled at installation time and if user remove VLC, then Elisa is completly broken. So let's force it (angry)
# https://forum.openmandriva.org/t/elisa-crash-on-rock/3700/16
Requires: %{_lib}vlc5
Requires: vlc-plugin-pulse

%rename %{_lib}%{name}0
%rename plasma6-elisa

BuildSystem:	cmake
BuildOption:	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON

%description
A powerful media player for Plasma.

%files -f elisa.lang
%dir %{_libdir}/elisa
%{_bindir}/elisa
%{_libdir}/elisa/*.so*
%{_datadir}/applications/org.kde.elisa.desktop
%{_datadir}/qlogging-categories6/elisa.categories
%{_iconsdir}/hicolor/scalable/apps/elisa.svg
%{_iconsdir}/hicolor/*/apps/elisa.png
%{_datadir}/metainfo/org.kde.elisa.appdata.xml
#{_libdir}/qt6/qml/org/kde/elisa/libelisaqmlplugin.so
#{_libdir}/qt6/qml/org/kde/elisa/qmldir
#{_libdir}/qt6/qml/org/kde/elisa/plugins.qmltypes
%{_datadir}/dbus-1/services/org.kde.elisa.service
