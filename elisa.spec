%define name elisa
%define version 0.1.6
%define release %mkrel 1

Summary: Media center written in Python
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://elisa.fluendo.com/static/download/elisa/%{name}-%{version}.tar.bz2
License: GPL, MIT
Group: Development/Python
Url: https://core.fluendo.com/pigment/trac
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python
BuildRequires: python-setuptools
BuildRequires: python-devel
BuildRequires: python-twisted
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires: pigment
Requires: python-imaging
Requires: python-twisted
Requires: gnome-python-extras
Requires: gstreamer0.10-python
Requires: python-sqlite2

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
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

# Install some stuff manually because the build process can't.

install -D -m644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m644 %{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -D -m644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -D -m644 %{name}.png %{buildroot}%{_liconsdir}/%{name}.png

# Generate and install 32x32 and 16x16 icons.

mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 %{name}.png %{buildroot}%{_iconsdir}/%{name}.png
convert -scale 32 %{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{name}.png %{buildroot}%{_miconsdir}/%{name}.png
convert -scale 16 %{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Desktop entry.

desktop-file-install --vendor="" \
  --remove-category="X-Ximian-Main" \
  --remove-category=";X-Red-Hat-Base" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README.txt 
%{_bindir}/%{name}
%{_bindir}/%{name}-client
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/*
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}-%{version}-py%pyver.egg-info
