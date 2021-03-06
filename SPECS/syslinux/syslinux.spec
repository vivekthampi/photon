%global security_hardening none
Summary:	Simple kernel loader which boots from a FAT filesystem
Name:		syslinux
Version:	6.04
Release:	5%{?dist}
License:	GPLv2+
URL:		http://www.syslinux.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.kernel.org/pub/linux/utils/boot/%{name}/Testing/%{version}/%{name}-%{version}-pre1.tar.xz
%define sha1 syslinux=599b7a85d522b1b6658a1fe290e4d23dc64b1470
Source1:        http://downloads.sourceforge.net/libpng/libpng-1.2.59.tar.xz
%define sha1 libpng=4376e9ae6cf23efe63975067c4f135ff1777671a
Source2:        http://www.zlib.net/zlib-1.2.11.tar.xz
%define sha1    zlib=e1cb0d5c92da8e9a8c2635dfa249c341dfd00322
Patch0:		0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
BuildArch:      x86_64
BuildRequires:	nasm
BuildRequires:	util-linux-devel
Requires:	util-linux

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package devel
Summary: Headers and libraries for syslinux development.
Group: Development/Libraries
Provides: %{name}-static = %{version}-%{release}
%description devel
Headers and libraries for syslinux development.

%prep
%setup -q -n %{name}-%{version}-pre1
%patch0 -p1

# to have higher versions of libpng, zlib
rm -rf com32/lib/libpng/
rm -rf com32/lib/zlib/
tar xf %{SOURCE1} -C com32/lib/
tar xf %{SOURCE2} -C com32/lib/
mv com32/lib/libpng-1.2.59 com32/lib/libpng
mv com32/lib/zlib-1.2.11 com32/lib/zlib

%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' extlinux/main.c
make bios clean all
%install
make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32
rm -rf %{buildroot}/boot
rm -rf %{buildroot}/tftpboot
# remove it unless provide perl(Crypt::PasswdMD5)
rm %{buildroot}/%{_bindir}/md5pass
# remove it unless provide perl(Digest::SHA1)
rm %{buildroot}/%{_bindir}/sha1pass
%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %{_datadir}/syslinux/com32
%exclude %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_datadir}/syslinux/com32/*

%changelog
*   Tue Jun 04 2019 Ajay Kaher <akaher@vmware.com> 6.04-5
-   Upgrade zlib to v1.2.11 and libpng to v1.2.59
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 6.04-4
-   Adding BuildArch
*   Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 6.04-3
-   Fix compilation issue against glibc-2.28
*   Wed Oct 25 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-2
-   Remove md5pass and sha1pass tools
*   Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-1
-   Initial version
