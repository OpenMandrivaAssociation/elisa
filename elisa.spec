Summary:	Media center written in Python
Name:		elisa
Version:	0.3.2
Release:	%mkrel 1
Source0:	http://elisa.fluendo.com/static/download/elisa/%{name}-%{version}.tar.gz
License:	GPLv2 and MIT
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
Requires:	pigment
Requires:	python-imaging
Requires:	python-twisted
Requires:	gnome-python-extras
Requires:	gstreamer0.10-python
Requires:	python-sqlite2
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
%setup -q

%build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot}

# Install some stuff manually because the build process can't.

install -D -m644 data/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -D -m644 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Generate and install 32x32 and 16x16 icons.

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Desktop entry.

desktop-file-install --vendor="" \
  --remove-category="X-Ximian-Main" \
  --remove-category=";X-Red-Hat-Base" \
  --remove-key="Version" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

# Delete silly unused icon.

rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.png

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
%doc AUTHORS FAQ FAQ_EXTRA FIRST_RUN HACKING NEWS RELEASE TRANSLATORS
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}-%{version}-py%pyver.egg-info
