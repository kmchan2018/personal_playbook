
##########################################################################
#
# Firejail profile for Steam
#

# Prevents blacklisting of the following files
noblacklist ${HOME}/.java
noblacklist ${HOME}/.killingfloor
noblacklist ${HOME}/.local/share/3909/PapersPlease
noblacklist ${HOME}/.local/share/aspyr-media
noblacklist ${HOME}/.local/share/cdprojektred
noblacklist ${HOME}/.local/share/feral-interactive
noblacklist ${HOME}/.local/share/Steam
noblacklist ${HOME}/.local/share/SuperHexagon
noblacklist ${HOME}/.local/share/Terraria
noblacklist ${HOME}/.local/share/vpltd
noblacklist ${HOME}/.local/share/vulkan
noblacklist ${HOME}/.steam
noblacklist ${HOME}/.steampath
noblacklist ${HOME}/.steampid
noblacklist /sbin
noblacklist /usr/sbin
noblacklist /usr/lib/llvm*

# Includes default rules
include /etc/firejail/disable-common.inc
include /etc/firejail/disable-programs.inc
include /etc/firejail/disable-devel.inc
include /etc/firejail/disable-passwdmgr.inc
include /etc/firejail/whitelist-common.inc
include /etc/firejail/whitelist-var-common.inc

# Ensure existence of essential files
mkdir ${HOME}/.java
mkdir ${HOME}/.local/share/Steam
mkdir ${HOME}/.local/share/vulkan
mkdir ${HOME}/.steam
mkdir ${HOME}/.steampath

# Whitelist steam files
whitelist ${HOME}/.java
whitelist ${HOME}/.steam
whitelist ${HOME}/.steampath
whitelist ${HOME}/.steampid
whitelist ${HOME}/.local/share/Steam
whitelist ${HOME}/.local/share/vulkan

# Allows game files for Unity games
mkdir ${HOME}/.config/unity3d
whitelist ${HOME}/.config/unity3d

# Allows game files for "Killing Floor" (http://store.steampowered.com/app/1250/Killing_Floor/)
# mkdir ${HOME}/.killingfloor
# whitelist ${HOME}/.killingfloor

# Allows game files for "Papers, Please" (http://store.steampowered.com/app/239030/Papers_Please/)
# mkdir ${HOME}/.local/share/3909/PapersPlease
# whitelist ${HOME}/.local/share/3909/PapersPlease

# Allows game files for "Super Hexagon" (http://store.steampowered.com/app/221640/Super_Hexagon/)
# mkdir ${HOME}/.local/share/SuperHexagon
# whitelist ${HOME}/.local/share/SuperHexagon

# Allows game files for "Terraria" (http://store.steampowered.com/app/105600/Terraria/)
# mkdir ${HOME}/.local/share/Terraria
# whitelist ${HOME}/.local/share/Terraria

# Allows game files for Aspyr Media titles (http://www.aspyr.com/)
# mkdir ${HOME}/.local/share/aspyr-media
# whitelist ${HOME}/.local/share/aspyr-media

# Allows game files for CD Projekt Red titles (http://en.cdprojektred.com/)
# mkdir ${HOME}/.local/share/cdprojektred
# whitelist ${HOME}/.local/share/cdprojektred

# Allows game files for Feral Interactive titles (http://www.feralinteractive.com/en/)
# mkdir ${HOME}/.local/share/feral-interactive
# whitelist ${HOME}/.local/share/feral-interactive

# Allows game files for Virtual Programming titles (https://www.vpltd.com/)
# mkdir ${HOME}/.local/share/vpltd
# whitelist ${HOME}/.local/share/vpltd

# Allows game files for Creeper World 3
mkdir ${HOME}/.config/creeperworld3
whitelist ${HOME}/.config/creeperworld3

# Allows game files for 7 Days to Die
mkdir ${HOME}/.local/share/7DaysToDie
whitelist ${HOME}/.local/share/7DaysToDie

# Allows game files for Paradox launcher
mkdir ${HOME}/.paradoxlauncher
mkdir ${HOME}/.local/share/Paradox Interactive
whitelist ${HOME}/.paradoxlauncher
whitelist ${HOME}/.local/share/Paradox Interactive

# Allows xpra files
read-only ${HOME}/.xpra
whitelist ${HOME}/.xpra

# Allows fcitx files
read-only ${HOME}/.config/fcitx
read-only ${HOME}/Software/firejail
whitelist ${HOME}/.config/fcitx
whitelist ${HOME}/Software/firejail

# Mocks temporary directory
private-tmp

# Sanitizes capabilities
caps.drop all

# Sanitizes devices
nodvd
notv

# Sanitizes networks
netfilter

# Sanitizes syscalls
protocol unix,inet,inet6,netlink

# Sanitizes users
noroot
nogroups

# Configures execution environment
nonewprivs
shell none

