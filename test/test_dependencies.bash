#!/bin/bash
#
# test/test_dependencies.bash
#
# it checks whether the required dependencies are installed or not.
#

echo ""
echo ""
echo " # AndroidRequestBackups test: dependencies"
echo " # #############################################################################"


CHECK_FAILED=false
check_depend() {

	local the_command
	the_command="$1"
	if hash "$the_command" 2>/dev/null; then
        echo " - (OK) dependency check .... '$the_command' exists."
    else
    	(>&2 echo " - (FAIL) dependency check ... '$the_command' was not found.")
        CHECK_FAILED=true
    fi
}

# ##################################################################
# CHECKS
# ##################################################################
check_depend /sbin/ifconfig
check_depend ssh
check_depend sftp
check_depend tar
check_depend find
check_depend uname
check_depend date
check_depend psql
check_depend pg_dump


# ##################################################################
# FINAL OUTPUT
# ##################################################################
if $CHECK_FAILED; then
	(>&2 echo " >>> (FAIL) Some dependencies are missing :'( .")
fi
echo " >>> (SUCCESS) All dependencies are installed."
