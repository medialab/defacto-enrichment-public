from dataclasses import dataclass
from typing import Dict, Optional

from casanova import TabularRecord


@dataclass
class SharedContent(TabularRecord):
    post_url: str
    content_url: str
    media_type: str
    height: Optional[str]
    width: Optional[str]

    @classmethod
    def from_json(cls, item: Dict, post_url: str) -> "SharedContent":
        return SharedContent(
            post_url=post_url,
            content_url=item["contentURL"],
            media_type=item["@type"],
            height=item.get("height"),
            width=item.get("width"),
        )

    @classmethod
    def from_csv_dict_row(cls, row: Dict) -> "SharedContent":
        def cast_empty_string(v: str) -> str | None:
            if v != "":
                return v

        row = {k: cast_empty_string(v) for k, v in row.items()}
        return SharedContent(**row)

    def to_json(self) -> Dict:
        base = {"@type": self.media_type, "contentURL": self.content_url}
        if self.height:
            base.update({"height": self.height})
        if self.width:
            base.update({"width": self.width})
        return base
