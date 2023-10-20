# CLASS TO FLATTEN APPEARANCE FROM JSON-LD TO CSV

from src.shared_content.constants import SHARED_CONTENT_FIELDNAMES, FlatSharedContent


class SharedContentFlattener:
    def __init__(self, data: dict, url: str) -> None:
        # Identifier for the associated appearance
        self.post_url = url

        # --- DIRECT METADATA ---
        self.type = data.get("@type")
        self.content_url = data.get("contentURL")
        self.height = data.get("height")
        self.width = data.get("width")

    def __call__(self) -> FlatSharedContent:
        shared_content_fields = {k: getattr(self, k) for k in SHARED_CONTENT_FIELDNAMES}
        return FlatSharedContent(**shared_content_fields)
