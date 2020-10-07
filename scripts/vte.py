#!/usr/bin/env python

from gi.repository import Gtk, Vte
from gi.repository import GLib
import os

class MyTerm(Vte.Terminal):
    def __init__(self, *args, **kwds):
        super(MyTerm, self).__init__(*args, **kwds)
        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
        self.pid = None
    def executeCommand(self,cmdstr):
        working_directory = ""
        env = os.environ.copy()
        env['TERM'] = "xterm"
        envv = ['%s=%s' % kv for kv in list(env.items())]
        if isinstance(command_string,(tuple,list)):
             argv = command_string
        else:
             argv = ['/bin/bash','-c','clear;echo;echo;' + command_string]
        print(("Terminal execute command: %s" % command_string))
        self.pid = self.fork_command_full(Vte.PtyFlags.DEFAULT,
             working_directory,
             argv,
             envv,
             GLib.SpawnFlags.DO_NOT_REAP_CHILD,
             None,
             None)[1]

#win = Gtk.Window()
#win.connect('delete-event', Gtk.main_quit)
#bigbox = Gtk.Box()
#win.add(bigbox)
#bigbox.add(MyTerm())
#win.show_all()

#Gtk.main()
