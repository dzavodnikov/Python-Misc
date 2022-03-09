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

    def cursor(self) -> AsyncCursor:
        return self._connection.cursor()

    async def sql(self, sql: str, parameters: dict | None = None) -> list[dict]:
        """Execute SQL-script and return result in a list of dictionaries. Accept parameters as a
        dictionary."""
        async with self.cursor() as cursor:
            await cursor.execute(sql, parameters)

            if cursor.description:
                resp_t_t = await cursor.fetchall()
                resp_l_d = []
                for row in resp_t_t:
                    d = {}
                    for idx in range(len(cursor.description)):
                        col = cursor.description[idx]
                        val = row[idx]
                        d[col.name] = val
                    resp_l_d.append(d)
                return resp_l_d
            else:
                return []

    async def sql_file(self, filepath: str, parameters: dict | None = None) -> list[dict] | None:
        """Execute SQL-script from provided file and return result in a list of dictionaries.
        Accept parameters as a dictionary."""
        with open(filepath, "r") as sql_script:
            return await self.sql(sql_script.read(), parameters)

    async def table_exists(self, table_name: str) -> bool:
        result = await self.sql(
            f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE CONCAT(table_schema, '.', table_name) LIKE '%%{table_name}'
            )
            """
        )
        return result[0]["exists"]

    def _string_validate(self, names: any) -> None:
        if not len(names):
            raise BaseException(f"Expect at least one string parameters")
        for n in names:
            if not isinstance(n, str):
                raise BaseException(f"Expect string parameters, but got '{n.__class__.__name__}'")

    def list_ph(self, *names: list[str]) -> str:
        """Create name placeholder: `name` splitted by comma."""
        self._string_validate(names)
        return f"{', '.join(names)}"

    def name_ph(self, *names: list[str]) -> str:
        """Create name placeholder: `%(name)s` splitted by comma."""
        self._string_validate(names)
        return self.list_ph(*[f"%({n})s" for n in names])

    def name_pair_ph(self, *names: list[str]) -> str:
        """Create list of pairs: `name = %(name)s` splitted by comma."""
        self._string_validate(names)
        return self.list_ph(*[f"{n} = {self.name_ph(n)}" for n in names])
