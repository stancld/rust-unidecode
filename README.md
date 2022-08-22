# Python Fast Unidecode

<div align="center">

[![Build](https://github.com/stancld/rust-unidecode/actions/workflows/ci_install-pkg.yml/badge.svg?branch=master&event=push)](https://github.com/stancld/rust-unidecode/actions/workflows/ci_install-pkg.yml)
[![Python version](https://img.shields.io/badge/python-3.8%7C3.9%7C3.10-blue)](https://img.shields.io/badge/python-3.8%7C3.9%7C3.10-blue)
[![Rust tests](https://github.com/stancld/rust-unidecode/actions/workflows/ci_test.yml/badge.svg?branch=master&event=push)](https://github.com/stancld/rust-unidecode/actions/workflows/ci_test.yml)
[![Python tests](https://github.com/stancld/rust-unidecode/actions/workflows/ci_python-test.yml/badge.svg?branch=master&event=push)](https://github.com/stancld/rust-unidecode/actions/workflows/ci_python-test.yml)
[![License](https://img.shields.io/crates/l/unidecode.svg?style=flat-square)](https://github.com/stancld/rust-unidecode/blob/master/LICENSE)

______________________________________________________________________
</div>



This repo is a fork of the [`rust-unicode`](https://github.com/chowdhurya/rust-unidecode)
repository and transports the original Rust implementation to be used with Python.
It also implements a couple of source code changes to hasten a translation of
ASCII family of characters and makes this implementation on par with [Python unidecode
implementation](https://github.com/avian2/unidecode) on this set of characters.

The overall result is this package should provide you with the same output
as the aforementioned Python implementation, but is much faster on a translation of
non-ASCII characters (>4x) and slightly faster on ASCII characters (in a degree of several percents) on average based on
the [test_speedup.py](./test_speedup.py) benchmark (depending on caching, etc.; sometimes, a translation of
non-ASCII characters provides you with a speedup of up to 100x).

## Installation

```bash
pip install fast_unidecode
```

<details>
  <summary> Installation from source </summary>

First, you need to build the package using [`maturin`](https://github.com/PyO3/maturin),
then install `fast_unidecode` simply with `pip`.

```bash
maturin build --release
pip install target/wheels/fast_unidecode...
```
</details>

## Usage

```python
>>> from fast_unidecode import unidecode

>>> print(unidecode("Æneid"))
'AEneid'

>>> print(unidecode("北亰"))
'Bei Jing'
```


<details>
  <summary> rust-unidecode (Original README.md) </summary>

[Documentation](https://docs.rs/unidecode/)

The `rust-unidecode` library is a Rust port of Sean M. Burke's famous
[`Text::Unidecode`](http://search.cpan.org/~sburke/Text-Unidecode-1.23/lib/Text/Unidecode.pm)
module for Perl. It transliterates Unicode strings such as "Æneid" into pure
ASCII ones such as "AEneid." For a detailed explanation on the rationale behind
using such a library, you can refer to both the documentation of the original
module and
[this article](http://interglacial.com/~sburke/tpj/as_html/tpj22.html) written
by Burke in 2001.

The data set used to translate the Unicode was ported directly from the
`Text::Unidecode` module using a Perl script, so `rust-unidecode` should produce
identical output.

Examples
--------
```rust
extern crate unidecode;
use unidecode::unidecode;

assert_eq!(unidecode("Æneid"), "AEneid");
assert_eq!(unidecode("étude"), "etude");
assert_eq!(unidecode("北亰"), "Bei Jing");
assert_eq!(unidecode("ᔕᓇᓇ"), "shanana");
assert_eq!(unidecode("げんまい茶"), "genmaiCha ");
```

Guarantees and Warnings
-----------------------
Here are some guarantees you have when calling `unidecode()`:
  * The `String` returned will be valid ASCII; the decimal representation of
    every `char` in the string will be between 0 and 127, inclusive.
  * Every ASCII character (0x0000 - 0x007F) is mapped to itself.
  * All Unicode characters will translate to a string containing newlines
    (`"\n"`) or ASCII characters in the range 0x0020 - 0x007E. So for example,
    no Unicode character will translate to `\u{01}`. The exception is if the
    ASCII character itself is passed in, in which case it will be mapped to
    itself. (So `'\u{01}'` will be mapped to `"\u{01}"`.)

There are, however, some things you should keep in mind:
  * As stated, some transliterations do produce `\n` characters.
  * Some Unicode characters transliterate to an empty string, either on purpose
    or because `rust-unidecode` does not know about the character.
  * Some Unicode characters are unknown and transliterate to `"[?]"`.
  * Many Unicode characters transliterate to multi-character strings. For
    example, 北 is transliterated as "Bei ".

This information was paraphrased from the original `Text::Unidecode`
documentation.

</details>
