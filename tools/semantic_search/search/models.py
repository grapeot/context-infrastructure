from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Tuple
import numpy as np

@dataclass
class Chunk:
    id: str                    # "{source_file}:{chunk_index}"
    text: str                  # 分块文本内容
    embedding: Optional[np.ndarray] = None  # float32 向量
    source_file: str = ""       # 源文件相对路径
    header: str = ""           # 所属标题
    position: Tuple[int, int] = (0, 0)  # (start_line, end_line)
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self, include_embedding: bool = False) -> Dict[str, Any]:
        d = asdict(self)
        if not include_embedding:
            d.pop('embedding')
        return d

@dataclass
class SearchResult:
    chunk: Chunk
    score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": float(self.score),
            "chunk": self.chunk.to_dict()
        }
