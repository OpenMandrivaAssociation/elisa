%define major 0
%define libname %mklibname %{name} %{major}

Summary:	A powerful media player for Plasma
Name:		elisa
Version:	0.3.0
Epoch:		1
Release:	1
License:	LGPLv2+
Group:		Sound
Url:		https://community.kde.org/Elisa
Source0:	https://download.kde.org/stable/%{name}/%{version}/%{name}-%{version}.tar.xz
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5Archive)
BuildRequires:	cmake(KF5ConfigWidgets)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Crash)
BuildRequires:	cmake(KF5Baloo)
BuildRequires:	cmake(KF5Declarative)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(KF5FileMetaData)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5KCMUtils)
BuildRequires:	cmake(KF5XmlGui)
BuildRequires:	cmake(KF5DBusAddons)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(Qt5Core) >= 5.9.0
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5QuickTest)
BuildRequires:	pkgconfig(Qt5WebSockets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
Requires:	qt5-qtquickcontrols2
Requires:	%{libname} = %{EVRD}

%description
A powerful media player for Plasma.

%package -n %{libname}
Summary:	Library for %{name}.
Group:	System/Libraries

%description -n %{libname}
Library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}Lib.so.%{major}*

%files -f %{name}.lang
%{_bindir}/elisa
%{_datadir}/applications/org.kde.elisa.desktop
%{_datadir}/kservices5//kcm_elisa_local_file.desktop
%{_datadir}/kpackage/kcms/kcm_elisa_local_file/
%{_iconsdir}/hicolor/scalable/apps/elisa.svg
%{_iconsdir}/hicolor/*/apps/elisa.png
%{_datadir}/metainfo/org.kde.elisa.appdata.xml
%{_qt5_plugindir}/kcms/kcm_elisa_local_file.so
%{_libdir}/qt5/qml/org/kde/elisa/libelisaqmlplugin.so
%{_libdir}/qt5/qml/org/kde/elisa/qmldir
%{_docdir}/HTML/*/elisa

#--------------------------------------------------------------------

%prep
%autosetup -p1

%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

rm -rf %{buildroot}%{_libdir}/libelisaLib.so

%find_lang %{name} --with-kde --all-name

