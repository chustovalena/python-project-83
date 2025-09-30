from page_analyzer.validate import validate


def test_validate_overlength():
    url = {'url': 'http://tklpxxpuevvrylfjebbzzjozaemkqilhlhmubscxyennntwqewnwcrwjkupxjsgtpowehieaxsexhfycnfxfzpjaybubclolxucvodfuliqtnuebqmqiwuueggqmegrfodzszpypaszqnzbeabecimzwamhtotdyqekerclccsnmmpxrkbrhbtcqurzkfilifolgmnsxothlqpvugaiewomhpbwgfeqlwrzmrneujukksvljppwefkyljcceutbfgewa.com'}
    errors = validate(url)

    assert "Url length must be less than 256 characters" in errors


def test_validate_got_scheme():
    url = {'url': 'wekgerg.com'}
    errors = validate(url)

    assert "URL must start with http:// or https://" in errors


def test_validate_hostname():
    url1 = {'url': 'http://wekgergcom'}
    url2 = {'url': 'http://'}
    errors_existhost = validate(url1)
    errors_existdot = validate(url2)

    assert "Incorrect URL" in errors_existdot
    assert "Incorrect URL" in errors_existhost


def test_validate_with_at_in_url():
    url = {'url': 'http://ththeheh@rt'}
    errors = validate(url)
    assert "Incorrect URL" in errors
