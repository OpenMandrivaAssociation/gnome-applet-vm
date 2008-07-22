%define	name	gnome-applet-vm
%define	version	0.1.2
%define	release	%mkrel 5

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    Simple virtual domains monitor
License:    GPL
Group:      Graphical desktop/GNOME
URL:        http://people.redhat.com/kzak/gnome-applet-vm
Source:     http://people.redhat.com/kzak/gnome-applet-vm/%{name}-%{version}.tar.bz2

BuildRequires:  libvirt-devel
BuildRequires:  gnome-panel-devel >= 2.5.91
BuildRequires:  gnome-doc-utils
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
%setup -q -n %{name}-%{version}

%build
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
%doc AUTHORS COPYING ChangeLog NEWS README
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


