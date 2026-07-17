from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from thun_deckbuilder.paths import DATABASE_FILE


class Database:
    def __init__(
        self,
        database_path: str | Path = DATABASE_FILE,
    ) -> None:
        self.database_path = Path(database_path)

    def exists(self) -> bool:
        return self.database_path.exists()

    def connect(
        self,
        *,
        readonly: bool = False,
    ) -> sqlite3.Connection:
        if readonly:
            if not self.database_path.exists():
                raise FileNotFoundError(
                    f"Datenbank nicht gefunden: {self.database_path}"
                )

            uri = f"file:{self.database_path.resolve().as_posix()}?mode=ro"

            connection = sqlite3.connect(
                uri,
                uri=True,
            )
        else:
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            connection = sqlite3.connect(self.database_path)

        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    @contextmanager
    def session(
        self,
        *,
        readonly: bool = False,
    ) -> Iterator[sqlite3.Connection]:
        connection = self.connect(readonly=readonly)

        try:
            yield connection

            if not readonly:
                connection.commit()

        except Exception:
            if not readonly:
                connection.rollback()
            raise

        finally:
            connection.close()

    def fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> dict[str, Any] | None:
        with self.session(readonly=True) as connection:
            row = connection.execute(
                query,
                parameters,
            ).fetchone()

        return dict(row) if row else None

    def fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        with self.session(readonly=True) as connection:
            rows = connection.execute(
                query,
                parameters,
            ).fetchall()

        return [dict(row) for row in rows]

    def scalar(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> Any:
        with self.session(readonly=True) as connection:
            row = connection.execute(
                query,
                parameters,
            ).fetchone()

        return row[0] if row else None