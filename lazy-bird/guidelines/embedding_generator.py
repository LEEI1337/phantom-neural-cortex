"""
Dimensionality Hierarchy for Guidelines - Optimierung #3
=========================================================

Inspiriert von HRM's emergente Dimensionalitäts-Eigenschaft:
    H-Module: 89.95 PR (Participation Ratio) - hochdimensional
    L-Module: 30.22 PR - niedrigdimensional

Implementiert hierarchische Guideline-Embeddings:
    Layer 0-1 (Universal):  256D - kompakt, fundamental
    Layer 2-3 (Tactical):   512D - mittlere Abstraktion
    Layer 4-5 (Strategic):  1024D - hochdimensional, flexibel

Key Benefits:
- Bessere semantische Ähnlichkeitssuche
- Hierarchie spiegelt Abstraktionslevel
- Effiziente Guideline-Retrieval

"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from datetime import datetime


@dataclass
class GuidelineEmbedding:
    """Embedding für ein Guideline-Dokument."""

    layer: int  # 0-5
    file_path: str
    content: str
    embedding: np.ndarray  # 256D, 512D, or 1024D
    dimension: int  # 256, 512, 1024
    created_at: datetime
    metadata: Dict  # z.B. {'applies_to': ['claude', 'gemini'], 'category': 'security'}


class GuidelineEmbeddingGenerator:
    """
    Generiert hierarchische Embeddings für Guideline-Dokumente.

    Verwendet sentence-transformers für semantische Embeddings.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(__file__).parent / "embeddings_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Dimensionen pro Layer-Gruppe
        self.layer_dimensions = {
            0: 256, 1: 256,  # Universal/Foundation
            2: 512, 3: 512,  # Tactical/Execution
            4: 1024, 5: 1024  # Strategic/Meta
        }

        # Embeddings Cache
        self.embeddings: Dict[str, GuidelineEmbedding] = {}

        # Sentence Transformer Model (lazy load)
        self._model = None

    @property
    def model(self):
        """Lazy-loads sentence-transformers model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                # Verwende kompaktes Modell (all-MiniLM-L6-v2: 384D)
                self._model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Sentence-Transformers model loaded")
            except ImportError:
                print("sentence-transformers not installed.")
                print("Install with: pip install sentence-transformers")
                # Fallback auf simple bag-of-words
                self._model = "BOW_FALLBACK"

        return self._model

    def generate_embedding(
        self,
        layer: int,
        file_path: Path,
        content: str,
        metadata: Optional[Dict] = None
    ) -> GuidelineEmbedding:
        """
        Generiert Embedding für ein Guideline-Dokument.

        Args:
            layer: Layer-Nummer (0-5)
            file_path: Pfad zum Guideline-File
            content: Text-Inhalt
            metadata: Optionale Metadaten

        Returns:
            GuidelineEmbedding mit passender Dimensionalität
        """
        # Determine target dimension
        target_dim = self.layer_dimensions.get(layer, 512)

        # Generate base embedding
        if self.model == "BOW_FALLBACK":
            base_embedding = self._bow_embedding(content)
        else:
            # Sentence-Transformers generiert 384D
            base_embedding = self.model.encode(content, show_progress_bar=False)

        # Project to target dimensionality
        final_embedding = self._project_to_dimension(base_embedding, target_dim)

        # Create embedding object
        embedding_obj = GuidelineEmbedding(
            layer=layer,
            file_path=str(file_path),
            content=content,
            embedding=final_embedding,
            dimension=target_dim,
            created_at=datetime.now(),
            metadata=metadata or {}
        )

        # Cache
        cache_key = f"layer_{layer}_{file_path.name}"
        self.embeddings[cache_key] = embedding_obj

        # Persist to disk
        self._save_embedding(cache_key, embedding_obj)

        return embedding_obj

    def load_all_guidelines(self, guidelines_dir: Path) -> List[GuidelineEmbedding]:
        """
        Lädt und embeddet alle Guideline-Dokumente.

        Args:
            guidelines_dir: Directory mit LAYER-*.md Files

        Returns:
            Liste aller Guideline-Embeddings
        """
        all_embeddings = []

        # Finde alle LAYER-*.md Files
        layer_files = sorted(guidelines_dir.glob("LAYER-*.md"))

        for file_path in layer_files:
            # Extrahiere Layer-Nummer
            filename = file_path.stem  # "LAYER-0" oder "LAYER-2-CLAUDE"
            parts = filename.split('-')

            try:
                layer = int(parts[1])
            except (IndexError, ValueError):
                print(f"Skipping {file_path}: could not parse layer number")
                continue

            # Lese Content
            try:
                content = file_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            # Extrahiere Metadaten aus Filename
            metadata = {}
            if len(parts) > 2:
                # z.B. "LAYER-2-CLAUDE" → applies_to: claude
                agent = parts[2].lower()
                metadata['applies_to'] = [agent]

            # Check Cache
            cache_key = f"layer_{layer}_{file_path.name}"
            if cache_key in self.embeddings:
                all_embeddings.append(self.embeddings[cache_key])
                continue

            # Try load from disk cache
            cached = self._load_embedding(cache_key)
            if cached is not None:
                self.embeddings[cache_key] = cached
                all_embeddings.append(cached)
                continue

            # Generate new embedding
            print(f"Generating embedding for {file_path.name} (Layer {layer}, {self.layer_dimensions[layer]}D)...")
            embedding = self.generate_embedding(layer, file_path, content, metadata)
            all_embeddings.append(embedding)

        return all_embeddings

    def find_relevant_guidelines(
        self,
        query: str,
        layer: Optional[int] = None,
        top_k: int = 3,
        agent: Optional[str] = None
    ) -> List[Tuple[GuidelineEmbedding, float]]:
        """
        Findet relevanteste Guidelines für eine Query.

        Args:
            query: Suchtext (z.B. "security best practices")
            layer: Optional: Nur in diesem Layer suchen
            top_k: Anzahl Top-Ergebnisse
            agent: Optional: Filter nach Agent (claude, gemini, etc.)

        Returns:
            Liste von (GuidelineEmbedding, similarity_score) Tuples
        """
        if not self.embeddings:
            return []

        # Generate query embedding (nutze mittlere Dimension 512D)
        if self.model == "BOW_FALLBACK":
            query_embedding = self._bow_embedding(query)
        else:
            query_embedding = self.model.encode(query, show_progress_bar=False)

        # Berechne Similarities
        results = []

        for key, guideline in self.embeddings.items():
            # Filter
            if layer is not None and guideline.layer != layer:
                continue

            if agent is not None:
                applies_to = guideline.metadata.get('applies_to', [])
                if agent.lower() not in applies_to and len(applies_to) > 0:
                    continue

            # Project query to same dimension as guideline
            query_proj = self._project_to_dimension(query_embedding, guideline.dimension)

            # Cosine similarity
            similarity = self._cosine_similarity(query_proj, guideline.embedding)

            results.append((guideline, similarity))

        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def get_hierarchical_context(
        self,
        target_layer: int,
        agent: Optional[str] = None
    ) -> List[GuidelineEmbedding]:
        """
        Holt hierarchischen Kontext für einen Layer.

        Includes: Alle Layers <= target_layer (Vererbung)
                  Plus agent-spezifische Varianten

        Args:
            target_layer: Ziel-Layer (z.B. 4 für Lazy Bird)
            agent: Optional: Agent-spezifische Guidelines

        Returns:
            Sortierte Liste von Guidelines (Layer 0 → target_layer)
        """
        relevant = []

        for key, guideline in self.embeddings.items():
            # Include wenn Layer <= target
            if guideline.layer <= target_layer:
                # Prüfe Agent-Filter
                if agent is not None:
                    applies_to = guideline.metadata.get('applies_to', [])
                    # Include wenn: (1) generisch ODER (2) matcht Agent
                    if len(applies_to) == 0 or agent.lower() in applies_to:
                        relevant.append(guideline)
                else:
                    relevant.append(guideline)

        # Sortiere nach Layer (0 → target)
        relevant.sort(key=lambda g: (g.layer, g.file_path))

        return relevant

    def _project_to_dimension(
        self,
        embedding: np.ndarray,
        target_dim: int
    ) -> np.ndarray:
        """
        Projiziert Embedding auf Ziel-Dimensionalität.

        Methods:
        - target_dim < source_dim: PCA-ähnliche Reduktion (einfache Truncation)
        - target_dim > source_dim: Zero-Padding

        """
        source_dim = len(embedding)

        if source_dim == target_dim:
            return embedding

        if target_dim < source_dim:
            # Truncate (simple dimensionality reduction)
            # In production: Verwende echte PCA
            return embedding[:target_dim]
        else:
            # Pad with zeros
            padded = np.zeros(target_dim, dtype=np.float32)
            padded[:source_dim] = embedding
            return padded

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Berechnet Cosine Similarity zwischen zwei Vektoren."""
        # Normalisierung
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        vec1_norm = vec1 / norm1
        vec2_norm = vec2 / norm2

        # Dot product
        similarity = np.dot(vec1_norm, vec2_norm)

        return float(similarity)

    def _bow_embedding(self, text: str) -> np.ndarray:
        """
        Fallback: Simple Bag-of-Words Embedding.

        Nur verwendet wenn sentence-transformers nicht verfügbar.
        """
        # Einfache word frequency basierte Vektor (384D für Kompatibilität)
        words = text.lower().split()

        # Hash words zu 384 Bins
        embedding = np.zeros(384, dtype=np.float32)

        for word in words:
            # Simple hash
            word_hash = hash(word) % 384
            embedding[word_hash] += 1.0

        # Normalisierung
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding

    def _save_embedding(self, cache_key: str, embedding: GuidelineEmbedding):
        """Speichert Embedding zu Disk."""
        cache_file = self.cache_dir / f"{cache_key}.npz"

        # Separate numpy array und metadata
        metadata = {
            'layer': embedding.layer,
            'file_path': embedding.file_path,
            'dimension': embedding.dimension,
            'created_at': embedding.created_at.isoformat(),
            'metadata': embedding.metadata
        }

        # Save (numpy array komprimiert, metadata als JSON)
        np.savez_compressed(
            cache_file,
            embedding=embedding.embedding,
            metadata=np.array([json.dumps(metadata)], dtype=object)
        )

    def _load_embedding(self, cache_key: str) -> Optional[GuidelineEmbedding]:
        """Lädt Embedding von Disk."""
        cache_file = self.cache_dir / f"{cache_key}.npz"

        if not cache_file.exists():
            return None

        try:
            data = np.load(cache_file, allow_pickle=True)
            embedding_array = data['embedding']
            metadata_json = str(data['metadata'][0])
            metadata = json.loads(metadata_json)

            # Reconstruct GuidelineEmbedding
            # Content nicht gecacht (zu groß), wird bei Bedarf neu gelesen
            return GuidelineEmbedding(
                layer=metadata['layer'],
                file_path=metadata['file_path'],
                content="",  # Wird bei Bedarf neu geladen
                embedding=embedding_array,
                dimension=metadata['dimension'],
                created_at=datetime.fromisoformat(metadata['created_at']),
                metadata=metadata['metadata']
            )
        except Exception as e:
            print(f"Error loading cached embedding {cache_key}: {e}")
            return None

    def get_participation_ratio(self, embedding: np.ndarray) -> float:
        """
        Berechnet Participation Ratio (PR) für ein Embedding.

        PR misst die effektive Dimensionalität:
        - Hohe PR (z.B. 90): Viele Dimensionen aktiv genutzt
        - Niedrige PR (z.B. 30): Wenige Dimensionen dominant

        Formel: PR = (Σ λᵢ)² / Σ λᵢ²
        wobei λᵢ = Singular Values

        """
        # Normalisiere Embedding
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return 0.0

        normalized = embedding / norm

        # Berechne PR (vereinfachte Version ohne full SVD)
        # PR ≈ 1 / Σ(xᵢ⁴) für normalized vector
        squares = normalized ** 2
        fourth_powers = squares ** 2

        pr = 1.0 / (np.sum(fourth_powers) + 1e-10)  # Avoid division by zero

        return float(pr)

    def analyze_hierarchy_statistics(self) -> Dict[str, any]:
        """
        Analysiert Dimensionalitäts-Hierarchie.

        Überprüft ob höhere Layers tatsächlich höhere PR haben.
        """
        if not self.embeddings:
            return {}

        stats_by_layer = {}

        for key, guideline in self.embeddings.items():
            layer = guideline.layer

            if layer not in stats_by_layer:
                stats_by_layer[layer] = {
                    'count': 0,
                    'dimension': guideline.dimension,
                    'pr_values': []
                }

            pr = self.get_participation_ratio(guideline.embedding)
            stats_by_layer[layer]['count'] += 1
            stats_by_layer[layer]['pr_values'].append(pr)

        # Aggregate
        result = {}
        for layer, stats in sorted(stats_by_layer.items()):
            pr_values = stats['pr_values']
            result[f'layer_{layer}'] = {
                'count': stats['count'],
                'dimension': stats['dimension'],
                'avg_pr': np.mean(pr_values),
                'median_pr': np.median(pr_values),
                'min_pr': np.min(pr_values),
                'max_pr': np.max(pr_values)
            }

        return result


# Singleton Instance
_embedding_generator_instance = None


def get_embedding_generator() -> GuidelineEmbeddingGenerator:
    """Holt Singleton Embedding-Generator-Instanz."""
    global _embedding_generator_instance
    if _embedding_generator_instance is None:
        _embedding_generator_instance = GuidelineEmbeddingGenerator()
    return _embedding_generator_instance


# Export
__all__ = [
    'GuidelineEmbedding',
    'GuidelineEmbeddingGenerator',
    'get_embedding_generator'
]
