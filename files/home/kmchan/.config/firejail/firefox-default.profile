
include ${HOME}/.config/firejail/firefox.inc

mkdir ~/.cache/mozilla/firefox/Default
mkdir ~/.mozilla/firefox/Default

whitelist ~/.cache/mozilla/firefox/Default
whitelist ~/.mozilla/firefox/Default

