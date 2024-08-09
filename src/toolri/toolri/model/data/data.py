import enum
import json
import typing

from ..json import ToolRIJSONEncoder

EMPTY_LABEL = ""


class EntityKeys(str, enum.Enum):
    ID = "id"
    TEXT = "text"
    BOX = "box"
    WORDS = "words"
    BOXES = "boxes"
    LABEL = "label"
    LINKS = "links"


class BoxOptions(str, enum.Enum):
    ENTITIES = "Entities"
    WORDS = "Words"
    BOTH = "Both"


class ToolRIEntity:

    def __init__(self, entitie_dict: dict) -> None:
        self.id: int = entitie_dict[EntityKeys.ID]
        self.text: str = entitie_dict[EntityKeys.TEXT]
        self.box: tuple[int, int, int, int] = entitie_dict[EntityKeys.BOX]
        self.words: list[str] = entitie_dict[EntityKeys.WORDS]
        self.boxes: list[tuple[int, int, int, int]] = entitie_dict[EntityKeys.BOXES]
        self.label: str = entitie_dict[EntityKeys.LABEL]
        self.links: list[list[int]] = entitie_dict[EntityKeys.LINKS]

    def __getitem__(self, key: EntityKeys):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError

    def get_as_dict(self):
        entity_dict = {KEY.value: self[KEY] for KEY in EntityKeys}
        return entity_dict

    def set_label(self, label):
        self.label = label

    def add_link(self, link):
        if link in self.links:
            raise RuntimeError(f"Link {link} already exist.")
        self.links.append(link)

    def delete_links(self, entity_id):
        links = []
        for link in self.links:
            if entity_id not in link:
                links.append(link)
        self.links = links

    def clear_label(self):
        self.label = EMPTY_LABEL

    def clear_links(self):
        self.links = []

    def remove_link(self, entity_id_to_remove):
        new_links = []
        for link in self.links:
            if entity_id_to_remove not in link:
                new_links.append(link)
        self.links = new_links


class ToolRIData:
    def __init__(self, entities_dict_list: typing.Union[None, list[dict]]) -> None:
        if entities_dict_list is None:
            entities_dict_list = []
        self.__check_data(entities_dict_list=entities_dict_list)
        self.__entities: dict[int, ToolRIEntity] = {
            entitie["id"]: ToolRIEntity(entitie) for entitie in entities_dict_list
        }

    def __check_data(self, entities_dict_list):
        unique_ids = []
        for entity in entities_dict_list:
            if entity[EntityKeys.ID] not in unique_ids:
                unique_ids.append(entity[EntityKeys.ID])
            else:
                raise RuntimeError(
                    f"Invalid ToolRI Data: entity ID '{entity[EntityKeys.ID]}' is not unique."
                )
        for entity in entities_dict_list:
            for link in entity[EntityKeys.LINKS]:
                if len(link) != 2:
                    raise RuntimeError(f"Invalid ToolRI Data: link '{link}' size != 2.")
                for entity_id in link:
                    if entity_id not in unique_ids:
                        raise RuntimeError(
                            f"Invalid ToolRI Data: link containing non-existing entity with ID '{entity_id}'."
                        )

    def __check_entity_non_duplication(self, words, boxes):
        for entity in self.__entities.values():
            if entity.boxes == boxes and entity.words == words:
                return False
        return True

    @property
    def entities(self):
        return list(self.__entities.values())

    def get_entity(self, entity_id):
        return self.__entities[entity_id]

    def get_entities(self):
        return list(self.__entities.values())

    def get_entities_ids(self):
        return list(self.__entities.keys())

    def get_entities_dict(self):
        entities = self.get_entities()
        entities_dict = [entity.get_as_dict() for entity in entities]
        return entities_dict

    def get_entities_by_point(
        self, point: tuple[int, int], box_option: BoxOptions
    ) -> list[ToolRIEntity]:
        """Returns a list with all entities whose box contains the `point`."""
        entities = []
        if box_option == BoxOptions.WORDS:
            for entity in self.__entities.values():
                for box in entity.boxes:
                    if point_in_box(image_point=point, box=box):
                        entities.append(entity)
        else:
            for entity in self.__entities.values():
                if point_in_box(image_point=point, box=entity.box):
                    entities.append(entity)
        return entities

    def get_entities_ids_by_point(
        self, image_point: tuple[int, int], box_option: BoxOptions
    ) -> list:
        entities = self.get_entities_by_point(point=image_point, box_option=box_option)
        entities_ids = [entity.id for entity in entities]
        return entities_ids

    def label_entity(self, entity_id: int, label: str):
        self.__entities[entity_id].set_label(label)

    def link_entities(self, entity_k_id: int, entity_v_id: int):
        if entity_k_id == entity_v_id:
            raise RuntimeError(
                f"ToolRIEntity key (id = {entity_k_id}) and entity value (id = {entity_v_id}) must be different."
            )
        link = [entity_k_id, entity_v_id]
        self.__entities[entity_k_id].add_link(link)
        self.__entities[entity_v_id].add_link(link)

    def get_child_entities_by_entity_id(self, entity_id) -> list[ToolRIEntity]:
        entities = []
        parent_entity = self.get_entity(entity_id=entity_id)
        for link in parent_entity.links:
            if link[0] == entity_id:
                entities.append(self.get_entity(link[1]))
        return entities

    def get_parent_entities_by_entity_id(self, entity_id) -> list[ToolRIEntity]:
        entities = []
        parent_entity = self.get_entity(entity_id=entity_id)
        for link in parent_entity.links:
            if link[1] == entity_id:
                entities.append(self.get_entity(link[0]))
        return entities

    def get_entities_with_link(self, entity_id):
        entities_with_link: list[ToolRIEntity] = []
        entities = self.get_entities()
        for entity in entities:
            for link in entity.links:
                if entity_id in link:
                    entities_with_link.append(entity)
                    continue
        return entities_with_link

    def delete_links(self, entity_id: int):
        entities_with_link = self.get_entities_with_link(entity_id=entity_id)
        for entity in entities_with_link:
            entity.delete_links(entity_id)

    def delete_entity(self, entity_id: int):
        self.delete_links(entity_id=entity_id)
        del self.__entities[entity_id]

    def __next_entity_id_available(self) -> int:
        entities_ids = self.get_entities_ids()
        new_entity_id = next(
            i for i in range(len(entities_ids) + 1) if i not in entities_ids
        )
        return new_entity_id

    def create_entity(self, words=None, boxes=None, label=EMPTY_LABEL) -> int:
        if not self.__check_entity_non_duplication(words=words, boxes=boxes):
            raise RuntimeError(f"Entity with same words and boxes already exist.")
        new_entity_id = self.__next_entity_id_available()
        new_entity_dict = {
            EntityKeys.ID: new_entity_id,
            EntityKeys.WORDS: words,
            EntityKeys.BOXES: boxes,
            EntityKeys.TEXT: join_words(words),
            EntityKeys.BOX: join_boxes(boxes),
            EntityKeys.LABEL: label,
            EntityKeys.LINKS: [],
        }
        entity = ToolRIEntity(entitie_dict=new_entity_dict)
        self.__entities[new_entity_id] = entity
        return new_entity_id

    def edit_entity(self, entity_id, words, label):
        entity = self.__entities[entity_id]
        entity.words = words
        entity.label = label

    def clear_label(self, entity_id: int):
        self.__entities[entity_id].clear_label()

    def clear_links(self, entity_id: int):
        for entity in self.__entities.values():
            entity.remove_link(entity_id_to_remove=entity_id)

    def clear_all_links(self):
        for entity_id, entity in self.__entities.items():
            entity.links = []

    def clear_all_labels(self):
        for entity_id, entity in self.__entities.items():
            entity.label = EMPTY_LABEL

    def clear_all_data(self):
        self.__entities = {}

    def __update_entity(self, entity: ToolRIEntity) -> ToolRIEntity:
        self.__entities[entity.id] = entity
        return entity

    def __add_entity(self, entity: ToolRIEntity) -> ToolRIEntity:
        if entity.id in self.__entities:
            entity.id = self.__next_entity_id_available()
        return self.__update_entity(entity=entity)

    def set_data_by_json(self, json_data: str) -> list[int]:
        entities_dict_list = json.loads(json_data)
        self.__init__(entities_dict_list=entities_dict_list)
        return list(self.__entities.keys())

    def join_entities(self, entity_k_id: int, entity_v_id: int) -> int:
        if entity_k_id == entity_v_id:
            raise RuntimeError(
                f"ToolRIEntity key (id = {entity_k_id}) and entity value (id = {entity_v_id}) must be different."
            )
        first_entity = self.get_entity(entity_id=entity_k_id)
        second_entity = self.get_entity(entity_id=entity_v_id)
        joined_entity_dict = {
            EntityKeys.ID: first_entity.id,
            EntityKeys.WORDS: first_entity.words + second_entity.words,
            EntityKeys.BOXES: first_entity.boxes + second_entity.boxes,
            EntityKeys.TEXT: join_words(first_entity.words + second_entity.words),
            EntityKeys.BOX: join_boxes([first_entity.box, second_entity.box]),
            EntityKeys.LABEL: first_entity.label,
            EntityKeys.LINKS: first_entity.links,
        }
        joined_entity = ToolRIEntity(entitie_dict=joined_entity_dict)
        self.__entities[first_entity.id] = joined_entity
        self.delete_entity(second_entity.id)
        return first_entity.id

    def update_label_name(self, old_label_name, new_label_name):
        for entity in self.__entities.values():
            if entity.label == old_label_name:
                entity.set_label(new_label_name)

    def clear_labels_by_label_name(self, label_name):
        for entity in self.__entities.values():
            if entity.label == label_name:
                entity.clear_label()

    def split_entitie_by_words(self, entity_id) -> list[int]:
        new_entities_ids = []
        for entity in self.entities:
            if entity.id == entity_id:
                words, boxes = entity.words, entity.boxes
                label = entity.label
                if len(words) > 1:
                    self.delete_entity(entity.id)
                    for word, box in zip(words, boxes):
                        new_entity_id = self.create_entity(
                            words=[word], boxes=[box], label=label
                        )
                        new_entities_ids.append(new_entity_id)
        return new_entities_ids

    def get_json_data(self):
        json_data = json.dumps(
            self.get_entities_dict(),
            indent=4,
            cls=ToolRIJSONEncoder,
            ensure_ascii=False,
        )
        return json_data


def point_in_box(image_point: tuple[int, int], box: tuple[int, int, int, int]):
    """Returns `True` if the `point` belongs to the `box` and `False` otherwise."""
    if image_point[0] >= box[0] and image_point[0] <= box[2]:
        if image_point[1] >= box[1] and image_point[1] <= box[3]:
            return True
    return False


def join_words(words):
    text = ""
    n = len(words)
    for i in range(n):
        text += words[i]
        if i < n - 1:
            text += " "
    return text


def join_boxes(boxes_to_join):
    box = [0, 0, 0, 0]
    if not boxes_to_join:
        return box
    x0_list = [box[0] for box in boxes_to_join]
    y0_list = [box[1] for box in boxes_to_join]
    x1_list = [box[2] for box in boxes_to_join]
    y2_list = [box[3] for box in boxes_to_join]
    box = [min(x0_list), min(y0_list), max(x1_list), max(y2_list)]
    return box
