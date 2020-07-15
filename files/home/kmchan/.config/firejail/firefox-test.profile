
include ${HOME}/.config/firejail/firefox.inc

mkdir ~/.cache/mozilla/firefox/Test
mkdir ~/.mozilla/firefox/Test
mkdir ~/Projects

whitelist ~/.cache/mozilla/firefox/Test
whitelist ~/.mozilla/firefox/Test
whitelist ~/Projects

