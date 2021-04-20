# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket

import subprocess
from libqtile import qtile

#import sys
#from ruamel.yaml import YAML

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


mod = "mod4"
terminal = 'alacritty'

keys = [


        #Basic control keys:
        #Volume control:
    Key([], "XF86AudioRaiseVolume", lazy.spawn( "pactl set-sink-volume 0 +5%"),
        desc = "Increase volume"),

    Key([], "XF86AudioLowerVolume", lazy.spawn( "pactl set-sink-volume 0 -5%"),
        desc = "Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle"),
        desc = "Mute"),
        #Brightness control:
     Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Brightness Up"),

     Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Brightness Up"),
        #Screenshoting
        # Open GUI
     Key([], "Print", lazy.spawn("xfce4-screenshooter")),
    # Full screen
     Key(["mod4"], "Print", lazy.spawn("xfce4-screenshooter -f")),
    # Select area
     Key(["mod4", "shift"], "Print", lazy.spawn("xfce4-screenshooter -r")),
    # Active window
     Key(["mod4", "control"], "Print", lazy.spawn("xfce4-screenshooter -w")),
     #Open Browser
     Key([mod], "b", lazy.spawn("chromium")),
     Key([mod, "control"], "b", lazy.spawn("firefox")),
     Key([mod, "shift"], "b", lazy.spawn("qutebrowser")),
     Key([mod], "m", lazy.spawn("spotify")),
     Key([mod], "t", lazy.spawn("thunar")),
     Key([mod], "Alt_L" , lazy.spawn("jupyter notebook")),
        # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    #Keyboard layout
    #Key([mod], "shift", cmd_next_keyboard()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    #
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "asdfuiop"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [

    layout.Columns(border_focus='#e35b00', border_normal_stack='#0B426D',
    border_normal='#0B426D', border_width=3, margin=2 ),

    
    # Try more layouts by unleashing below layouts.
    layout.Stack(num_stacks=2, border_focus='#e35b00', border_normal='#0B426D',  border_width=3, margin=2),
    #layout.Bsp(border_width=3, margin=2),
    #layout.Matrix(border_width=3, margin=2),
    layout.MonadWide(border_focus='#e35b00', border_normal_stack='#0B426D',
    border_normal='#0B426D', border_width=3, margin=2),
    #layout.MonadTall(),
    #layout.RatioTile(),
    #layout.Tile(border_focus='#e35b00', border_normal_stack='#0B426D',
    #border_normal='#0B426D', border_width=3, margin=2),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
    
    layout.Max(),
    layout.Floating(border_focus='#e35b00', 
    border_normal='#0B426D', border_width=3),
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())


screens = [
        Screen(
            top=bar.Bar(
                [

                    widget.Spacer(background="#0a1e24",length=10),
                    widget.Image(
                       filename = "~/.config/qtile/icons/pythonBig.png",
                       background = "#0a1e24",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
                       ),
                    widget.Spacer(background="#0a1e24", length=10),

                   
                    widget.GroupBox(
                        margin_y = 3,
                        padding_y = 5,
                        padding_x = 3,
                        borderwidth = 3,
                        active = "#ffffff",
                        inactive = "83a7b4",
                        rounded = True,
                        hightlight_color = "#e35b00",
                        hightlight_method = "line",
                        this_current_screen_border = "#e35b00",
                        this_screen_border = "#06afc7",
                        other_current_screen_border = "#e35b00",
                        other_screen_border = "#06afc7",
                        foreground = "#ffffff",
                        background = "#0a1e24"

                                    ),
                    
                    widget.Prompt( background="#0a1e24"
                                 ), 
                    widget.WindowName( background="#0a1e24"
                                     ),                
                    widget.Chord( background="#0a1e24",
    
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                                  },
                    name_transform=lambda name: name.upper(),
                                ),
               
                    widget.Systray( background="#0a1e24", icon_size=24, padding = 10
                                  ),
                    widget.Spacer(background="#0a1e24", length=10),
                    #widget.KhalCalendar(),

		            widget.Clock(format='%d %b, %a, %I:%M %p',
                        background="#0a1e24"),

                    #widget.Volume(background="#0a1e24"),
                    
                    #widget.BatteryIcon(background="#0a1e24"),

                    widget.KeyboardLayout(configured_keyboards=['us','ru',], background="#0a1e24", update_interval=0.2),

               
		           # widget.QuickExit(background="#0a1e24"),

                    widget.CurrentLayoutIcon(background="#0a1e24",
                            mouse_callbacks = {'Button1': lambda: cmd_next_layout()}),
                    ], 
            24, opacity=0.80,
            ),
        ),    
]        
    



# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


# Startup hook:


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('/home/john/.config/qtile/autostart.sh')
    subprocess.call([home])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
