import pytest


def add_url(repo, url='http://example.com'):
    return repo.save({'url': url})


def add_check(repo, url_id, status_code=200, h1='H1', title='Title', description='Desc'):
    return repo.new_check(url_id, status_code, h1, title, description)


def test_create(repo):
    created, flag = add_url(repo)

    assert len(repo.get_content()) == 1
    assert created is not None
    assert 'id' in created
    assert created['name'] == 'http://example.com'
    assert created['created_at'] is not None
    assert flag is True


def test_create_unique(repo):
    add_url(repo)
    duble, flag = add_url(repo)

    assert len(repo.get_content()) == 1
    assert flag is False


def test_find(repo):
    created, _ = add_url(repo, 'http://google.com')
    found = repo.find(created['id'])

    assert created['name'] == found['name']
    assert created['id'] == found['id']


def test_find_return_none_for_wrong_id(repo):
    assert repo.find(999) is None


def test_find_name(repo):
    created1, _ = add_url(repo)
    created2, _ = add_url(repo, 'http://smthing.com')

    assert created1 == repo.find_name(created1['name'])
    assert created2 == repo.find_name(created2['name'])


def test_find_name_wrong_is_none(repo):
    assert repo.find_name('http://smthing.com') is None


def test_new_check(repo):
    saved, _ = add_url(repo)
    check_id = add_check(repo, saved['id'], 200, 'hello', 'from', 'outside')

    assert check_id is not None

    check = repo.get_checks_with_id(saved['id'])[0]

    assert check_id is not None
    assert check['h1'] == 'hello'
    assert check['title'] == 'from'
    assert check['description'] == 'outside'
    assert check['status_code'] == 200


def test_get_checks_with_id(repo):
    saved, _ = add_url(repo)
    check1 = add_check(repo, saved['id'], status_code=300)
    check2 = add_check(repo, saved['id'], status_code=200)
    checks = repo.get_checks_with_id(saved['id'])

    assert len(checks) == 2
    assert checks[0]['id'] == check1
    assert checks[1]['id'] == check2
    assert checks[0]['status_code'] == 300
    assert checks[1]['status_code'] == 200
