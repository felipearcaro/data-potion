import snowflake.connector


class SnowflakeClient:

    METADATA_QUERY = """
select db.database_name, db.comment, sc.schema_name, sc.comment, tb.table_name, tb.comment, co.column_name, co.comment, co.data_type
from {db_name}.information_schema.databases db 
INNER join {db_name}.information_schema.schemata sc on db.database_name = sc.catalog_name
INNER join {db_name}.information_schema.tables tb on sc.schema_name = tb.table_schema and db.database_name = tb.table_catalog
INNER join {db_name}.information_schema.columns co on tb.table_name = co.table_name and sc.schema_name = co.table_schema and db.database_name = co.table_catalog
where database_name = '{db_name}' 
and sc.schema_name NOT IN ('PUBLIC','INFORMATION_SCHEMA') AND tb.table_schema NOT IN ('PUBLIC','INFORMATION_SCHEMA') and co.table_schema NOT IN ('PUBLIC','INFORMATION_SCHEMA');
"""

    def __init__(self, user, account, password, role, warehouse, database):
        self.user = user
        self.account = account
        self.password = password
        self.role = role
        self.warehouse = warehouse
        self.database = database

    def __connect(self):
        conn = snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            role=self.role,
            warehouse=self.warehouse
        )
        return conn.cursor()

    def execute_query(self, query):
        with self.__connect() as cursor:
            cursor.execute(f'USE DATABASE {self.database}')
            cursor.execute(query)
            df = cursor.fetch_pandas_all()
            return df

    def get_metadata(self):
        metadata = SnowflakeClient.METADATA_QUERY.format(
            db_name=self.database)
        return self.execute_query(metadata)
