import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search.chunker import MarkdownChunker


@pytest.fixture
def chunker():
    return MarkdownChunker(max_chunk_size=200)


class TestParseYamlFrontmatter:
    def test_with_frontmatter(self, chunker):
        content = "---\ntitle: Test\ntags: [a, b]\n---\n# Hello\nBody text"
        metadata, body = chunker.parse_yaml_frontmatter(content)
        assert metadata == {"title": "Test", "tags": ["a", "b"]}
        assert body.startswith("# Hello")

    def test_without_frontmatter(self, chunker):
        content = "# Hello\nBody text"
        metadata, body = chunker.parse_yaml_frontmatter(content)
        assert metadata == {}
        assert body == content.strip()

    def test_invalid_yaml(self, chunker):
        content = "---\n: invalid: yaml: [[\n---\nBody"
        metadata, body = chunker.parse_yaml_frontmatter(content)
        assert metadata == {}


class TestChunking:
    def test_basic_header_split(self, chunker):
        content = "# Section 1\nText A\n# Section 2\nText B"
        chunks = chunker.chunk("test.md", content)
        assert len(chunks) == 2
        assert "Text A" in chunks[0].text
        assert "Text B" in chunks[1].text

    def test_chunk_ids_are_sequential(self, chunker):
        content = "# A\nfoo\n# B\nbar\n# C\nbaz"
        chunks = chunker.chunk("doc.md", content)
        assert [c.id for c in chunks] == ["doc.md:0", "doc.md:1", "doc.md:2"]

    def test_no_headers(self, chunker):
        content = "Just some plain text\nwith multiple lines."
        chunks = chunker.chunk("plain.md", content)
        assert len(chunks) == 1
        assert chunks[0].header == ""

    def test_large_chunk_is_split(self):
        chunker = MarkdownChunker(max_chunk_size=50)
        content = "# Header\n" + "word " * 100
        chunks = chunker.chunk("big.md", content)
        assert len(chunks) > 1
        for c in chunks:
            assert c.header == "# Header"

    def test_position_tracking(self, chunker):
        content = "# A\nline1\nline2\n# B\nline3"
        chunks = chunker.chunk("pos.md", content)
        assert chunks[0].position[0] == 1
        assert chunks[1].position[0] == 4

    def test_metadata_propagated(self, chunker):
        content = "---\nauthor: test\n---\n# A\nfoo\n# B\nbar"
        chunks = chunker.chunk("meta.md", content)
        for c in chunks:
            assert c.metadata == {"author": "test"}

    def test_empty_content(self, chunker):
        chunks = chunker.chunk("empty.md", "")
        assert len(chunks) == 0 or all(c.text.strip() == "" for c in chunks)
