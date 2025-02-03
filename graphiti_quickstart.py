from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Initialize Graphiti
graphiti = Graphiti("bolt://localhost:7687", os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])

# Initialize the graph database with Graphiti's indices. This only needs to be done once.
graphiti.build_indices_and_constraints()

# Add episodes
episodes = [
    "Kamala Harris is the Attorney General of California. She was previously "
    "the district attorney for San Francisco.",
    "As AG, Harris was in office from January 3, 2011 – January 3, 2017",
]
for i, episode in enumerate(episodes):
    await graphiti.add_episode(
        name=f"Freakonomics Radio {i}",
        episode_body=episode,
        source=EpisodeType.text,
        source_description="podcast",
        reference_time=datetime.now(timezone.utc)
    )

# Search the graph
# Execute a hybrid search combining semantic similarity and BM25 retrieval
# Results are combined and reranked using Reciprocal Rank Fusion
results = await graphiti.search('Who was the California Attorney General?')
print(results)
[
    EntityEdge(
│   uuid = '3133258f738e487383f07b04e15d4ac0',
│   source_node_uuid = '2a85789b318d4e418050506879906e62',
│   target_node_uuid = 'baf7781f445945989d6e4f927f881556',
│   created_at = datetime.datetime(2024, 8, 26, 13, 13, 24, 861097),
│   name = 'HELD_POSITION',
# the fact reflects the updated state that Harris is
# no longer the AG of California
│   fact = 'Kamala Harris was the Attorney General of California',
│   fact_embedding = [
│   │   -0.009955154731869698,
│       ...
│   │   0.00784289836883545
│],
│   episodes = ['b43e98ad0a904088a76c67985caecc22'],
│   expired_at = datetime.datetime(2024, 8, 26, 20, 18, 1, 53812),
# These dates represent the date this edge was true.
│   valid_at = datetime.datetime(2011, 1, 3, 0, 0, tzinfo= < UTC >),
│   invalid_at = datetime.datetime(2017, 1, 3, 0, 0, tzinfo= < UTC >)
)
]

# Rerank search results based on graph distance
# Provide a node UUID to prioritize results closer to that node in the graph.
# Results are weighted by their proximity, with distant edges receiving lower scores.
results = await graphiti.search('Who was the California Attorney General?', center_node_uuid)
print(results)

# Close the connection
graphiti.close()