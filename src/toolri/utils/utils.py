def sort_entities_by_position(entities):
    entities.sort(
        key=lambda entity: (
            entity["box"][1],
            entity["box"][0],
            entity["box"][3],
            entity["box"][2],
            entity["id"],
        )
    )


def sort_entities_links(entities):
    for entity in entities:
        entity["links"].sort(key=lambda link: (link[0], link[1]))


def make_entities_ids_sequencial(entities):
    def fix_links_ids(entities, ids_map):
        for entity in entities:
            for link in entity["links"]:
                link[0] = ids_map[link[0]]
                link[1] = ids_map[link[1]]

    def create_invalid_ids(entities):
        ids_map = {}
        for entity in entities:
            ids_map[entity["id"]] = entity["id"] * -1
            entity["id"] = ids_map[entity["id"]]
        fix_links_ids(entities, ids_map)

    create_invalid_ids(entities)
    ids_map = {}
    for i, entity in enumerate(entities):
        ids_map[entity["id"]] = i
        entity["id"] = ids_map[entity["id"]]
    fix_links_ids(entities, ids_map)
    sort_entities_links(entities)


def fix_entities(entities):
    remove_duplicated_links(entities)
    sort_entities_by_position(entities)
    make_entities_ids_sequencial(entities)


def clear_entities_labels(entities):
    for entity in entities:
        entity["label"] = ""


def clear_entities_links(entities):
    for entity in entities:
        entity["links"] = []


def remove_duplicated_links(entities):
    for entity in entities:
        links = []
        for link in entity["links"]:
            if link not in links:
                links.append(link)
        entity["links"] = links
