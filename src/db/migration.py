from logging import Logger
from os import listdir
from pathlib import Path

from psycopg import AsyncConnection

from dao import BaseAsyncDao


class Migration(BaseAsyncDao):
    """Apply database migration.

    Note:
    - Migration script should starts with "v" and ends with ".sql".
    - Scripts applied in alphabet order.
    - Applied scripts saved into the table "migration" and will not applied twice.
    """

    def __init__(self, connection: AsyncConnection, script_path: str, logger: Logger) -> None:
        super().__init__(connection)
        self._script_path = script_path
        self._logger = logger

    def _applied_scripts(self) -> list[str]:
        selection = self.sql(
            f"""
            SELECT script FROM migration
            """
        )
        applied_scripts = [row["script"] for row in selection]
        self._logger.debug(f"Found following records in database: {', '.join(applied_scripts)}")
        return applied_scripts

    def _create_table(self) -> None:
        self._logger.info("No 'version' table exists: create it")
        self.sql(
            """
            CREATE TABLE migration (
                script VARCHAR(64) NOT NULL,
                UNIQUE(script)
            )
            """
        )

    def _posix_path(self, script_name) -> str:
        return Path(self._script_path, script_name).as_posix()

    def _apply_script(self, script_name: str) -> None:
        with self.transaction():
            self._logger.info(f"Apply script '{script_name}'")

            self.sql_file(self._posix_path(script_name))
            self.sql(
                f"""
                INSERT INTO migration (script)
                VALUES ({self.name_ph(script_name)})
                """,
                {"script_name": script_name},
            )

    def migration(self) -> None:
        self._logger.info("Start migration...")

        applied_scripts = []
        if self.table_exists("migration"):
            applied_scripts = self._applied_scripts()
        else:
            self._create_table()

        self._logger.info(f"Checking deirectory '{self._script_path}'...")
        for fname in listdir(self._script_path):
            if not fname.endswith(".sql"):
                self._logger.debug(f"Skip file {fname}: name is not ended with '.sql'")
                continue

            if not fname.startswith("v"):
                self._logger.debug(f"Skip file {fname}: name is not started with 'v'")
                continue

            if fname in applied_scripts:
                self._logger.debug(f"Skip file {fname}: presented into the list applied scripts")
                continue

            self._apply_script(fname)

        self._logger.info("Migration done.")
