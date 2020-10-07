#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os

class DoTheLogOut:

    # Cancel/exit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # Hibernate
    def hibernate(self, widget):
        os.system("(sleep 1s && gnome-power-cmd hibernate) && killall python /usr/bin/openbox-logout")

    # Suspend
    def suspend(self, widget):
        os.system("(sleep 1s && gnome-power-cmd suspend) && killall python /usr/bin/openbox-logout")

    # Logout
    def logout(self, widget):
        os.system("gdm-control --reboot && openbox --exit")

    # Reboot
    def reboot(self, widget):
        os.system("gksu reboot")

    # Shutdown
    def shutdown(self, widget):
        os.system("gksu 'shutdown -h now'")

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Exit? Choose an option:")
        self.window.set_resizable(False)
        self.window.set_position(1)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(15)

        # Create a box to pack widgets into
        self.box1 = gtk.HBox(False, 0)
        self.window.add(self.box1)

        # Create cancel button
        self.button1 = gtk.Button(u"キャンセル")
        self.button1.set_border_width(5)
        self.button1.connect("clicked", self.delete_event, "Changed me mind :)")
        self.box1.pack_start(self.button1, True, True, 0)
        self.button1.show()

        # Create hibernate button
        self.button2 = gtk.Button(u"休止状態")
        self.button2.set_border_width(5)
        self.button2.connect("clicked", self.hibernate)
        self.box1.pack_start(self.button2, True, True, 0)
        self.button2.show()

        # Create suspend button
        self.button3 = gtk.Button(u"サスペンド")
        self.button3.set_border_width(5)
        self.button3.connect("clicked", self.suspend)
        self.box1.pack_start(self.button3, True, True, 0)
        self.button3.show()

        # Create logout button
        self.button4 = gtk.Button(u"ログアウト")
        self.button4.set_border_width(5)
        self.button4.connect("clicked", self.logout)
        self.box1.pack_start(self.button4, True, True, 0)
        self.button4.show()

        # Create reboot button
        self.button5 = gtk.Button(u"再起動")
        self.button5.set_border_width(5)
        self.button5.connect("clicked", self.reboot)
        self.box1.pack_start(self.button5, True, True, 0)
        self.button5.show()

        # Create shutdown button
        self.button6 = gtk.Button(u"シャットダウン")
        self.button6.set_border_width(5)
        self.button6.connect("clicked", self.shutdown)
        self.box1.pack_start(self.button6, True, True, 0)
        self.button6.show()

        self.box1.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    gogogo = DoTheLogOut()
    main()
