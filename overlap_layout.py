from libqtile.backend.base import Window
from libqtile.command.base import expose_command
from libqtile.config import ScreenRect
from libqtile.layout import base
# from libqtile.log_utils import logger


class OverlapLayout(base._SimpleLayoutBase):
    defaults = [
        ("border_focus", "#ff0000", "Focused Border Color."),
        ("border_normal", "#000000", "Unfocused Border Color."),
        ("margin", 0, "Window Margins."),
        ("border_width", 4, "Border width."),
        ("single_side_left", True, "If the First window is fixed on the left (or right)."),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(OverlapLayout.defaults)
        self.last_side_index = 1

    def configure(self, client: Window, screen_rect: ScreenRect) -> None:
        index = self.clients.index(client)
        # logger.warning(f"handling window {index}")
        if index == 0:
            right_aligned = not self.single_side_left
        else:
            right_aligned = self.single_side_left  # invert it because we're not single_side
        if index != 0 and index != self.last_side_index and not client.has_focus:
            # logger.warning(f"hiding window {index}")
            client.hide()
            return
        client.unhide()
        coords = [
            self.margin + (right_aligned and (screen_rect.width // 10 * 4)),
            # who ever said I wasn't a python criminal
            self.margin,
            ((screen_rect.width // 10) * 6) - (self.border_width+self.margin)*2,
            screen_rect.height - (self.border_width+self.margin)*2,
        ]
        # logger.warning("placing window {} at x/y w:h {}/{} {}:{}".format(
        #     index,
        #     *coords,
        # ))
        client.place(
            *coords,
            self.border_width,
            self.border_focus if client.has_focus else self.border_normal,
            margin=self.margin,
        )

    @expose_command
    def next(self) -> None:
        client = self.clients.focus_next(self.clients.current_client) or self.clients.focus_first()
        self.clients.focus(client)
        self.group.focus(client)
        return

    def previous(self) -> None:
        client = self.clients.focus_previous(self.clients.current_client) or self.clients.focus_last()
        self.clients.focus(client)
        self.group.focus(client)
        return

    @expose_command
    def left(self) -> None:
        if self.single_side_left:
            client = self.clients.focus_first()
        else:
            client = self.clients[self.last_side_index]
        self.clients.focus(client)
        self.group.focus(client)

    @expose_command
    def right(self) -> None:
        if not self.single_side_left:
            client = self.clients.focus_first()
        else:
            client = self.clients[self.last_side_index]
        self.clients.focus(client)
        self.group.focus(client)

    @expose_command
    def down(self) -> None:
        index = self.clients.index(self.clients.current_client)
        if index == 0:
            return
        next = self.clients.focus_next(self.clients.current_client)
        if next is None:
            next = self.clients[1]  # hard coded top of side-stack
        self.clients.focus(next)
        self.group.focus(next)

    @expose_command
    def up(self) -> None:
        index = self.clients.index(self.clients.current_client)
        if index == 0:
            return
        if index == 1:
            next = self.clients.focus_last()
        else:
            next = self.clients.focus_previous(self.clients.current_client)
        self.clients.focus(next)
        self.group.focus(next)

    @expose_command
    def shuffle_left(self) -> None:
        if self.single_side_left:
            client = self.clients.focus_first()
        else:
            client = self.clients[self.last_side_index]
        if client.has_focus:
            return
        target = self.clients.current_client
        self.clients.swap(client, target, focus=1)  # this focuses the 2nd arg
        self.group.focus(target)

    @expose_command
    def shuffle_right(self) -> None:
        if not self.single_side_left:
            client = self.clients.focus_first()
        else:
            client = self.clients[self.last_side_index]
        if client.has_focus:
            return
        target = self.clients.current_client
        self.clients.swap(client, target, focus=1)  # this focuses the 2nd arg
        self.group.focus(target)

    # TODO
    # @expose_command
    # def shuffle_down(self) -> None:
    #     return

    # @expose_command
    # def shuffle_up(self) -> None:
    #     return

    @expose_command
    def flip(self) -> None:
        self.single_side_left = not self.single_side_left
        self.group.layout_all()

    def focus(self, client: Window) -> None:
        client.bring_to_front()
        index = self.clients.index(client)
        if index != 0:
            self.last_side_index = index

    def add_client(self, client: Window) -> None:
        self.clients.append(client)

    def remove(self, client: Window) -> Window | None:
        self.last_side_index = min(self.last_side_index, len(self.clients) - 2)
        ret = super().remove(client)
        self.group.layout_all()
        return ret
