#!/bin/python

from subprocess import check_output, call

###### a rule

def run_linter(f):
    out = check_output(["rubocop", f], shell=True)
    return out.splitlines()

def error_linenum(error):
    pass

def format_error(error):
    pass

class GitInterface:

    def current_brach(self):
        return self._r(['rev-parse', '--abbrev-ref', 'HEAD'])

    def rev_parse(self, o):
        return self._r(['rev-parse', o])

    def blame_file(self, f, only_new_lines=True):
        lines = self._r(['blame', '-s', '--show-name', f]).splitlines()
        return {
            int(line.split()[2][:-1]): line 
            for line in lines 
            if not only_new_lines or line.startswith('00000000')}

    def _r(self, cmd):
        return check_output(['git'] + cmd).decode('utf-8').strip()


f = "test/unit/models/buyer_test.rb"
git = GitInterface()
current_brach = git.current_brach()
f_sha = git.rev_parse("{:s}:{:s}".format(current_brach, f))
blame = git.blame_file(f)

errors = 
for error in run_linter(f):
    linenum = error_linenum(error)

# function check_function() {
#   type $1 1>/dev/null 2>/dev/null
#   if [ ! $? -eq 0 ]; then
#     echo "Please provide a $1 function (see README)"
#     exit 1
#   fi
# }

# if [ $# -eq 0 ] || [ ! -f $1 ]; then
#   echo "Please provide a valid config file"
#   exit 1
# fi

# CONFIG_FILE=`realpath $1`
# source $CONFIG_FILE

# check_function run
# check_function print_output

# FILE=$2
# BASE_DIR="./.partial-lint"
# CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

# [ -d $BASE_DIR ] || mkdir -p $BASE_DIR || exit 1

# LINTER_OUTPUT=$BASE_DIR/checker_output
# run $FILE $LINTER_OUTPUT

# [ $? -eq 0 ] || exit 1

# SHA=`git rev-parse $CURRENT_BRANCH:$FILE 2>/dev/null`

# if [ $? -eq 0 ]; then
#   BLAME=$BASE_DIR/blame
#   git blame -s --show-name $FILE > $BLAME
#   while read line; do
#     extract_error_linenum $line
#     cat $BLAME | grep "^00000000" | awk -F\  '{print $3}' | grep "^$LINENUM)" > /dev/null
#     R=$?
#     if [ $R -eq 0 ]; then
#       print_output "$line"
#     elif [ $R -eq 2 ]; then #error
#       echo "ERROR in grep"
#     fi
#   done <$LINTER_OUTPUT
# else
#   while read line; do
#     print_output $line
#   done <$LINTER_OUTPUT
# fi

# rm -rf $BASE_DIR
