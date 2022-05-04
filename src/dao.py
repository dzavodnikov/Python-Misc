from psycopg import AsyncConnection, AsyncCursor, AsyncTransaction


class BaseAsyncDao:
    """This class contains useful methods for database and table investigation."""

    async def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    def transaction(self) -> AsyncTransaction:
        return self._connection.transaction()

    def commit(self) -> AsyncTransaction:
        return self._connection.commit()

    def cursor(self) -> AsyncCursor:
        return self._connection.cursor()

    def _row_convert(self, cursor: AsyncCursor, row_tuple: tuple) -> dict:
        row_dict = {}
        if columns := cursor.description:
            for idx in range(len(columns)):
                col = columns[idx]
                val = row_tuple[idx]
                row_dict[col.name] = val
        return row_dict

    async def sql(self, sql: str, params: dict | None = None) -> list[dict]:
        """Execute SQL-script and return result in a list of dictionaries. Accept parameters as a
        dictionary."""
        key_str_params = {str(k): params[k] for k in params} if params else None

        async with self.cursor() as cursor:
            await cursor.execute(sql, key_str_params)
            if cursor.description:
                return [self._row_convert(cursor, row) for row in await cursor.fetchall()]
            else:
                return []

    async def sql_file(self, filepath: str, parameters: dict | None = None) -> list[dict] | None:
        """Execute SQL-script from provided file and return result in a list of dictionaries.
        Accept parameters as a dictionary."""
        with open(filepath, "r") as sql_script:
            return await self.sql(sql_script.read(), parameters)

    async def table_exists(self, table_name: str, table_schema: str = "public") -> bool:
        result = await self.sql(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = %(table_schema)s
                    AND table_name = %(table_name)s
            )
            """,
            {
                "table_schema": table_schema,
                "table_name": table_name,
            },
        )
        return result[0]["exists"]

    async def table_columns(self, table_name: str, table_schema: str = "public") -> list[str]:
        result = await self.sql(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            ;
            """,
            {
                "table_schema": table_schema,
                "table_name": table_name,
            },
        )
        return [r["column_name"] for r in result]

    async def database_size(self) -> str:
        result = await self.sql(
            """
            SELECT pg_size_pretty(
                pg_database_size(current_database())
            ) AS db_size
            """
        )
        return result[0]["db_size"]

    async def table_size(self, table_name: str, table_schema: str = "public") -> str:
        result = await self.sql(
            """
            SELECT pg_size_pretty(
                pg_total_relation_size(%(table)s)
            ) AS table_size
            """,
            {
                "table": f"{table_schema}.{table_name}",
            },
        )
        return result[0]["table_size"]

    async def table_list(self, table_schema: str = "public") -> list[str]:
        result = await self.sql(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            """,
            {
                "table_schema": table_schema,
            },
        )
        return [r["table_name"] for r in result]
