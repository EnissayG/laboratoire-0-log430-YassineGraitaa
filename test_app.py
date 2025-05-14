from app import greet


def test_greet_empty_output(capfd):
    greet("")
    out, err = capfd.readouterr()
    assert out.strip() == "Hello, !"


def test_greet_output(capfd):
    greet("Yassine")
    out, err = capfd.readouterr()
    assert out.strip() == "Hello, Yassine!"
