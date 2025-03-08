import pytest
from scenario_2.cli_module import display_menu


def test_display_menu(capsys):
    """
    test CLI menu display
    """
    display_menu()
    captured = capsys.readouterr()

    assert "Carpark Search System" in captured.out
    assert "1. Search by Carpark Number" in captured.out
    assert "2. Search by Address" in captured.out
    assert "3. Exit" in captured.out
