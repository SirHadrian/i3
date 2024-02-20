#!/usr/bin/env python3

from i3ipc import Connection, Event


def find_parent(i3, window_id):

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

    focused_window = i3.get_tree().find_focused()
    parent = find_parent(i3, focused_window.id)

    if parent and parent.layout != 'tabbed' and parent.layout != 'stacked':

        if focused_window.rect.height > focused_window.rect.width:
            if parent.orientation == 'horizontal':
                i3.command('split v')
        else:
            if parent.orientation == 'vertical':
                i3.command('split h')


i3 = Connection()
i3.on(Event.WINDOW_FOCUS, set_layout)
i3.main()
