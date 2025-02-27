%define	name	gnome-applet-vm
%define	version	0.2.0
%define	beta    rc1
%define	release	%mkrel 0.%{beta}.5

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    Simple virtual domains monitor
License:    GPL
Group:      Graphical desktop/GNOME
URL:        https://people.redhat.com/kzak/gnome-applet-vm
Source:     http://people.redhat.com/kzak/gnome-applet-vm/v0.2/%{name}-%{version}-%{beta}.tar.bz2
Patch:      gnome-applet-vm-0.2.0-rc1-fix-format-errors.patch
BuildRequires:  libvirt-devel
BuildRequires:  gnome-panel-devel >= 2.5.91
BuildRequires:  libglade2-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  gnomeui2-devel libgnome2-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig
BuildRequires:  libxslt-proc
Requires:	    xen
Requires:	    gnome-panel >= 2.5.91
Requires:	    usermode
Requires:	    virt-manager
Requires(post):		scrollkeeper >= 0.3
Requires(postun):   scrollkeeper >= 0.3
BuildRoot:           %{_tmppath}/%{name}-%{version}

%description
The gnome-applet-vm is GNOME panel applet for monitoring and controlling 
locally-running virtual machines.

%prep
%setup -q -n %{name}-%{version}-%{beta}
%patch -p 1

%build
export CPPFLAGS="$CPPFLAGS -I %{_includedir}/libgnomeui-2.0"
export LDFLAGS="$LDFLAGS -lgnomeui-2"
%configure2_5x --enable-consolehelper
%make

%install
rm -rf %{buildroot}

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=%{buildroot}
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean up unpackaged files
rm -rf %{buildroot}%{_localstatedir}/lib/scrollkeeper
# userhelper
mkdir -p %{buildroot}/%{_bindir}
ln -s consolehelper %{buildroot}/%{_bindir}/vm_applet_wrapper

%clean
rm -rf %{buildroot}

%post
%update_scrollkeeper
%post_install_gconf_schemas vm-applet

%preun
%preun_uninstall_gconf_schemas vm-applet

%postun
%clean_scrollkeeper

%files
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README TODO COPYING-DOCS
%{_datadir}/pixmaps/vm-applet
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome/help/*
%{_datadir}/omf/*
%{_libdir}/bonobo/servers/GNOME_VmApplet.server
%{_libdir}/vm_applet
%{_sbindir}/vm_applet_wrapper
%{_bindir}/vm_applet_wrapper
%{_sysconfdir}/gconf/schemas/*
%config(noreplace) %{_sysconfdir}/pam.d/vm_applet_wrapper
%config(noreplace) %{_sysconfdir}/security/console.apps/vm_applet_wrapper


