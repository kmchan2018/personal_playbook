
include ${HOME}/.config/firejail/firefox.inc

mkdir ~/.cache/mozilla/firefox/Work
mkdir ~/.mozilla/firefox/Work

whitelist ~/.cache/mozilla/firefox/Work
whitelist ~/.mozilla/firefox/Work

