#!/bin/bash


echo ""
echo ""
echo " # AndroidRequestBackups test: dependencies"
echo " # #############################################################################"


CHECK_FAILED=false
check_depend() {

	local the_command
	the_command="$1"
	if hash "$the_command" 2>/dev/null; then
        echo " - (OK) dependency check .... $the_command exists."
    else
    	(>&2 echo " - (FAIL) dependency check ... $the_command was not found.")
        CHECK_FAILED=true
    fi
}

# ##################################################################
# CHECKS
# ##################################################################
check_depend ifconfig
check_depend ssh
check_depend sftp


# ##################################################################
# FINAL OUTPUT
# ##################################################################
if $CHECK_FAILED; then
	(>&2 echo " >>> (FAIL) Some dependencies are missing :'( .")
fi
echo " >>> (SUCCESS) All dependencies are installed."
