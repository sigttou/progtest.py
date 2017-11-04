# progtest.py
Simple test script used to compare output of binary (valgrind and return code check included)

## Usage:
* Place your tests into the `tests/` directory
* Place your binary into the current directory
* Change `progtest.py` to your needs

## Example:
```
.
├── progtest.py
├── testbin
└── tests
    ├── simple1
    │   ├── in
    │   └── out
    ├── wo_valgrind
    │   ├── in
    │   ├── noval
    │   └── out
    └── w_ret_code
        ├── in
        ├── out
        └── ret
```
* There are 3 testcases (`simple1`, `wo_valgrind`, `w_ret_code`).
* If you don't want a test to be run with `valgrind` place a `noval` file into the test directory
* If your testcase returns with something different than 0 create a `ret` file inside the test directory, containing the return code

## Configure Options:
```
VAL_ERR = 111
VALGRIND_ARGS = '--leak-check=full --show-leak-kinds=all --track-origins=yes --quiet'
BINARY = sys.argv[1] if len(sys.argv) > 1 else "./testbin"
RESULTS_DIR = mkdtemp()
VALGRIND_CHECK = True
TIMEOUT = 10
```
* The **VAL_ERR** is used to find out if the error was returned by the program or `valgrind`.
* The **VALGRIND_ARGS** are written to provide good debugging information. Make sure your program was compiled with `-g`.
* The **BINARY** is taken from the command line arguments, if not provided *testbin* is used.
* The **RESULTS_DIR** is placed in `/tmp/` per default.
* The **VALGRIND_CHECK** is activated by default.
* The **TIMEOUT** is the maximum amount of seconds a testcase can run.
