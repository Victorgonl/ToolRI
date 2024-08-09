import toolri

image = toolri.load_image("examples/samples/uflaforms-072-custom.png")
data = toolri.load_data("examples/samples/uflaforms-072-custom.json")

labels = [
    toolri.ToolRILabel(
        name="DOC_TITLE", color="#F6E000", links=["ANSWER"], is_visible=True
    ),
    toolri.ToolRILabel(name="DOC_INFO", color="#F87900", links=[], is_visible=True),
    toolri.ToolRILabel(
        name="HEADER_KEY",
        color="#58B3C0",
        links=[
            "KEY",
            "VALUE_PERSON",
            "VALUE_ID",
            "VALUE_CHANNEL",
            "VALUE_LOCATION",
            "VALUE_OTHER",
            "VALUE_DATE",
            "HEADER_KEY",
        ],
        is_visible=True,
    ),
    toolri.ToolRILabel(
        name="KEY",
        color="#004BB9",
        links=[
            "ANSWER",
            "VALUE_PERSON",
            "VALUE_CHANNEL",
            "VALUE_ID",
            "VALUE_LOCATION",
            "VALUE_OTHER",
            "VALUE_DATE",
        ],
        is_visible=True,
    ),
    toolri.ToolRILabel(name="VALUE_PERSON", color="#21F960", links=[], is_visible=True),
    toolri.ToolRILabel(
        name="VALUE_CHANNEL", color="#4E2B89", links=[], is_visible=True
    ),
    toolri.ToolRILabel(name="VALUE_ID", color="#A97300", links=[], is_visible=True),
    toolri.ToolRILabel(
        name="VALUE_LOCATION", color="#FF2B9C", links=[], is_visible=True
    ),
    toolri.ToolRILabel(name="VALUE_DATE", color="#1C9336", links=[], is_visible=True),
    toolri.ToolRILabel(name="VALUE_OTHER", color="#700984", links=[], is_visible=True),
    toolri.ToolRILabel(name="OTHER", color="#f30e15", links=[], is_visible=True),
]

data = toolri.toolri(image=image, data=data, labels=labels)

toolri.draw_data_on_image(image=image, data=data, labels=labels).show()
