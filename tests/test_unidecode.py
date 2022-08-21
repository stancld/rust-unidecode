from fast_unidecode import unidecode
from unidecode import unidecode as py_unidecode


def test_py_unidecode_equivalence():
    valid_unicode = tuple(range(0x0, 0xD7FF + 1)) + tuple(range(0xE000, 0x10FFFF + 1))
    for _u in valid_unicode:
        u = hex(_u)
        assert unidecode(u) == py_unidecode(u)


def test_conversion():
    assert unidecode("Æneid") == "AEneid"
    assert unidecode("étude") == "etude"
    assert unidecode("北亰") == "Bei Jing "
    assert unidecode("ᔕᓇᓇ") == "shanana"
    assert unidecode("ᏔᎵᏆ") == "taliqua"
    assert unidecode("ܦܛܽܐܺ") == "ptu'i"
    assert unidecode("अभिजीत") == "abhijiit"
    assert unidecode("অভিজীত") == "abhijiit"
    assert unidecode("അഭിജീത") == "abhijiit"
    assert unidecode("മലയാലമ്") == "mlyaalm"
    assert unidecode("げんまい茶") == "genmaiCha "
