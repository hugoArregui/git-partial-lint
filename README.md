#Git-partial-lint

[![Build Status](https://travis-ci.org/hugoArregui/git-partial-lint.png)](https://travis-ci.org/hugoArregui/git-partial-lint)

Run your preferred linter only on your current changes!

## Table of Contents

- [git-partial-lint](#)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Customization](#customization)
  - [Contributing](#contributing)
  - [License](#license)

<a name="requirements"></a>
##Requirements

The only requirement to run git-partial-lint is python 3.5+.

(Of course you'll also need git and your chosen linter :-D)

<a name="usage"></a>
##Usage

Example: `git-partial-lint.py eslint test.js`

```
usage: git-partial-lint.py [-h] [--format FORMAT] rule file [file ...]

run linter only on the repo current changes

positional arguments:
rule             rule name
file             file or wildcard

optional arguments:
-h, --help       show this help message and exit
--format FORMAT  format
```
<a name="customization"></a>
##Customization

git-partial-lint doesn't provide too much customization options, but it's
designed in a very modular way, so it should be pretty easy to you to write
your own main script, and make your changes from there.

<a name="contributing"></a>
##Contributing

Just send me a pull request! If you add a new rule please make sure to add
a test for it, so I don't have to install the linter you chose to use.

<a name="license"></a>
##License

This software is distributed under the "BSD 3-clause" license. See LICENSE for details.
