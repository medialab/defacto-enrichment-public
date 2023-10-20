def parse_interaction_count(
    data: dict, target_service: str, target_action: str
) -> str | None:
    count_array = data.get("interactionStatistic")
    if isinstance(count_array, list):
        for counter in count_array:
            service = counter.get("interactionService", {}).get(
                "name"
            ) or parse_old_interaction_format(counter, "service")
            action = counter.get("interactionType") or parse_old_interaction_format(
                counter, "action"
            )
            if (
                service
                and service.lower() == target_service.lower()
                and action
                and target_action.lower() in action.lower()
            ):
                return counter.get("userInteractionCount")


def parse_creator_interaction_count(
    data: dict, service: str, action: str
) -> str | None:
    creator = data.get("creator")
    if creator:
        return parse_interaction_count(
            data=creator, target_service=service, target_action=action
        )


# DELETE EVENTUALLY
def parse_old_creator_date_created_format(data: dict) -> str | None:
    creator_action = data.get("creator", {}).get("action", {})
    if creator_action.get("@type") == "CreateAction":
        return creator_action.get("result", {}).get("dateCreated")


# DELETE EVENTUALLY
def parse_old_interaction_format(counter: dict, target: str) -> str | None:
    if target == "service":
        return counter.get("object", {}).get("name")
    elif target == "action":
        return counter.get("@type")


def build_interaction_format(service: str, interaction_type: str, count: str):
    return {
        "@type": "InteractionCounter",
        "interactionType": interaction_type,
        "interactionService": {"@type": "WebSite", "name": service},
        "userInteractionCount": count,
    }
