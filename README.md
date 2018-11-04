# crypto-sdcard ("sbj" edition)
Configuration files for unlocking and mounting encrypted SD-cards, using udev, udisks2, polkit and systemd.

This edition is provided specifically for devices (e.g. Jolla 1 phones aka "sbj"), which need Qualcomm's `qcrypto` kernel module to be loaded in order to support modern cryptographic schemes as e.g. XTS.  
For all other devices, the [generic edition](https://github.com/Olf0/crypto-sdcard) shall be used.

Extensively tested with systend 225 (which includes udev), udisks2 2.7.5 and polkit 0.104.<br />
RPM spec file is for SailfishOS 2.2, which provides aforementioned environment.<br />
RPMs built for SailfishOS are available at [OpenRepos](https://openrepos.net/content/olf/crypto-sdcard_sbj).

The necessary steps to prepare an SD-card (or any other removable storage) are described at [Together.Jolla.com](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/).<br />
Note that the "key"-files reside unencrypted on fixed, internal mass storage, as mobile devices usually have only a single user, who unlocks the whole device.<br />
Thus **crypto-sdcard** solely protects "data at rest" on SD-cards and other removable storage, i.e. specifically when the device is locked or switched off (and the SD-card may be taken out).

Features:
* These configuration files do not alter, replace or delete any extant files.
* Support of encrypted partitions and whole devices.
* Support for Cryptsetup LUKS and Cryptsetup "plain".
   * Note that SailfishOS (by providing Cryptsetup v1.x.y) supports only LUKSv1 headers.
   * Default parameters for Cryptsetup "plain" are "*-h sha1 -s 256 -c aes-xts-plain*".
* Start mounting encrypted (partitions on) SD-card via udisks at the earliest sensible time: Right after udisks2.service has started.
* Unmount before udisks2 begins stopping, hence achieving a clean unmount.
* Ensure, that AlienDalvik (specifically *alien-service-manager.service*) begins starting after mounting succeeded, to allow for [android_storage on SD-card](https://together.jolla.com/question/179060/how-to-externalising-android_storage-and-other-directories-files-to-sd-card/#179060-2-externalising-homenemoandroid_storage).  Even more importantly this also ensures, that unmounting occurs only after AlienDalvik is completely stopped.<br />
Nevertheless, these configuration files are also applicable to devices without AlienDalvik installed.
* Boot time is not significantly prolonged, as unlocking encrypted partitions per Cryptsetup occurs in parallel to starting udisks2; after both succeeded, all mount operations are also started concurrently.
* Create / try to rectify the "compatibility symlink" in order to allow older apps seamlessly accessing encrypted (partitions on) SD-cards at their new (since SailfishOS 2.2.0) mount point.

Version history:
* v0.4<br />
  Optimised configuration file names.<br />
  RPM spec file provided.
* v0.3<br />
  Switched to a UUID-based "key"-file naming scheme to allow for swapping encrypted SD-cards easily and moved "key"-files into a directory.<br /> 
  Hence the "key"-file format has changed again (please rename your "key"-files accordingly): 
    * For Cryptsetup LUKS: `/etc/crypto-sdcard/crypto_luks_<UUID>.key`
    * For Cryptsetup "plain": `/etc/crypto-sdcard/crypto_plain_<UUID>.key`
* v0.2<br />
  Fixed automatic mounting of DM-Crypt "plain" partitions.<br />
  "Key"-file format has changed (please rename your "key"-files accordingly):
    * For Cryptsetup LUKS: `/etc/crypto_luks_<device>.key`, e.g. */etc/crypto_luks_mmcblk1p2.key*
    * For Cryptsetup "plain": `/etc/crypto_plain_<device>.key`, e.g. */etc/crypto_plain_mmcblk1p2.key*
* v0.1<br />
  Initial check-in of the [last version at TJC](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/?answer=189813#post-id-189813).<br />
  "Key"-file format is `/etc/<device>.key`, e.g. */etc/mmcblk1p2.key*
