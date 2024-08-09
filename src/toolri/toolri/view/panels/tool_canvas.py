import enum
import typing

import customtkinter

from .image_canvas import ImageCanvas

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


class MousePoints(str, enum.Enum):
    LEFT_START = "left_start"
    LEFT_END = "left_end"
    RIGHT_START = "right_start"


# TODO: this class was taken from a prototype version and shold be better implemented
class ToolCanvas(ImageCanvas):

    name = "Tool"

    __DEFAULT_POINT = [0, 0]

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)
        self.__box_draw_id = None
        self.__link_draw_id = None
        self._box: typing.Union[None, tuple[int, int, int, int]] = None
        self._link: typing.Union[None, tuple[int, int, int, int]] = None
        self.__last_point: typing.Union[None, tuple[int, int]] = None
        self.__init__mouse_points()
        self.__init_buttons()
        self.__active_draw_shape: typing.Literal["point", "box", "link"] = "point"

    def activate_shape(self, shape: typing.Literal["point", "box", "link"]):
        self.__active_draw_shape = shape

    def deactivate_shape(self):
        self.__active_draw_shape = "point"

    def __get_point(self) -> tuple[int, int]:  # type: ignore
        if self.__last_point is not None:
            return self.__last_point

    def __get_box(self) -> tuple[int, int, int, int]:  # type: ignore
        if self._box is not None:
            return self._box

    def __get_link(self) -> tuple[int, int, int, int]:  # type: ignore
        if self._link is not None:
            return self._link

    def __send_geometry(self):
        if self.__active_draw_shape == "point":
            geometry = self.__get_point()
        elif self.__active_draw_shape == "box":
            geometry = self.__get_box()
        elif self.__active_draw_shape == "link":
            geometry = self.__get_link()
        if geometry is not None:
            self._toolri_controller.receive_geometry(geometry=geometry)

    def __init__mouse_points(self):
        self.__mouse_points: dict[str, list[int]] = {
            holder.value: self.__DEFAULT_POINT for holder in MousePoints
        }

    def __init_buttons(self):
        self.bind_key("<ButtonPress-1>", self._mouse_left_button_press)
        self.bind_key("<B1-Motion>", self._mouse_left_button_motion)
        self.bind_key("<ButtonRelease-1>", self._mouse_left_button_release)
        self.bind_key("<Button-3>", self._mouse_right_button_press)
        self.bind_key("<Button-2>", self._mouse_middle_button_press)
        self.bind_key("<B2-Motion>", self._mouse_middle_button_motion)
        self.bind_key("<ButtonRelease-2>", self._mouse_middle_button_release)

    def __draw_shape(self, shape: typing.Literal["link", "box"]):
        if self.__box_draw_id is not None:
            self.delete_drawing(drawing_id=self.__box_draw_id)
            self.__box_draw_id = self.draw(
                self._box,  # type: ignore
                shape="box",
                dash=(5,),
            )
        if shape == "link":
            if self.__link_draw_id is not None:
                self.__update_draw(draw_id=self.__link_draw_id)
            else:
                self.__link_draw_id = self.draw(
                    (
                        int(self.__mouse_points[MousePoints.LEFT_START][0]),
                        int(self.__mouse_points[MousePoints.LEFT_START][1]),
                        int(self.__mouse_points[MousePoints.LEFT_END][0]),
                        int(self.__mouse_points[MousePoints.LEFT_END][1]),
                    ),
                    dash=(5,),
                    shape="link",
                )
        elif shape == "box":
            pass

    def __update_box(self):
        self._box = [
            int(self.__mouse_points[MousePoints.LEFT_START][0]),
            int(self.__mouse_points[MousePoints.LEFT_START][1]),
            int(self.__mouse_points[MousePoints.LEFT_END][0]),
            int(self.__mouse_points[MousePoints.LEFT_END][1]),
        ]

    def __update_link(self):
        self._link = [
            int(self.__mouse_points[MousePoints.LEFT_START][0]),
            int(self.__mouse_points[MousePoints.LEFT_START][1]),
            int(self.__mouse_points[MousePoints.LEFT_END][0]),
            int(self.__mouse_points[MousePoints.LEFT_END][1]),
        ]

    def __updates_shapes(self):
        self.__update_box()
        self.__update_link()

    def __get_current_mouse_point(self, event, point_holder: MousePoints):
        point = self.__image_canvas.point_screen2canvas([event.x, event.y])
        self.__mouse_points[point_holder] = point
        self.__last_point = point
        self.__updates_shapes()

    def _get_current_mouse_point_on_image(self) -> list:
        image_point = self.__image_canvas.point_canvas2image(self.__last_point)
        return image_point

    def _mouse_middle_button_press(self, event):
        pass

    def _mouse_left_button_press(self, event):
        self.__clear_drawings()
        self.__get_current_mouse_point(event=event, point_holder=MousePoints.LEFT_START)

    def _mouse_left_button_motion(self, event):
        self.__get_current_mouse_point(event=event, point_holder=MousePoints.LEFT_END)
        if self.__active_draw_shape != "point":
            self.__draw_shape(self.__active_draw_shape)

    def _mouse_left_button_release(self, event):
        self.__get_current_mouse_point(event=event, point_holder=MousePoints.LEFT_END)
        self.__send_geometry()
        self.__clear_drawings()

    def _mouse_right_button_press(self, event):
        self.__clear_drawings()
        self.__get_current_mouse_point(
            event=event, point_holder=MousePoints.RIGHT_START
        )

    def _mouse_middle_button_motion(self, event):
        pass

    def _mouse_middle_button_release(self, event):
        self.__clear_drawings()

    def __clear_drawings(self):
        if self.__box_draw_id is not None:
            self.__image_canvas.delete_drawing(self.__box_draw_id)
            self.__box_draw_id = None
        if self.__link_draw_id is not None:
            self.__image_canvas.delete_drawing(self.__link_draw_id)
            self.__link_draw_id = None
        self.__last_point = None
        self._box = None
        self._link = None
