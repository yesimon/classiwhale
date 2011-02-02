#!/bin/sh

#set -x

test_dir=$(cd $(dirname $0) && pwd)

export WORKON_HOME="$(echo ${TMPDIR:-/tmp}/WORKON_HOME | sed 's|//|/|g')"

oneTimeSetUp() {
    rm -rf "$WORKON_HOME"
    mkdir -p "$WORKON_HOME"
    source "$test_dir/../virtualenvwrapper.sh"
}

oneTimeTearDown() {
    rm -rf "$WORKON_HOME"
}

setUp () {
    echo
    rm -f "$test_dir/catch_output"
}

test_remove () {
    mkvirtualenv "deleteme"
    assertTrue "[ -d $WORKON_HOME/deleteme ]"
    deactivate
    rmvirtualenv "deleteme"
    assertFalse "[ -d $WORKON_HOME/deleteme ]"
}

test_rm_aliased () {
    mkvirtualenv "deleteme"
    deactivate
    alias rm='rm -i'
    set -x
    rmvirtualenv "deleteme"
    set +x
    unalias rm
}

test_no_such_env () {
    assertFalse "[ -d $WORKON_HOME/deleteme ]"
    assertTrue "rmvirtualenv deleteme"
}

test_no_workon_home () {
    old_home="$WORKON_HOME"
    export WORKON_HOME="$WORKON_HOME/not_there"
    output=`rmvirtualenv should_not_be_created 2>&1`
    assertTrue "Did not see expected message" "echo $output | grep 'does not exist'"
    WORKON_HOME="$old_home"
}


. "$test_dir/shunit2"
