#
# Copyright (C) 2012 - Marcus Dillavou
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import sys

from gi.repository import Gtk, Champlain, GtkChamplain, Clutter

from StopMarker import StopMarker

class GTMap(GtkChamplain.Embed):
    def __init__(self):
        GtkChamplain.Embed.__init__(self)

        # give ourselves an initial size
        self.set_size_request(640, 480)

        self.view = self.get_view()

        # our bus station layer
        self.stop_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.stop_layer)
        self.stop_layer.show()
        self.stop_layer.show_all_markers()

        # !mwd - temp zoom to birmingham
        self.view.go_to(33.511878, -86.808826)
        self.view.set_zoom_level(14)

        # add a route layer
        self.route_layer = Champlain.PathLayer()
        self.view.add_layer(self.route_layer)

        # our big image layer
        self.image_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.image_layer)
        # our picture
        self.picture_group = Clutter.Group()
        self.view.bin_layout_add(self.picture_group, Clutter.BinAlignment.CENTER, Clutter.BinAlignment.CENTER)
        
        self.view.set_kinetic_mode(True)
        self.view.set_reactive(True)


    def add_stop(self, stop):
        m = StopMarker(self, stop)
        self.stop_layer.add_marker(m)
        m.animate_in()

        return m

    def remove_stop(self, stop):
        m = None
        for i in self.stop_layer.get_markers():
            if i.stop == stop:
                m = i
                break
        if m:
            self.stop_layer.remove_marker(m)

    def unshow_stop_info(self):
        for m in self.stop_layer.get_markers():
            m.hide()

    def draw_route(self, r):
        if r is None:
            return

        # clear our route layer of any old stuff
        self.route_layer.remove_all()

        for stop in r.stops:
            self.route_layer.add_node(Champlain.Coordinate.new_full(stop.latitude, stop.longitude))
        self.route_layer.show()
        
        return self.route_layer

    def remove_route(self, route):
        self.route_layer.remove_all()
        self.route_layer.show()

    def show_image(self, img):
        self.picture_group.remove_all()

        self.picture_group.add_child(img)
        self.image_layer.show()

    def remove_image(self, img):
        if img:
            self.picture_group.remove_child(img)

        self.image_layer.hide()
