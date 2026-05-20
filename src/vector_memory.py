from __future__ import annotations

import json
from pathlib import Path

from src.config import load_config

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.agent_state import AgentState


def get_vector_dir() -> Path:
    config = load_config()
    return Path(config["memory"]["vector_dir"])


def get_index_path() -> Path:
    return get_vector_dir() / "investigations.faiss"


def get_metadata_path() -> Path:
    return get_vector_dir() / "metadata.json"


def get_model_name() -> str:
    config = load_config()
    return config["memory"]["embedding_model"]


_model = None


def get_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(get_model_name())

    return _model


def state_to_text(state: AgentState) -> str:
    lines = []

    lines.append(f"User query: {state.user_query}")
    lines.append(f"Final answer: {state.final_answer}")

    for step in state.steps:
        lines.append(f"Thought: {step.thought}")

        if step.command:
            lines.append(f"Command: {step.command}")

        if step.observation:
            lines.append(f"Observation: {step.observation}")

    return "\n".join(lines)


def embed_text(text: str) -> np.ndarray:
    model = get_model()

    embedding = model.encode(
        [text],
        normalize_embeddings=True,
    )

    return np.array(embedding, dtype="float32")


def load_metadata() -> list[dict]:
    if not get_metadata_path().exists():
        return []

    return json.loads(get_metadata_path().read_text(encoding="utf-8"))


def save_metadata(metadata: list[dict]) -> None:
    get_vector_dir().mkdir(parents=True, exist_ok=True)
    get_metadata_path().write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


def load_or_create_index(dimension: int) -> faiss.Index:
    get_vector_dir().mkdir(parents=True, exist_ok=True)

    if get_index_path().exists():
        return faiss.read_index(str(get_index_path()))

    return faiss.IndexFlatIP(dimension)


def save_investigation_vector(state: AgentState, investigation_id: int) -> None:
    text = state_to_text(state)
    embedding = embed_text(text)

    dimension = embedding.shape[1]

    index = load_or_create_index(dimension)
    metadata = load_metadata()

    index.add(embedding)

    metadata.append(
        {
            "investigation_id": investigation_id,
            "user_query": state.user_query,
            "final_answer": state.final_answer,
            "text": text,
        }
    )
    faiss.write_index(index, str(get_index_path()))
    save_metadata(metadata)


def search_similar_vectors(query: str, limit: int = 3) -> list[dict]:
    if not get_index_path().exists() or not get_metadata_path().exists():
        return []

    metadata = load_metadata()

    if not metadata:
        return []

    query_embedding = embed_text(query)

    index = faiss.read_index(str(get_index_path()))

    scores, indices = index.search(query_embedding, limit)

    results = []

    for score, index_id in zip(scores[0], indices[0]):
        if index_id < 0 or index_id >= len(metadata):
            continue

        item = metadata[index_id].copy()
        item["score"] = float(score)
        results.append(item)

    return results