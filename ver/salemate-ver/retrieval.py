"""Bộ truy xuất tài liệu (RAG nhẹ) cho prototype Salemate.

Dùng truy xuất từ vựng có chuẩn hóa dấu tiếng Việt — chạy được ngay,
không cần tải model embedding. Khi lên production có thể thay bằng
vector embeddings (multilingual-e5 / Vietnamese-SBERT) mà giữ nguyên interface.
"""
import os
import re
import glob
import math
import unicodedata


def strip_tones(s: str) -> str:
    """Bỏ dấu tiếng Việt + đ/Đ để khớp từ vựng bền hơn."""
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def normalize(s: str) -> str:
    return strip_tones(s).lower()


def tokenize(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize(s))


class Retriever:
    def __init__(self, knowledge_dir: str):
        self.chunks: list[dict] = []
        for path in sorted(glob.glob(os.path.join(knowledge_dir, "*.md"))):
            source = os.path.basename(path)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            approved = "r&d_approved: false" not in text.lower()
            # Cắt chunk theo từng mục (heading cấp 2-6)
            sections = re.split(r"(?m)^#{2,6}\s+", text)
            for sec in sections:
                sec = sec.strip()
                # Bỏ comment HTML và heading cấp 1
                sec = re.sub(r"<!--.*?-->", "", sec, flags=re.S).strip()
                sec = re.sub(r"(?m)^#\s+.*$", "", sec).strip()
                if len(sec) >= 40:
                    self.chunks.append(
                        {
                            "text": sec,
                            "source": source,
                            "approved": approved,
                            "tokens": set(tokenize(sec)),
                        }
                    )

        # IDF: ưu tiên từ hiếm/đặc trưng (vd "chiết khấu") hơn từ phổ biến.
        n_docs = max(1, len(self.chunks))
        self.idf: dict[str, float] = {}
        for ch in self.chunks:
            for tok in ch["tokens"]:
                self.idf[tok] = self.idf.get(tok, 0) + 1
        for tok, df in self.idf.items():
            self.idf[tok] = math.log(1 + n_docs / df)

    def search(self, query: str, k: int = 4, only_approved: bool = True) -> list[dict]:
        q_tokens = [t for t in tokenize(query) if len(t) > 1]
        scored = []
        for ch in self.chunks:
            if only_approved and not ch["approved"]:
                continue
            score = 0.0
            for t in q_tokens:
                w = self.idf.get(t, 1.0)
                if t in ch["tokens"]:
                    score += 2.0 * w
                elif len(t) >= 4 and any(tok.startswith(t) or t.startswith(tok) for tok in ch["tokens"]):
                    score += 0.4 * w
            if score > 0:
                scored.append((score, ch))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"noi_dung": c["text"], "nguon": c["source"]} for _, c in scored[:k]
        ]
