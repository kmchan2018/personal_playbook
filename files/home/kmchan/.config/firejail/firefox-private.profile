
include ${HOME}/.config/firejail/firefox.inc

mkdir ~/.cache/mozilla/firefox/Private
mkdir ~/.mozilla/firefox/Private

whitelist ~/.cache/mozilla/firefox/Private
whitelist ~/.mozilla/firefox/Private

