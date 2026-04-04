import yaml
import re
from typing import List, Dict, Any
from .models import Chunk

class MarkdownChunker:
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def parse_yaml_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """提取 YAML 元数据和正文。"""
        if content.startswith('---'):
            parts = re.split(r'^---', content, flags=re.MULTILINE)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    body = '---'.join(parts[2:]).strip()
                    return metadata or {}, body
                except yaml.YAMLError:
                    pass
        return {}, content.strip()

    def chunk(self, file_path: str, content: str) -> List[Chunk]:
        """按标题分块并保留元数据。"""
        metadata, body = self.parse_yaml_frontmatter(content)
        chunks = []

        # Calculate line offset: frontmatter lines + separator lines are skipped
        all_lines = content.split('\n')
        body_lines = body.split('\n')
        frontmatter_offset = len(all_lines) - len(body_lines)

        lines = body_lines
        current_header = ""
        current_chunk_lines = []
        chunk_idx = 0
        start_line = frontmatter_offset + 1

        for i, line in enumerate(lines, frontmatter_offset + 1):
            if line.startswith('#'):
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunks.append(Chunk(
                        id=f"{file_path}:{chunk_idx}",
                        text="\n".join(current_chunk_lines),
                        source_file=file_path,
                        header=current_header,
                        position=(start_line, i-1),
                        metadata=metadata
                    ))
                    chunk_idx += 1
                
                current_header = line
                current_chunk_lines = [line]
                start_line = i
            else:
                current_chunk_lines.append(line)
                
                # Split if chunk is too large
                if len("\n".join(current_chunk_lines)) > self.max_chunk_size:
                    chunks.append(Chunk(
                        id=f"{file_path}:{chunk_idx}",
                        text="\n".join(current_chunk_lines),
                        source_file=file_path,
                        header=current_header,
                        position=(start_line, i),
                        metadata=metadata
                    ))
                    chunk_idx += 1
                    # Start next chunk with header for context
                    current_chunk_lines = [current_header] if current_header else []
                    start_line = i

        # Final chunk
        if current_chunk_lines:
            chunks.append(Chunk(
                id=f"{file_path}:{chunk_idx}",
                text="\n".join(current_chunk_lines),
                source_file=file_path,
                header=current_header,
                position=(start_line, len(lines)),
                metadata=metadata
            ))
            
        return chunks
