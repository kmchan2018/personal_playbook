
##########################################################################
#
# Firejail profile for Mozilla Firefox
#

# Prevents blacklisting of the following files
noblacklist ${HOME}/.cache/baidunetdisk
noblacklist ${HOME}/.config/baidunetdisk

# Includes default rules
include /etc/firejail/disable-common.inc
include /etc/firejail/disable-programs.inc
include /etc/firejail/disable-devel.inc
include /etc/firejail/disable-passwdmgr.inc
include /etc/firejail/whitelist-common.inc

# Ensure existence of essential files
mkdir ${HOME}/.cache/baidunetdisk
mkdir ${HOME}/.config/baidunetdisk

# Allows mozilla files
whitelist ${HOME}/.cache/baidunetdisk
whitelist ${HOME}/.config/baidunetdisk
whitelist ${DOWNLOADS}

# Allows xpra files
read-only ${HOME}/.xpra
whitelist ${HOME}/.xpra

# Allows fcitx files
read-only ${HOME}/.config/fcitx
read-only ${HOME}/Software/firejail
whitelist ${HOME}/.config/fcitx
whitelist ${HOME}/Software/firejail

# Sanitizes capabilities
caps.drop all

# Sanitizes networks
netfilter

# Sanitizes syscalls
protocol unix,inet,inet6,netlink

# Sanitizes users
noroot

# Configures execution environment
nonewprivs

