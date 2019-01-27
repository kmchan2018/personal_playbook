
##########################################################################
#
# Firejail profile for Mozilla Firefox
#

# Prevents blacklisting of the following files
noblacklist ${HOME}/.mozilla
noblacklist ${HOME}/.cache/mozilla

# Includes default rules
include /etc/firejail/disable-common.inc
include /etc/firejail/disable-programs.inc
include /etc/firejail/disable-devel.inc
include /etc/firejail/disable-passwdmgr.inc
include /etc/firejail/whitelist-common.inc

# Ensure existence of essential files
mkdir ${HOME}/.mozilla
mkdir ${HOME}/.mozilla/extensions
mkdir ${HOME}/.mozilla/firefox
mkdir ${HOME}/.mozilla/firefox/Crash Reports

# Allows mozilla files
whitelist ${DOWNLOADS}
whitelist ${HOME}/.mozilla
whitelist ${HOME}/.mozilla/extensions
whitelist ${HOME}/.mozilla/firefox
whitelist ${HOME}/.mozilla/firefox/profiles.ini
whitelist ${HOME}/.mozilla/firefox/Crash Reports
whitelist ${HOME}/.cache/mozilla

# Allows extension files
whitelist ${HOME}/dwhelper
whitelist ${HOME}/.zotero
whitelist ${HOME}/.vimperatorrc
whitelist ${HOME}/.vimperator
whitelist ${HOME}/.pentadactylrc
whitelist ${HOME}/.pentadactyl
whitelist ${HOME}/.keysnail.js
whitelist ${HOME}/.config/gnome-mplayer
whitelist ${HOME}/.cache/gnome-mplayer/plugin
whitelist ${HOME}/.dbus/session-bus
whitelist ${HOME}/.pki
whitelist ${HOME}/.wine-pipelight
whitelist ${HOME}/.wine-pipelight64
whitelist ${HOME}/.config/pipelight-widevine
whitelist ${HOME}/.config/pipelight-silverlight5.1

# Allows xpra files
read-only ${HOME}/.xpra
whitelist ${HOME}/.xpra

# Allows fcitx files
read-only ${HOME}/.config/fcitx
read-only ${HOME}/Software/firejail
whitelist ${HOME}/.config/fcitx
whitelist ${HOME}/Software/firejail

# Mocks temporary directory
#private-tmp

# Sanitizes capabilities
caps.drop all

# Sanitizes networks
netfilter

# Sanitizes syscalls
#seccomp
protocol unix,inet,inet6,netlink

# Sanitizes users
noroot

# Configures execution environment
nonewprivs

