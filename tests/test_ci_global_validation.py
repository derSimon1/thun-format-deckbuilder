import sqlite3
from contextlib import closing

from scripts.ci_global_validation import _database_usable


def test_database_health_check_releases_file_before_replacement(tmp_path) -> None:
    database = tmp_path / "cards.db"
    replacement = tmp_path / "replacement.db"
    with closing(sqlite3.connect(database)) as connection:
        connection.executescript(
            "CREATE TABLE cards (id INTEGER);"
            "CREATE TABLE prints (id INTEGER);"
        )
        connection.executemany(
            "INSERT INTO cards VALUES (?)",
            ((value,) for value in range(1001)),
        )
        connection.executemany(
            "INSERT INTO prints VALUES (?)",
            ((value,) for value in range(1001)),
        )
        connection.commit()
    replacement.write_bytes(database.read_bytes())

    assert _database_usable(database)
    replacement.replace(database)

    assert database.is_file()
    assert not replacement.exists()
