%define debug_package	%{nil}
%define svn	5106
%if %svn
%define release	%mkrel 0.%svn.2
%else
%define release	%mkrel 1
%endif

%define fversion	0.3.4.rc2

Summary:	Media center written in Python
Name:		elisa
Version:	0.3.3.1
Release:	%{release}
%if %svn
# svn co https://code.fluendo.com/elisa/svn/trunk elisa
Source0:	%{name}-%{svn}.tar.lzma
%else
Source0:	http://elisa.fluendo.com/static/download/elisa/%{name}-%{version}.tar.gz
%endif
License:	GPLv3 and MIT
Group:		Development/Python
URL:		http://elisa.fluendo.com/
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	python
BuildRequires:	python-setuptools
BuildRequires:	python-devel
BuildRequires:	python-twisted
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils
BuildRequires:	gstreamer0.10-python
Requires:	pigment-python
Requires:	python-imaging
Requires:	python-twisted
Requires:	gnome-python-extras
Requires:	gstreamer0.10-python
Requires:	python-sqlite2
Requires:	pyxdg
Requires:	python-setuptools
Suggests:	gstreamer0.10-plugins-bad
Suggests:	python-gpod
Suggests:	python-dbus

%description
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intel’s ViiV 
systems.

%prep
%setup -q -n %{name}
# correct mandir
sed -i -e 's,man/man1,share/man/man1,g' elisa-core/setup.py

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{py_puresitedir}
export PYTHONPATH=$PYTHONPATH:%{buildroot}%{py_puresitedir}
./run_elisa_bundles_setups.sh install --root=%{buildroot} --single-version-externally-managed --compile --optimize=2

# Install some stuff manually because the build process can't.
install -D -m644 %{name}-core/data/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -D -m644 %{name}-core/data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Generate and install 32x32 and 16x16 icons.
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 %{name}-core/data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{name}-core/data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu file
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=Elisa Media Center
Comment=Play movies and songs on TV with remote
Exec=%{name} %U
StartupWMClass=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=foo/bar;foo2/bar2;
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;
X-Osso-Service=com.fluendo.elisa
EOF

#don't want these
rm -rf %{buildroot}%{py_puresitedir}/mswin32
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.png
rm -rf %{buildroot}%{_datadir}/mobile-basic-flash

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc elisa-core/{AUTHORS,FAQ,FAQ_EXTRA,FIRST_RUN,HACKING,NEWS,RELEASE,TRANSLATORS}
%{_bindir}/%{name}
%{_bindir}/%{name}-get
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/dbus-1/services/*.service
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}_get.*
%{py_puresitedir}/%{name}_boot.*
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}-nspkg.pth
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}.egg-info
%{py_puresitedir}/%{name}_plugins_good-%{fversion}-py%{pyver}.egg-info
%{py_puresitedir}/%{name}_plugins_bad-%{fversion}-py%{pyver}.egg-info
%{py_puresitedir}/%{name}_plugins_ugly-%{fversion}-py%{pyver}.egg-info
%{py_puresitedir}/%{name}_plugins_good-%{fversion}-py%{pyver}-nspkg.pth
%{py_puresitedir}/%{name}_plugins_bad-%{fversion}-py%{pyver}-nspkg.pth
%{py_puresitedir}/%{name}_plugins_ugly-%{fversion}-py%{pyver}-nspkg.pth
