#!/usr/bin/env python3

import dbus

obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
obj = dbus.Interface(obj, "org.freedesktop.Notifications")
obj.Notify("", 0, "", "Hello world", "This is an example notification.", [], {"urgency": 1}, 10000)

