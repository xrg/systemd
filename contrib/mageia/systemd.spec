%define git_repo systemd
%define git_head HEAD

%define libsystemd_major 0
%define libudev_major 1
%define libgudev_api 1.0
%define libgudev_major 0

%define libname %mklibname %{name} %{libsystemd_major}

%define libdaemon %mklibname systemd-daemon 0
%define libjournal %mklibname systemd-journal 0
%define liblogin %mklibname systemd-login 0
%define libid128 %mklibname systemd-id 128 0

%define libudev %mklibname udev %{libudev_major}
%define libudev_devel %mklibname -d udev

%define libgudev %mklibname gudev %{libgudev_api} %{libgudev_major}
%define libgudev_devel %mklibname -d gudev %{libgudev_api}
%define libgudev_gir %mklibname gudev-gir %{libgudev_api}

Summary:	A System and Session Manager
Name:		systemd
Version:	%git_get_ver
%define subrel	1
Release:	%mkrel %git_get_rel2
License:	GPLv2+
Group:		System/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source:		%git_bs_source %{name}-%{version}.tar.gz
Source1:	%{name}-gitrpm.version
Source2:	%{name}-changelog.gitrpm.txt

# (hk) udev rules for zte 3g modems with drakx-net

# (blino) net rules and helpers

# (cg) Upstream cherry picks
# (not technically upstream yet, but confident it will be...)
# (doktor5000) backported from 221, supposedly fixes mga#16396
# see http://cgit.freedesktop.org/systemd/systemd/commit/?id=41dfeaa194c18de49706b5cecf4e53accd12b7f6 for details

# (cg/bor) clean up directories on boot as done by rc.sysinit
# - Lennart should be poked about this (he couldn't think why he hadn't done it already)

BuildRequires:	dbus-devel >= 1.4.0
BuildRequires:	libcap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pam-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	vala >= 0.9
BuildRequires:	glib2-devel
BuildRequires:	libnotify-devel
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	gperf
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	cryptsetup-devel
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	python-devel
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(python)
BuildRequires:	python-lxml
# (cg) don't add more deps for now but add this when cauldron reopens.
#BuildRequires:	pkgconfig(libqrencode)
Requires(pre):	filesystem >= 2.1.9-18
Requires(pre):	shadow-utils
Requires:	systemd-units = %{version}-%{release}
Requires:	dbus >= 1.3.2
Requires:	initscripts >= 9.21-3
Requires:	util-linux-ng >= 2.18
Requires:	nss-myhostname
Requires:	lockdev
Conflicts:	initscripts < 9.25
Provides:	should-restart = system
Provides: udev = %{version}-%{release}
Obsoletes: udev < 185
Provides:  systemd-sysvinit = %{version}-%{release}
Conflicts: systemd-sysvinit < 185
Obsoletes: systemd-sysvinit < 185
Provides:  sysvinit = 2.87-22
Obsoletes: sysvinit < 2.87-22
Conflicts: SysVinit
# Due to halt/poweroff etc. in _bindir
Conflicts: usermode-consoleonly < 1:1.110
Provides:  system-logger
# (blino) consolekit has been replaced by systemd-logind
Obsoletes: consolekit
Obsoletes: consolekit-x11
Obsoletes: libconsolekit0
Obsoletes: lib64consolekit0
Obsoletes: systemd-tools
Obsoletes: bootchart
Obsoletes: bootchart-daemon

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		System/Boot and Init
Requires(pre):	filesystem >= 2.1.9-18
Requires:	%{name} = %{version}-%{release}
Requires:	chkconfig > 1.3.61-2
Conflicts:	%{name} <= 216-10
Conflicts:	initscripts < 9.25
Requires(post): coreutils grep awk

%description units
Basic configuration files, directories and installation tool for the systemd
system and session manager.

%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python

%description -n python-%{name}
Python bindings for %{name}

%package devel
Summary:       Systemd development files
Group:         Development/C
Conflicts:     %{name} <= 35-4
Requires:      %{libname} = %{version}-%{release}
#Obsoletes:     %{libdaemon}
#Obsoletes:     %{liblogin}
#Obsoletes:     %{libid128}
#Obsoletes:     %{libjournal}
# (cg) Obsolete the old, versioned/split devel packages
Provides:      libsystemd-daemon-devel = %{version}-%{release}
Provides:      %{mklibname -d systemd-daemon 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-daemon 0} < 185
Provides:      %{mklibname -d systemd-daemon} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-daemon} < 186
Provides:      libsystemd-login-devel = %{version}-%{release}
Provides:      %{mklibname -d systemd-login 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-login 0} < 185
Provides:      %{mklibname -d systemd-login} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-login} < 186
Provides:      libsystemd-journal-devel = %{version}-%{release}
Provides:      %{mklibname -d systemd-journal 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-journal 0} < 185
Provides:      %{mklibname -d systemd-journal} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-journal} < 186
Provides:      libsystemd-id128-devel = %{version}-%{release}
Provides:      %{mklibname -d systemd-id128 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-id128 0} < 185
Provides:      %{mklibname -d systemd-id128} = %{version}-%{release}
Obsoletes:     %{mklibname -d systemd-id128} < 186
# (cg) Provide old autogenerated names until other devel packages are rebuilt
%ifarch x86_64
Provides: devel(libsystemd-id128(64bit))
Provides: devel(libsystemd-journal(64bit))
Provides: devel(libsystemd-login(64bit))
Provides: devel(libsystemd-daemon(64bit))
%else
Provides: devel(libsystemd-id128)
Provides: devel(libsystemd-journal)
Provides: devel(libsystemd-login)
Provides: devel(libsystemd-daemon)
%endif

%description devel
This package provides the development files for systemd.

%package -n nss-myhostname
Summary:	systemd provided glibc plugin for local system host name resolution
Group:		System/Base

%description -n nss-myhostname
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2). Various software relies on an always resolvable local
host name. When using dynamic hostnames this is usually achieved by
patching /etc/hosts at the same time as changing the host name. This
however is not ideal since it requires a writable /etc file system and
is fragile because the file might be edited by the administrator at
the same time. nss-myhostname simply returns all locally configure
public IP addresses, or -- if none are configured -- the IPv4 address
127.0.0.2 (wich is on the local loopback) and the IPv6 address ::1
(which is the local host) for whatever system hostname is configured
locally. Patching /etc/hosts is thus no longer necessary.

%package -n %{libname}
Summary:       Systemd library package
Group:         System/Libraries

%description -n %{libname}
This package provides the systemd shared library.

%package -n %{libudev}
Summary:       udev library package
Group:         System/Libraries
Requires(pre): filesystem >= 2.1.9-18

%description -n %{libudev}
This package provides the udev shared library.

%package -n %{libudev_devel}
Summary:       udev library development files
Group:         Development/C
Requires:      %{libudev} = %{version}-%{release}
Provides:      udev-devel = %{version}-%{release}
Provides:      libudev-devel = %{version}-%{release}
# (cg) Obsolete the old, versioned devel package
Provides:      %{mklibname -d udev 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d udev 0} < 185

%description -n %{libudev_devel}
This package provides the development files for the udev shared library.

%package -n %{libgudev}
Summary:       gudev library package
Group:         System/Libraries
Requires(pre): filesystem >= 2.1.9-18
Provides:      libgudev = %{version}-%{release}

%description -n %{libgudev}
This package provides the gudev shared library.

%package -n %{libgudev_gir}
Summary:       GObject Introspection interface description for GUdev
Group:         System/Libraries
Requires:      %{libgudev} = %{version}-%{release}
Conflicts:     %{_lib}gudev1.0_0 < 187-5

%description -n %{libgudev_gir}
GObject Introspection interface description for GUdev.


%package -n %{libgudev_devel}
Summary:       gudev library development files
Group:         Development/C
Requires:      %{libgudev} = %{version}-%{release}
Provides:      libgudev-devel = %{version}-%{release}
# (cg) Obsolete the old, versioned devel package
Provides:      %{mklibname -d gudev 0} = %{version}-%{release}
Obsoletes:     %{mklibname -d gudev 0} < 185

%description -n %{libgudev_devel}
This package provides the development files for the gudev shared library.


%prep
%git_get_source
%setup -q
find src/ -name "*.vala" -exec touch '{}' \;

%build
autoreconf --force --install --verbose
#NO_CONFIGURE=1 ./autogen.sh
%configure2_5x \
  --with-rc-local-script-path-start=/etc/rc.d/rc.local \
  --enable-chkconfig \
  --enable-compat-libs \
  --disable-static \
  --disable-selinux \
  --with-firmware-path=%{_prefix}/lib/firmware/updates:%{_prefix}/lib/firmware

%make

%install
%makeinstall_std
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;

# (cg) Create and ship folder to hold user rules
install -d -m 755 %{buildroot}%{_sysconfdir}/udev/rules.d

install -m 644 contrib/mageia/50-udev-mageia.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 contrib/mageia/69-printeracl.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
# udev rules for zte 3g modems and drakx-net
install -m 0644 contrib/mageia/61-mobile-zte-drakx-net.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# net rules
install -m 0644 contrib/mageia/81-net.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 0755 contrib/mageia/udev_net_create_ifcfg %{buildroot}%{_prefix}/lib/udev/net_create_ifcfg
install -m 0755 contrib/mageia/udev_net_action %{buildroot}%{_prefix}/lib/udev/net_action
install -m 0755 -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 contrib/mageia/udev_net.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/udev_net


# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}{%{_bindir},%{_sbindir}}
ln -s ../lib/systemd/systemd %{buildroot}%{_bindir}/systemd
ln -s ../lib/systemd/systemd %{buildroot}%{_sbindir}/init
ln -s ../bin/systemctl %{buildroot}%{_bindir}/reboot
ln -s ../bin/systemctl %{buildroot}%{_bindir}/halt
ln -s ../bin/systemctl %{buildroot}%{_bindir}/poweroff
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/shutdown
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/telinit
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/runlevel

# Also add a symlink for udevadm for now as lots of things use an absolute path
ln -s ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# (cg) Add aliases for prefdm.service
ln -s prefdm.service %{buildroot}%{_prefix}/lib/systemd/system/display-manager.service
ln -s prefdm.service %{buildroot}%{_prefix}/lib/systemd/system/dm.service

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants

# (cg) To avoid making life hard for developers, don't package the
# kernel.core_pattern setting until systemd-coredump is a part of an actual
# systemd release and it's made clear how to get the core dumps out of the
# journal.
rm -f %{buildroot}%{_prefix}/lib/sysctl.d/50-coredump.conf

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/basic.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/default.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/syslog.target.wants

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/systemd/system/default.target

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/bluetooth.target.wants

# (cg) Set up the pager to make it generally more useful
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh << EOF
export SYSTEMD_PAGER="/usr/bin/less -FR"
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh

# (bor) enable rpcbind.target by default so we have something to plug
# portmapper service into
ln -s ../rpcbind.target %{buildroot}%{_prefix}/lib/systemd/system/multi-user.target.wants

# create modules.conf as a symlink to /etc/
ln -s /etc/modules %{buildroot}%{_sysconfdir}/modules-load.d/modules.conf

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/timezone
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
mkdir -p %{buildroot}%{_sysconfdir}/udev
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin

# (cg) Make the journal's persistent in order to provide a real syslog implementation
install -m 0755 -d %{buildroot}%{_logdir}/journal

# (cg) Default preset policy
# (for now, just a placeholder directory)
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset

# Various filetriggers
install -d %{buildroot}%{_var}/lib/rpm/filetriggers

# automatic systemd release on rpm installs/removals
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
# (cg) I'm not sure if the file list check works against the packaged rpm
#      or what is installed, so I've added both the /lib and /usr/lib paths
#      below, even thought the former is just a symlink to the latter
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.filter << EOF
^./((usr/)?lib/systemd/system/|etc(/rc.d)?/init.d/)
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.script << EOF
#!/bin/sh
if %{_bindir}/mountpoint -q /sys/fs/cgroup/systemd; then
  if [ -x %{_bindir}/systemctl ]; then
    %{_bindir}/systemctl daemon-reload >/dev/null 2>&1 || :
  fi
fi
EOF
chmod 0755 %buildroot%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.script


# sysusers (make sure to run before tmpfiles)
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/01-sysusers.filter << EOF
^./usr/lib/sysusers.d/
EOF
# TODO Make sysusers support --quiet
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/01-sysusers.script << EOF
#!/bin/sh
exec %{_bindir}/systemd-sysusers
EOF
chmod 0755 %{buildroot}%{_var}/lib/rpm/filetriggers/01-sysusers.script


# tmpfiles (make sure to run early just incase the tmpfiles created are needed by other filetriggers)
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/02-tmpfiles.filter << EOF
^./usr/lib/tmpfiles.d/
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/02-tmpfiles.script << EOF
#!/bin/sh
exec %{_bindir}/systemd-tmpfiles --create
EOF
chmod 0755 %{buildroot}%{_var}/lib/rpm/filetriggers/02-tmpfiles.script


# hwdb
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/hwdb.filter << EOF
^./usr/lib/udev/hwdb.d/
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/hwdb.script << EOF
#!/bin/sh
exec %{_bindir}/udevadm hwdb --update
EOF
chmod 0755 %{buildroot}%{_var}/lib/rpm/filetriggers/hwdb.script


# journal catalog
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/journal-catalog.filter << EOF
^./usr/lib/systemd/catalog/
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/journal-catalog.script << EOF
#!/bin/sh
exec %{_bindir}/journalctl --update-catalog
EOF
chmod 0755 %{buildroot}%{_var}/lib/rpm/filetriggers/journal-catalog.script



# This file is already in sytemd-ui rpm
rm -fr %{buildroot}%_mandir/man1/systemadm.*

# (cg) These are the compat libs but we don't need them in cauldron.
# All we need is the pkgconfig files so we can rebuild everything and
# kill off the need for the old library packages (which will remain installed
# and operational due to our packaging policy)
for lib in daemon id128 journal login; do
  rm -f %{buildroot}%{_libdir}/libsystemd-$lib.so{,.0.*}
done

%find_lang %{name}


%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
	%{_bindir}/systemctl daemon-reexec 2>&1 || :
fi

%pre
# (cg) Cannot use rpm-helper scripts as it results in a cyclical dep as
# rpm-helper requires systemd-units which in turn requires systemd...
if ! getent group %{name}-journal >/dev/null 2>&1; then
  /usr/sbin/groupadd -r %{name}-journal >/dev/null || :
fi

# Write on first install or upgrade from MGA3.
if [ ! -r %{_prefix}/lib/sysctl.d/50-default.conf ]; then
  if [ ! -d %{_sysconfdir}/sysctl.d ]; then
    mkdir -m 0755 %{_sysconfdir}/sysctl.d
  fi
  cat > %{_sysconfdir}/sysctl.d/51-alt-sysrq.conf << EOF
# This file ensures that the Alt+SysRq Magic keys still work.
# This setting is insecure, although commonly expected and you can remove this
# file to disable this feature. It will not be readded on future systemd
# upgrades/updates.
# http://en.wikipedia.org/wiki/Magic_SysRq_key#Security
kernel.sysrq = 1
EOF

fi

%post
%{_bindir}/systemd-machine-id-setup > /dev/null 2>&1 || :
%{_prefix}/lib/systemd/systemd-random-seed save >/dev/null 2>&1 || :
#%{_bindir}/systemctl daemon-reexec > /dev/null 2>&1 || :

# (blino) systemd 195 changed the prototype of logind's OpenSession()
# see http://lists.freedesktop.org/archives/systemd-devel/2012-October/006969.html
# and http://cgit.freedesktop.org/systemd/systemd/commit/?id=770858811930c0658b189d980159ea1ac5663467
%triggerun -- %{name} < 195-4.mga3
%{_bindir}/systemctl restart systemd-logind.service

# (cg) mageia 4 introduces the Consistent Network Device Names feature
# https://wiki.mageia.org/en/Feature:NetworkDeviceNameChange
# To prevent it being enabled on upgrades and breaking configs, we ensure the
# feature is disabled when we detect an older version of systemd being removed.
%triggerun -- %{name} < 206
echo >&2
echo "Disabling Persistent Network Device Names due to upgrade." >&2
echo "To enable, rm %{_sysconfdir}/udev/rules.d/80-net-name-slot.rules and your" >&2
echo "%{_sysconfdir}/udev/rules.d/70-persistent-net.rules files." >&2
echo "Note: Some reconfiguration of firewall and network config scripts will also" >&2
echo "      be required if you do this" >&2
echo >&2
mkdir -p %{_sysconfdir}/udev/rules.d >/dev/null 2>&1 || :
ln -s /dev/null %{_sysconfdir}/udev/rules.d/80-net-name-slot.rules >/dev/null 2>&1 || :

%triggerun -- %{name} < 208
chgrp -R systemd-journal /var/log/journal || :
chmod 02755 /var/log/journal || :
if [ -f /etc/machine-id ]; then
	chmod 02755 /var/log/journal/$(cat /etc/machine-id) || :
fi

%post units
if [ $1 -eq 1 ] ; then
        # Try to read default runlevel from the old inittab if it exists
        runlevel=$(%{_bindir}/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
        if [ -z "$runlevel" ] ; then
                target="%{_prefix}/lib/systemd/system/multi-user.target"
        else
                target="%{_prefix}/lib/systemd/system/runlevel$runlevel.target"
        fi

        # And symlink what we found to the new-style default.target
        %{_bindir}/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target || :

        # Enable the services we install by default.
        %{_bindir}/systemctl --quiet preset \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                systemd-timesyncd.service \
                systemd-networkd.service \
                systemd-networkd-wait-online.service \
                systemd-resolved.service \
                2>/dev/null || :
fi

hostname_new=`cat %_sysconfdir/hostname 2>/dev/null`
if [ -z $hostname_new ]; then
        hostname_old=`cat /etc/sysconfig/network 2>/dev/null | grep HOSTNAME | cut -d "=" -f2`
        if [ ! -z $hostname_old ]; then
                echo $hostname_old >> %_sysconfdir/hostname
        else
                echo "localhost" >> %_sysconfdir/hostname
        fi
fi

%preun units
if [ $1 -eq 0 ] ; then
        %{_bindir}/systemctl --quiet disable \
                getty@.service \
                remote-fs.target \
                2>&1 || :

        %{_bindir}/rm -f %_sysconfdir/systemd/system/default.target 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ] ; then
        %{_bindir}/systemctl daemon-reload 2>&1 || :
fi

%triggerin units -- %{name}-units < 215
        # Enable the services we install by default.
        %{_bindir}/systemctl --quiet preset systemd \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                systemd-timesyncd.service \
                systemd-networkd.service \
                systemd-networkd-wait-online.service \
                systemd-resolved.service \
                2>/dev/null || :
        # rc-local is now enabled by default in base package
        # and read-ahead stuff is no more
        rm -f %_sysconfdir/systemd/system/multi-user.target.wants/rc-local.service \
              %_sysconfdir/systemd/system/default.target.wants/systemd-readahead-{collect,replay}.service || :

%files -f %{name}.lang
# (cg) Note some of these directories are empty, but that is intended
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/system-generators
%dir %{_prefix}/lib/systemd/system-shutdown
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_prefix}/lib/systemd/network
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%dir %{_prefix}/lib/binfmt.d
%{_var}/lib/rpm/filetriggers/*.filter
%{_var}/lib/rpm/filetriggers/*.script
%config(noreplace) %{_sysconfdir}/sysconfig/udev_net
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-remote.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%ghost %{_sysconfdir}/udev/hwdb.bin
%{_sysconfdir}/xdg/systemd
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
# (cg) NB dbus policy files are not really config that users are expected to
# edit manually and thus should NOT be marked as config(noreplace).
# This should really be fixed in upstream dbus (work in progress)
# to separate these policy files from /etc and ship them in /usr instead
# but allow override by admins by copying to /etc.
# There are security implications here (CVE's have been issued due to mistakes
# in these type of files)
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%{_sysconfdir}/pam.d/%{name}-user
%dir %{_sysconfdir}/udev/rules.d
%{_prefix}/lib/systemd/network/80-container-host0.network
%{_prefix}/lib/systemd/network/80-container-ve.network
%{_prefix}/lib/systemd/network/99-default.link
# (cg) NB See pre script for soemthing that relies on this name...
# If it is ever renamed, change the pre script too
%{_prefix}/lib/sysctl.d/50-default.conf
#%{_prefix}/lib/sysctl.d/50-coredump.conf
%{_prefix}/lib/sysusers.d/basic.conf
%{_prefix}/lib/sysusers.d/systemd.conf
%{_prefix}/lib/sysusers.d/systemd-remote.conf
%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/legacy.conf
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/systemd-remote.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/kernel/install.d/50-depmod.install
%{_prefix}/lib/kernel/install.d/90-loaderentry.install
%{_bindir}/bootctl
%{_bindir}/busctl
%{_bindir}/coredumpctl
%{_bindir}/hostnamectl
%{_bindir}/journalctl
%{_bindir}/kernel-install
%{_bindir}/localectl
%{_bindir}/loginctl
%{_bindir}/machinectl
%{_bindir}/networkctl
%{_bindir}/systemd
%{_bindir}/systemd-ask-password
%{_bindir}/systemd-escape
%{_bindir}/systemd-firstboot
%{_bindir}/systemd-inhibit
%{_bindir}/systemd-machine-id-setup
%{_bindir}/systemd-notify
%{_bindir}/systemd-path
%{_bindir}/systemd-run
%{_bindir}/systemd-sysusers
%{_bindir}/systemd-tmpfiles
%{_bindir}/systemd-tty-ask-password-agent
%{_bindir}/timedatectl
%{_bindir}/reboot
%{_bindir}/halt
%{_bindir}/poweroff
%{_sbindir}/shutdown
%{_sbindir}/init
%{_sbindir}/telinit
%{_sbindir}/runlevel
%{_sbindir}/udevadm
%{_prefix}/lib/systemd/systemd*
%{_prefix}/lib/systemd/system-generators/systemd-*
%{_prefix}/lib/udev
%{_libdir}/security/pam_systemd.so
%{_bindir}/systemd-analyze
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/udevadm
%dir %{_datadir}/systemd
%{_datadir}/systemd/kbd-model-map
%dir %{_datadir}/systemd/gatewayd
%{_datadir}/systemd/gatewayd/browse.html
%{_mandir}/man1/bootctl.*
%{_mandir}/man1/busctl.*
%{_mandir}/man1/coredumpctl.*
%{_mandir}/man1/hostnamectl.*
%{_mandir}/man1/journalctl.*
%{_mandir}/man1/localectl.*
%{_mandir}/man1/loginctl.*
%{_mandir}/man1/machinectl.*
%{_mandir}/man1/systemd.*
%{_mandir}/man1/systemd-*
%{_mandir}/man1/timedatectl.*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/kernel-install.*
%{_mandir}/man8/pam_systemd.*
%{_mandir}/man8/systemd-*
%{_mandir}/man8/udevadm.*
%{_mandir}/man1/init.*
%{_mandir}/man8/halt.*
%{_mandir}/man8/reboot.*
%{_mandir}/man8/shutdown.*
%{_mandir}/man8/poweroff.*
%{_mandir}/man8/telinit.*
%{_mandir}/man8/runlevel.*
%{_sysconfdir}/init.d/README
%{_logdir}/README
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%{_datadir}/factory/etc/nsswitch.conf
%dir %{_datadir}/factory/etc/pam.d
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_docdir}/systemd
%{_prefix}/lib/systemd/catalog/systemd.catalog
%lang(fr) %{_prefix}/lib/systemd/catalog/systemd.fr.catalog
%lang(it) %{_prefix}/lib/systemd/catalog/systemd.it.catalog
%lang(ru) %{_prefix}/lib/systemd/catalog/systemd.ru.catalog
%lang(pl) %{_prefix}/lib/systemd/catalog/systemd.pl.catalog
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal

%files units
# (cg) Note some of these directories are empty, but that is intended
# NB I'm not totally sure of the ownership split of directories between systemd and systemd-units.
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_datadir}/bash-completion
%{_bindir}/systemctl
%{_datadir}/bash-completion/completions
%{_datadir}/zsh/site-functions
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/modules-load.d/*.conf
%{_prefix}/lib/systemd/system
%{_prefix}/lib/systemd/system-preset
%{_prefix}/lib/systemd/user
%{_prefix}/lib/systemd/user-preset
%{_mandir}/man1/systemctl.*

%files -n python-%{name}
%{py_platsitedir}/%{name}

%files devel
%{_includedir}/systemd
%{_libdir}/libsystemd*.so
%{_libdir}/pkgconfig/libsystemd*.pc
%{_datadir}/pkgconfig/systemd.pc
%{_prefix}/lib/rpm/macros.d/macros.systemd

%files -n nss-myhostname
%{_mandir}/man8/nss-myhostname.*
%{_libdir}/libnss_myhostname.so.2
# (cg) Yes, this is a hack for now, I'll likely rename the package to just lib[64]systemd-nss2 or something...
%{_libdir}/libnss_mymachines.so.2
%{_libdir}/libnss_resolve.so.2

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libsystemd.so.%{libsystemd_major}*

%files -n %{libudev}
%{_libdir}/libudev.so.%{libudev_major}*

%files -n %{libudev_devel}
%{_libdir}/libudev.so
%{_includedir}/libudev.h
%{_datadir}/pkgconfig/udev.pc
%{_libdir}/pkgconfig/libudev.pc

%files -n %{libgudev}
%{_libdir}/libgudev-%{libgudev_api}.so.%{libgudev_major}*

%files -n %{libgudev_gir}
%{_libdir}/girepository-1.0/GUdev-%{libgudev_api}.typelib

%files -n %{libgudev_devel}
%{_libdir}/libgudev-%{libgudev_api}.so
%{_includedir}/gudev-%{libgudev_api}
%{_libdir}/pkgconfig/gudev-%{libgudev_api}.pc
%{_datadir}/gir-1.0/GUdev-%{libgudev_api}.gir
