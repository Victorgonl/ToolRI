import dataclasses
import functools
import platform
import typing

import numpy
import PIL.Image
import PIL.ImageTk

from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


class DrawWidth(enum.Enum):
    SMALL = 1
    MEDIUM = 2
    BIG = 3


@dataclasses.dataclass
class Draw:
    geometry: tuple[int, int, int, int]
    shape: typing.Literal["box", "link", "line"]
    ajust_to_image: bool
    tags: typing.Union[str, tuple[str, str]]
    color: str = BLACK
    width: DrawWidth = DrawWidth.BIG
    dash: bool = False
    fill: bool = False
    arrowshape = (8, 12, 4)
    move_dashes: bool = False
    ajust_boxes: bool = False


class ImageCanvas(Panel):

    __BOX = "box"
    __LINK = "link"
    __TEMP = "temp"

    __DASH = (5,)
    __FILL = "gray50"

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)

        self.__canvas = self.__init_canvas()

        self.__original_image = PIL.Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        self.__image = self.__original_image.copy()
        self.__image_tk = None

        self.__current_zoom = 0
        self.__max_zoom = 1.5
        self.__min_zoom = 0.5
        self.__zoom_step = 0.1
        self.__image_zoom_cache: dict[float, PIL.ImageTk.PhotoImage] = {}
        self.__canvas_image_id = self.__canvas.create_image(
            0, 0, anchor="nw", image=self.__image_tk
        )

        self.__drawings: dict[int, Draw] = {}

        self.__button_event_active = False
        self.__right_mouse_function: typing.Literal["point", "box", "link"] = "point"
        self.__left_mouse_function: typing.Literal["point", "box", "link"] = "point"
        self.__right_mouse_geometry: typing.Union[None, tuple[int, int, int, int]] = (
            None
        )
        self.__left_mouse_geometry: typing.Union[None, tuple[int, int, int, int]] = None

        self.set_image(image=self.__original_image, loading_bar=False)

    @property
    def __image_tk_width(self):
        return self.__image_tk.width()  # type: ignore

    @property
    def __image_tk_height(self):
        return self.__image_tk.height()  # type: ignore

    @property
    def __canvas_tk_width(self):
        return self.__canvas.winfo_width()  # type: ignore

    @property
    def __canvas_tk_height(self):
        return self.__canvas.winfo_height()  # type: ignore

    def __init_canvas(self):

        def zoom_out(event):
            self.delete_temporary_drawings()
            self.__zoom(zoom="out")

        def zoom_in(event):
            self.delete_temporary_drawings()
            self.__zoom(zoom="in")

        canvas = ToolRICanvas(self._master)
        canvas.pack(side="left", expand=True, fill="both")
        canvas.bind("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Down>", lambda event: canvas.yview_scroll(1, "units"))
        canvas.bind("<Left>", lambda event: canvas.xview_scroll(-1, "units"))
        canvas.bind("<Right>", lambda event: canvas.xview_scroll(1, "units"))
        canvas.bind(
            "<ButtonPress-1>", lambda event: self._mouse_button_press(event, "left")
        )
        canvas.bind(
            "<B1-Motion>", lambda event: self._mouse_button_motion(event, "left")
        )
        canvas.bind(
            "<ButtonRelease-1>", lambda event: self._mouse_button_release(event, "left")
        )
        canvas.bind(
            "<ButtonPress-3>", lambda event: self._mouse_button_press(event, "right")
        )
        canvas.bind(
            "<B3-Motion>", lambda event: self._mouse_button_motion(event, "right")
        )
        canvas.bind(
            "<ButtonRelease-3>",
            lambda event: self._mouse_button_release(event, "right"),
        )
        scrollbar_x = ToolRIScrollbar(canvas, orientation="horizontal")
        scrollbar_x.configure(command=canvas.xview)
        canvas.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y = ToolRIScrollbar(canvas, orientation="vertical")
        scrollbar_y.configure(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        if platform.system() == "Windows":
            canvas.bind(
                "<MouseWheel>",
                lambda event: canvas.yview_scroll(
                    -1 if event.delta > 0 else 1, "units"
                ),
            )
            canvas.bind(
                "<Control-MouseWheel>",
                lambda event: (zoom_in(event) if event.delta > 0 else zoom_out(event)),
            )
        else:
            canvas.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
            canvas.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
            canvas.bind("<Control-Button-4>", zoom_in)
            canvas.bind("<Control-Button-5>", zoom_out)

        return canvas

    def set_image(self, image: PIL.Image.Image, loading_bar=True):
        self.__original_image = image
        self.__image = self.__original_image.copy()
        x = self.__canvas_tk_width
        y = int(self.__image.size[1] * (x / self.__image.size[0]))
        self.__image = self.__image.resize(size=(x, y))

        zoom_values = numpy.arange(
            self.__min_zoom, self.__max_zoom + self.__zoom_step, self.__zoom_step
        )

        if loading_bar:
            self.delete_all_drawings()
            loading_frame = ToolRIFrame(
                self.__canvas,
                fg_color=TEXT_FG_COLOR,
                corner_radius=15,
                bg_color="transparent",
            )
            loading_label = ToolRILabel(
                master=loading_frame,
                text="Loading...",
                font=TEXT_BIG,
            )
            loading_bar = ToolRIProgressBar(master=loading_frame)
            loading_status = 0.0
            loading_bar.set(loading_status)
            loading_ratio = 1 / (len(zoom_values))
            loading_label.pack(padx=25, pady=(25, 0))
            loading_bar.pack(padx=25, pady=(0, 25))
            loading_frame.pack(expand=True)

        for i, zv in enumerate(zoom_values):
            width, height = self.__image.size
            new_size = int(width * zv), int(height * zv)
            resized_image = self.__image.resize(new_size)
            image_tk = PIL.ImageTk.PhotoImage(resized_image)
            self.__image_zoom_cache[i] = image_tk
            if loading_bar:
                loading_status += loading_ratio  # type: ignore
                loading_bar.set(loading_status)
                loading_frame.update()

        self.__current_zoom = 4
        self.__zoom(zoom="in")

        if loading_bar:
            loading_frame.destroy()

    def __zoom(self, zoom: typing.Literal["in", "out"]):
        if zoom == "in" and self.__current_zoom < len(self.__image_zoom_cache) - 1:
            self.__current_zoom += 1
        elif zoom == "out" and self.__current_zoom > 0:
            self.__current_zoom -= 1

        self.__image_tk = self.__image_zoom_cache[self.__current_zoom]
        self.__canvas.itemconfig(self.__canvas_image_id, image=self.__image_tk)

        self.__canvas.config(
            scrollregion=(0, 0, self.__image_tk.width(), self.__image_tk.height())
        )
        self.__redraw()

    def __redraw(self):
        for drawing_id in list(self.__drawings.keys()):
            self.__update_draw(drawing_id)

    def __canvas_coords_to_image_coords(
        self, geometry: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:
        return (
            round(geometry[0] * self.__original_image.size[0] / self.__image_tk_width),
            round(geometry[1] * self.__original_image.size[1] / self.__image_tk_height),
            round(geometry[2] * self.__original_image.size[0] / self.__image_tk_width),
            round(geometry[3] * self.__original_image.size[1] / self.__image_tk_height),
        )

    def __image_coords_to_canvas_coords(
        self, geometry: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:
        return (
            int(geometry[0] * self.__image_tk_width / self.__original_image.size[0]),
            int(geometry[1] * self.__image_tk_height / self.__original_image.size[1]),
            int(geometry[2] * self.__image_tk_width / self.__original_image.size[0]),
            int(geometry[3] * self.__image_tk_height / self.__original_image.size[1]),
        )

    def draw_box(
        self,
        box: tuple[int, int, int, int],
        entity_id=None,
        color=BLACK,
        width=DrawWidth.BIG,
        fill: bool = False,
        dash: bool = False,
        move_dashes=False,
    ):

        if entity_id is None:
            tags = (self.__BOX, self.__TEMP)
        else:
            tags = (self.__BOX, str(entity_id))

        box_draw = Draw(
            geometry=box,
            shape="box",
            color=color,
            width=width,
            fill=fill,
            dash=dash,
            move_dashes=move_dashes,
            ajust_to_image=True,
            tags=tags,
        )
        box_draw_id = self.__draw(box_draw)
        return box_draw_id

    def draw_link(
        self,
        link: tuple[int, int, int, int],
        entity_id=None,
        color=BLACK,
        width=DrawWidth.BIG,
        fill=False,
        dash: bool = False,
        move_dashes=False,
    ):

        if entity_id is None:
            tags = (self.__LINK, self.__TEMP)
        else:
            tags = (self.__LINK, str(entity_id))

        link_draw = Draw(
            geometry=link,
            shape="link",
            color=color,
            width=width,
            fill=fill,
            dash=dash,
            move_dashes=move_dashes,
            ajust_to_image=True,
            tags=tags,
        )
        link_draw_id = self.__draw(link_draw)
        return link_draw_id

    def draw_line(
        self,
        line: tuple[int, int, int, int],
        entity_id=None,
        color=BLACK,
        width=DrawWidth.BIG,
        fill=False,
        dash: bool = False,
        move_dashes=False,
    ):

        if entity_id is None:
            tags = (self.__LINK, self.__TEMP)
        else:
            tags = (self.__LINK, str(entity_id))

        link_draw = Draw(
            geometry=line,
            shape="line",
            color=color,
            width=width,
            fill=fill,
            dash=dash,
            move_dashes=move_dashes,
            ajust_to_image=True,
            tags=tags,
        )
        link_draw_id = self.__draw(link_draw)
        return link_draw_id

    def delete_drawing(self, drawing_id):
        self.__canvas.delete(drawing_id)
        del self.__drawings[drawing_id]

    def delete_all_drawings(self):
        for drawing_id in list(self.__drawings):
            self.delete_drawing(drawing_id=drawing_id)

    def __draw(self, draw: Draw) -> int:

        self.delete_temporary_drawings()

        dash = self.__DASH if draw.dash or draw.move_dashes else ""

        geometry = draw.geometry
        if draw.ajust_to_image:
            geometry = self.__image_coords_to_canvas_coords(geometry)

        def animate_dashes(box):
            move_dash(box)
            self._set_timer_function(100, functools.partial(animate_dashes, box))

        def move_dash(box):
            # Get current dash pattern
            dash_offset = self.__canvas.itemcget(box, "dashoffset")
            if not dash_offset:
                dash_offset = 0
            else:
                dash_offset = int(dash_offset)
            # Move the dash by changing the dash offset
            dash_offset -= 1
            self.__canvas.itemconfig(box, dashoffset=dash_offset)

        if draw.shape == "box":
            stipple = self.__FILL if draw.fill else ""
            fill = draw.color if draw.fill else ""
            draw_id = self.__canvas.create_rectangle(
                geometry[0],
                geometry[1],
                geometry[2],
                geometry[3],
                outline=draw.color,
                width=draw.width.value,
                tags=draw.tags,
                dash=dash,
                stipple=stipple,
                fill=fill,
            )
        elif draw.shape == "link":
            draw_id = self.__canvas.create_line(
                geometry[0],
                geometry[1],
                geometry[0],
                geometry[1],
                fill=draw.color,
                width=draw.width.value,
                arrow="last",
                dash=dash,
                arrowshape=draw.arrowshape,
                tags=draw.tags,
            )
        elif draw.shape == "line":
            draw_id = self.__canvas.create_line(
                geometry[0],
                geometry[1],
                geometry[0],
                geometry[1],
                fill=draw.color,
                width=draw.width.value,
                dash=dash,
                tags=draw.tags,
            )

        if draw.move_dashes:
            animate_dashes(draw_id)

        self.__drawings[draw_id] = draw

        # TODO: this is fixing a problem where the link needs to be updated to be draw, so it must be remove after find the problem source
        self.__update_draw(draw_id=draw_id)

        return draw_id

    def __update_draw(self, draw_id):
        draw = self.__drawings[draw_id]
        geometry = draw.geometry
        if draw.ajust_to_image:
            geometry = self.__image_coords_to_canvas_coords(geometry)
        self.__canvas.coords(
            draw_id, geometry[0], geometry[1], geometry[2], geometry[3]
        )
        self.__canvas.tag_raise(draw_id)

    def delete_temporary_drawings(self):
        drawings_ids = self.__canvas.find_withtag(self.__TEMP)
        self.__canvas.delete(self.__TEMP)
        for draw_id in drawings_ids:
            del self.__drawings[draw_id]

    def activate_left_mouse_button_function(
        self, shape: typing.Literal["point", "box", "link"]
    ):
        self.__left_mouse_function = shape

    def activate_right_mouse_button_function(
        self, shape: typing.Literal["point", "box", "link"]
    ):
        self.__right_mouse_function = shape

    def __send_geometry_or_point(self, mouse_button: typing.Literal["right", "left"]):
        if mouse_button == "left":
            function = self.__left_mouse_function
            geometry = self.__left_mouse_geometry
        elif mouse_button == "right":
            function = self.__right_mouse_function
            geometry = self.__right_mouse_geometry
        if geometry is not None:
            geometry = self.__canvas_coords_to_image_coords(geometry=geometry)
            if function != "point":
                self._toolri_controller.receive_mouse_function(
                    geometry_or_point=geometry, mouse_button=mouse_button
                )
            else:
                point = (geometry[0], geometry[1])
                self._toolri_controller.receive_mouse_function(
                    geometry_or_point=point, mouse_button=mouse_button
                )

    def __draw_selection(self, mouse_button: typing.Literal["right", "left"]):
        if mouse_button == "left":
            function = self.__left_mouse_function
            geometry = self.__left_mouse_geometry
        elif mouse_button == "right":
            function = self.__right_mouse_function
            geometry = self.__right_mouse_geometry
        self.delete_temporary_drawings()
        if function != "point":
            draw = Draw(
                geometry=geometry,  # type: ignore
                dash=True,
                shape=function,
                ajust_to_image=False,
                tags=self.__TEMP,
            )
            self.__draw(draw=draw)

    def __update_mouse_geometry(
        self, x, y, mouse_button: typing.Literal["right", "left"]
    ):
        if mouse_button == "right":
            geometry = self.__right_mouse_geometry
        elif mouse_button == "left":
            geometry = self.__left_mouse_geometry
        if geometry is None:
            geometry = [x, y, 0, 0]
        geometry = (geometry[0], geometry[1], x, y)
        if mouse_button == "right":
            self.__right_mouse_geometry = geometry
        elif mouse_button == "left":
            self.__left_mouse_geometry = geometry

    def __clear_mouse_geometry(self):
        self.__right_mouse_geometry = None
        self.__left_mouse_geometry = None

    def __get_canvas_mouse_position(self, event):
        x, y = self.__canvas.canvasx(event.x), self.__canvas.canvasy(event.y)
        return x, y

    def _mouse_button_press(self, event, mouse_button: typing.Literal["right", "left"]):
        self.__button_event_active = True
        self.delete_temporary_drawings()
        self.__clear_mouse_geometry()
        x, y = self.__get_canvas_mouse_position(event)
        self.__update_mouse_geometry(x, y, mouse_button=mouse_button)

    def _mouse_button_motion(
        self, event, mouse_button: typing.Literal["right", "left"]
    ):
        if not self.__button_event_active:
            return
        x, y = self.__get_canvas_mouse_position(event)
        self.__update_mouse_geometry(x, y, mouse_button=mouse_button)
        self.__draw_selection(mouse_button=mouse_button)

    def _mouse_button_release(
        self, event, mouse_button: typing.Literal["right", "left"]
    ):
        if not self.__button_event_active:
            return
        x, y = self.__get_canvas_mouse_position(event)
        self.__update_mouse_geometry(x, y, mouse_button=mouse_button)
        self.delete_temporary_drawings()
        self.__send_geometry_or_point(mouse_button=mouse_button)
        self.__button_event_active = False
