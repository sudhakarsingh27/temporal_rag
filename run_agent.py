import asyncio
import json
import logging
import os
import sys
import uuid
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import ipywidgets as widgets
from dotenv import load_dotenv
from IPython.display import Image, display
from typing_extensions import TypedDict


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

# Configure Graphiti
from graphiti_core import Graphiti
from graphiti_core.edges import EntityEdge
from graphiti_core.nodes import EpisodeType
from graphiti_core.utils.maintenance.graph_data_operations import clear_data
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.anthropic_client import AnthropicClient
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.llm_client.hf_client import HuggingFaceClient

def configure_graphiti(client = "openai"):
    neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
    neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')

    # create necessary clients
    if client == "openai":
        llm_client = None
    elif client == "openai-lambda":
        llm_client = OpenAIClient(
            config = LLMConfig(
                api_key = os.environ["LAMBDA_API_KEY"],
                base_url = "https://api.lambdalabs.com/v1",
                model="llama3.1-8b-instruct"
            )
        )
    elif client == "anthropic":
        llm_client = AnthropicClient(
            config = LLMConfig(
                api_key = os.environ["ANTHROPIC_API_KEY"]
            )
        )
    elif client == "huggingface":
        llm_client = HuggingFaceClient(
            config = LLMConfig(
                base_url = os.environ["HF_MODEL"],
                api_key = os.environ["HF_API_KEY"],

            )
        )

    client = Graphiti(
        neo4j_uri,
        neo4j_user,
        neo4j_password,
        llm_client=llm_client,
    )
    return client

async def ingest_products_data(client: Graphiti):

    # Note: This will clear the database
    await clear_data(client.driver)
    await client.build_indices_and_constraints()
    
    script_dir = Path.cwd().parent
    json_file_path = script_dir / 'graphiti/examples/data' / 'manybirds_products.json'

    with open(json_file_path) as file:
        products = json.load(file)['products']

    for i, product in enumerate(products):
        await client.add_episode(
            name=product.get('title', f'Product {i}'),
            episode_body=str({k: v for k, v in product.items() if k != 'images'}),
            source_description='ManyBirds products',
            source=EpisodeType.json,
            reference_time=datetime.now(timezone.utc),
        )

if __name__ ==  "__main__":
    load_dotenv()
    logger = setup_logging()
    
    os.environ['LANGCHAIN_TRACING_V2'] = 'false'
    os.environ['LANGCHAIN_PROJECT'] = 'Graphiti LangGraph Tutorial'

    client = configure_graphiti("huggingface")
    logger.warning("Graphiti configured!")

    asyncio.run(ingest_products_data(client))
    logger.warning("Ingesting done!")