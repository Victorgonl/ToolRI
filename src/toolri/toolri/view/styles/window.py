from .top_level import ToolRITopLevel


def ToolRIWindow(master, title):
    window = ToolRITopLevel(master=master.master, title=title)
    window.resizable(False, False)
    window.transient(master=master)
    window.update()
    window.grab_set()
    return window
