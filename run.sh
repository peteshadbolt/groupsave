#/bin/sh
export GROUPSAVER_SETTINGS=/home/pete/websites/groupsaver_settings.cfg
nosetests -s | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"
