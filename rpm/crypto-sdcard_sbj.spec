Name:       	crypto-sdcard_sbj
Summary:    	Configuration files for unlocking and mounting encrypted SD-cards automatically ("sbj" edition)
Version:    	1.1
Release:    	1
Group:      	System/Base
Distribution:	SailfishOS
Vendor:     	olf
Packager:   	olf
License:    	MIT
URL:        	https://github.com/Olf0/%{name}
Source:     	%{name}-%{version}-%{release}.tar.gz
Source1:    	https://github.com/Olf0/%{name}/archive/%{version}-%{release}.tar.gz
BuildArch:  	noarch
Requires:   	systemd
Requires:   	polkit
Requires:   	udisks2
Requires:   	cryptsetup >= 1.4.0
Conflicts:  	crypto-sdcard

%description
%{summary}
"Key"-file naming scheme: /etc/crypto-sdcard/crypto_luks_<UUID>.key rsp. /etc/crypto-sdcard/crypto_plain_<device-name>.key
This "sbj" edition is specifically for devices, which need the qcrypto kernel module loaded to support modern cryptographic schemes as e.g. XTS.  For all other devices, the generic edition of crypto-sdcard shall be used.

%prep
%setup -n %{name}-%{version}-%{release}

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/crypto-sdcard
cp -R systemd polkit-1 udev %{buildroot}%{_sysconfdir}/

%files
%defattr(-,root,root,-)
# Files which may be altered by user:
%config %{_sysconfdir}/systemd/system/cryptosd-plain@.service
# Regular files:
%{_sysconfdir}/systemd/system/cryptosd-luks@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-luks@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-plain@.service
%{_sysconfdir}/polkit-1/localauthority/50-local.d/69-cryptosd.pkla
%{_sysconfdir}/udev/rules.d/96-cryptosd.rules
# Extraordinary files / dirs:
%defattr(0640,root,root,0750)
%dir %{_sysconfdir}/crypto-sdcard

