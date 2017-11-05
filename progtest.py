#!/usr/bin/env python3
"""
Copyright (c) 2015 - 2017, David Bidner <david -at- crap.solutions>

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted,
provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE
USE OR PERFORMANCE OF THIS SOFTWARE.
"""
# progtest.py - A simple tool used to apply I/O diffs on a given binary
# Further Information: https://crap.solutions/pages/progtest.html - https://github.com/sigttou/progtest

import sys
import os
import os.path
from subprocess import check_output, CalledProcessError
from difflib import unified_diff
from tempfile import mkdtemp

VAL_ERR = 111
VALGRIND_ARGS = '--leak-check=full --show-leak-kinds=all --track-origins=yes --quiet'
BINARY = sys.argv[1] if len(sys.argv) > 1 else "./testbin"
RESULTS_DIR = mkdtemp()
VALGRIND_CHECK = True
TIMEOUT = 10
TIMEOUT_ERR = 124

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NOCOL = '\033[0m'


def main():
    tests = [os.path.join('./tests/', o) for o in os.listdir('./tests/') if os.path.isdir(os.path.join('./tests/', o))]
    for test in tests:
        input = open(test + '/in') if os.path.isfile(test + '/in') else None
        exp_output = open(test + '/out').read() if os.path.isfile(test + '/out') else ''
        print('Running test: ' + os.path.basename(test))

        args = open(test + '/args').read() if os.path.isfile(test + '/args') else ''
        val_check = False if os.path.isfile(test + '/noval') else VALGRIND_CHECK
        exp_ret = int(open(test + '/ret').read()) if os.path.isfile(test + '/ret') else 0

        call = []
        call.append('timeout')
        call.append(str(TIMEOUT))
        if val_check:
            call.append('valgrind')
            call += VALGRIND_ARGS.split()
            val_logfile = RESULTS_DIR + '/' + os.path.basename(test) + '.val'
            call.append('--log-file={}'.format(val_logfile))
            call.append('--error-exitcode={}'.format(VAL_ERR))
        call.append(BINARY)
        call += args.split()

        fail = False
        try:
            out = check_output(call, stdin=input).decode()
        except CalledProcessError as grepexc:
            out = grepexc.output.decode()
            fail = True
            if grepexc.returncode == exp_ret:
                fail = False
                break
            elif grepexc.returncode == VAL_ERR:
                print('    Valgrind error: {}'.format(val_logfile))
            elif grepexc.returncode == TIMEOUT_ERR:
                print('    Test timed out!')
            else:
                print('    Test had the Wrong return value: {} should be: {}'.format(grepexc.returncode, exp_ret))

        diff = list(unified_diff(exp_output.splitlines(1), out.splitlines(1), fromfile='exp_output', tofile='output'))
        if(diff):
            difffile = open(RESULTS_DIR + '/' + os.path.basename(test) + '.diff', 'w+')
            difffile.writelines(diff)
            print('    Output does not match: {}'.format(difffile.name))
            fail = True
        if(fail):
            outfile = open(RESULTS_DIR + '/' + os.path.basename(test) + '.out', 'w+')
            outfile.write(out)
            print(RED + 'FAIL' + NOCOL + ': {}'.format(outfile.name))
        else:
            print(GREEN + 'OK' + NOCOL)


if __name__ == '__main__':
    main()
