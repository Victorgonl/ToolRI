import toolri

image = toolri.load_image("examples/samples/funsd-0000971160.png")
data = toolri.load_data("examples/samples/funsd-0000971160.json")

labels = [
    toolri.ToolRILabel(
        name="HEADER",
        color="#F6A800",
        links=["HEADER", "QUESTION", "ANSWER"],
        is_visible=True,
    ),
    toolri.ToolRILabel(
        name="QUESTION", color="#004B80", links=["ANSWER"], is_visible=True
    ),
    toolri.ToolRILabel(name="ANSWER", color="#00943E", links=[], is_visible=True),
    toolri.ToolRILabel(name="OTHER", color="#DE1F26", links=[], is_visible=True),
]

data = toolri.toolri(image=image, data=data, labels=labels)

toolri.draw_data_on_image(image=image, data=data, labels=labels).show()
