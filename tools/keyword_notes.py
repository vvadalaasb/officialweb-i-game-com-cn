from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SUMMARY_WEBSITE = "https://officialweb-i-game.com.cn"
TAG_CORE = "爱游戏"


@dataclass
class KeywordNote:
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    source_url: Optional[str] = None
    note_level: int = 0
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags.copy(),
            "source_url": self.source_url,
            "note_level": self.note_level,
            "created_at": self.created_at,
        }


def format_note_single(note: KeywordNote, prefix: str = "•") -> str:
    lines = [
        f"{prefix} 【{note.title}】",
        f"  内容: {note.content}",
        f"  标签: {', '.join(note.tags) if note.tags else '无'}",
    ]
    if note.source_url:
        lines.append(f"  来源: {note.source_url}")
    lines.append(f"  等级: {note.note_level} (创建于 {note.created_at})")
    return "\n".join(lines)


def format_note_list(notes: List[KeywordNote], separator: str = "-" * 40) -> str:
    parts = []
    for idx, note in enumerate(notes, 1):
        header = f"笔记 #{idx}"
        body = format_note_single(note, prefix=">")
        parts.append(f"{header}\n{body}")
    return f"\n{separator}\n".join(parts)


def build_demo_notes() -> List[KeywordNote]:
    note1 = KeywordNote(
        title="游戏内容实录",
        content="记录爱游戏平台的核心玩法与交互反馈。",
        tags=[TAG_CORE, "玩法", "评测"],
        source_url=SUMMARY_WEBSITE,
        note_level=2,
    )
    note2 = KeywordNote(
        title="社区动态观察",
        content="用户对爱游戏近期的活动反响积极。",
        tags=[TAG_CORE, "社区", "活动"],
        note_level=1,
    )
    note3 = KeywordNote(
        title="技术架构笔记",
        content="爱游戏后端基于微服务，接口响应稳定。",
        tags=[TAG_CORE, "技术", "架构"],
        source_url=SUMMARY_WEBSITE + "/tech",
        note_level=3,
    )
    return [note1, note2, note3]


def notes_to_markdown(notes: List[KeywordNote], header: str = "## 关键词笔记") -> str:
    md_lines = [header, ""]
    for n in notes:
        md_lines.append(f"### {n.title}")
        md_lines.append(f"- **内容**: {n.content}")
        md_lines.append(f"- **标签**: {', '.join(n.tags) if n.tags else '无'}")
        if n.source_url:
            md_lines.append(f"- **来源**: {n.source_url}")
        md_lines.append(f"- **等级**: {n.note_level}")
        md_lines.append(f"- **创建时间**: {n.created_at}")
        md_lines.append("")
    return "\n".join(md_lines)


if __name__ == "__main__":
    demo_notes = build_demo_notes()
    print("=== 格式化单条笔记 ===")
    print(format_note_single(demo_notes[0]))
    print()
    print("=== 格式化全部笔记 ===")
    print(format_note_list(demo_notes))
    print()
    print("=== Markdown 输出 ===")
    print(notes_to_markdown(demo_notes))