from fast_unidecode import unidecode


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
