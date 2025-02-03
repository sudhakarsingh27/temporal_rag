from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(
        os.environ["NEO4J_USER"],
        os.environ["NEO4J_PASSWORD"]
    )
)

with driver.session() as session:
    result = session.run("RETURN 'Neo4j is working!' AS message")
    print(result.single()["message"])  # Output: "Neo4j is working!"
