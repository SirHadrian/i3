#!/usr/bin/env python3

from i3ipc import Connection, Event


def find_parent(i3, window_id):
    """
        Find the parent of a given window id
    """

    def finder(con, parent):
        if con.id == window_id:
            return parent
        for node in con.nodes:
            res = finder(node, con)
            if res:
                return res
        return None

    return finder(i3.get_tree(), None)


def set_layout(i3, e):
    """
        Set the layout/split for the currently
        focused window to either vertical or
        horizontal, depending on its width/height
    """
    win = i3.get_tree().find_focused()
    parent = find_parent(i3, win.id)

    if (parent and parent.layout != 'tabbed'
            and parent.layout != 'stacked'):

        if win.rect.height > win.rect.width:
            if parent.orientation == 'horizontal':
                i3.command('split v')
        else:
            if parent.orientation == 'vertical':
                i3.command('split h')


i3 = Connection()
i3.on(Event.WINDOW_FOCUS, set_layout)
i3.main()
