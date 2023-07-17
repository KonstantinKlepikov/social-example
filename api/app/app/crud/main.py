from neo4j import GraphDatabase
from pprint import pprint
from app.config import settings


class BaseEngine:

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def clear(self):
        with self.driver.session() as session:
            session.execute_write(self._clear_data)
            session.execute_write(self._clear_schema)

    @staticmethod
    def _clear_data(tx):
        tx.run('MATCH (n) DETACH DELETE n;')

    @staticmethod
    def _clear_schema(tx):
        tx.run('CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *;')

    def query(self, q: str, param: dict[str, str] | None = None):

        with self.driver.session() as session:
            result = session.run(query=q, parameters=param)

            return result.data()


if __name__ == '__main__':

    connection = BaseEngine(
        settings.DATABASE_URL,
        'neo4j',
        settings.PASS.get_secret_value()
            )
    print('=====> Created driver')

    print(f'Driver agent: {connection.driver.get_server_info().agent}\n')

    query = connection.query(
        """
        CALL apoc.meta.stats()
        YIELD labels, relTypes, relTypesCount
        RETURN labels, relTypes, relTypesCount;
        """
    )

    pprint(query[0])

    query = connection.query(
        """
        MATCH (n) RETURN COUNT(n) AS count
        """
    )

    print(f'Count of nodes: {query[0]["count"]}')

    connection.close()
