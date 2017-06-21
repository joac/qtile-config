import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Match, Screen

mod = "mod4"


class Commands:
    """Just a namespace for commands"""
    launch_console = lazy.spawn("dbus-launch gnome-terminal")
    volume_up = lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 +2%"')
    volume_down = lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 -2%"')
    mute_toggle = lazy.spawn('pactl set-sink-mute 0 toggle')
    mic_toggle = lazy.spawn('pactl set-source-mute 1 toggle')
    monitor_brightness_up = lazy.spawn('xbacklight -inc 10')
    monitor_brightness_down = lazy.spawn('xbacklight -dec 10')

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", Commands.launch_console),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_floating()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "d", lazy.spawncmd()),

    Key([mod, "shift"], 'h', lazy.screen.prev_group()),
    Key([mod, "shift"], 'l', lazy.screen.next_group()),

    # Switch focus to other screens
    Key([mod], 'Left', lazy.to_screen(1)),  # left
    Key([mod], 'Right', lazy.to_screen(0)), # right

    # Volume Related Commands
    Key([], 'XF86AudioLowerVolume', Commands.volume_down),
    Key([], 'XF86AudioRaiseVolume', Commands.volume_up),
    Key([], 'XF86AudioMute', Commands.mute_toggle),
    Key([], 'XF86AudioMicMute', Commands.mic_toggle),

    # Screen Brightness
    Key([], 'XF86MonBrightnessUp', Commands.monitor_brightness_up),
    Key([], 'XF86MonBrightnessDown', Commands.monitor_brightness_down),
]

groups = [
    Group('web', matches=[Match(title=["Google Chrome"]), Match(title=["Firefox"])]),
    Group('term'),
    Group('chat', matches=[Match(title=["Pidgin"])]),
    Group('graph', matches=[Match(title=["Inkscape"]), Match(title=["Gimp"])]),
    Group('time', matches=[Match(title=["hamster"])]),
    Group('servers'),
]

for idx, i in enumerate(groups, 1):
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], str(idx), lazy.group[i.name].toscreen())
    )

    # mod2 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], str(idx), lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.RatioTile(),
    layout.MonadTall(),
    layout.Stack(num_stacks=2),
    layout.Tile(),
]

theme = {
    'bg': "033f47",
    'fg': "08b1c7",
    'subtle_gray': "729499",
    'light_green': "308d99",
    'dark_green': "056876",
}

widget_defaults = dict(
    font='roboto',
    fontsize=12,
    padding=4,
    background=theme['bg'],
    foreground=theme['subtle_gray']
)

graph_defaults = {
    'line_width': 2,
    'width': 50,
    'border_width': 0
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.WindowName(
                    fontsize=12,
                    padding=5,
                    foreground=theme['fg']
                ),
                widget.GroupBox(),
                widget.Sep(),
                widget.Prompt(),
                widget.Sep(),
                widget.Systray(),
                widget.Sep(),
                widget.Clock(format='%a %d/%m/%Y %I:%M %p',
                             fontsize=14,
                             padding=8,
                             foreground=theme['fg']
                            ),
                widget.Sep(),
                widget.CPUGraph(**graph_defaults),
                widget.MemoryGraph(
                    graph_color="0ae855",
                    fill_color="0bffa3.3",
                    **graph_defaults
                    ),
                widget.NetGraph(
                    graph_color="b2a400",
                    fill_color="fff36c.3",
                    **graph_defaults
                ),
                 widget.GenPollUrl(url='http://sandia.local:2017/pango/',
                                   json=False,
                                   update_interval=5,
                                   parse=lambda r: r,
                                   markup=True,
                                   ),
                widget.Sep(),
                widget.Backlight(backlight_name='intel_backlight'),
                widget.Sep(),
                widget.Battery(battery_name='BAT0'),
                widget.BatteryIcon(battery_name='BAT0'),
                widget.Battery(battery_name='BAT1'),
                widget.BatteryIcon(battery_name='BAT1'),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.WindowName(
                    fontsize=12,
                    padding=5,
                    foreground=theme['fg']
                ),
                widget.GroupBox(),
                widget.Sep(),
                widget.Prompt(),
            ],
            30,
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
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
