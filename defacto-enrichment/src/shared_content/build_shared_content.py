def build_shared_content(
    appearance_url: str, shared_content_index: dict
) -> dict | None:
    if shared_content_index.get(appearance_url):
        shared_content = []
        for i in shared_content_index[appearance_url]:
            r = {
                "@type": i["type"],
                "contentURL": i["content_url"],
            }
            if i.get("height"):
                r.update({"height": i["height"]})
            if i.get("width"):
                r.update({"width": i["width"]})
            shared_content.append(r)
        return {"sharedContent": shared_content}
