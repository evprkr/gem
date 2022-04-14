# Gem Text Editor

Gem (code name) is a terminal-based text editor written in Python using curses.

I'm working on this in my spare time in between like 50 other personal projects, because I have a bad habit of taking on too many projects at once. This is also just an excuse for me to better learn curses, and to finally make a text editor, something I've been wanting to do since picking up Vim years ago.

Any planned features (listed below) are not guaranteed, but I'm hoping to at least get the basic functionality and some fun extra stuff going, and we'll see what happens from there.

## "Planned" Features
* Customizable keyboard shortcuts that utilize a leader key for platform-agnosticism
* Commandline with customizable commands plus a bunch of useful built-in commands
* Syntax highlighting for major languages
* Tabline for keeping multiple buffers open and switching between them
* Easy configuration done with YAML (because I like YAML)
* Built-in parsing for custom color schemes (also made with YAML)
* Plugin API for making plugins quick and easy
* Built-in file manager (drawer-style, also very ambitious)
* Terminal integration (split buffer, VERY ambitious)

Once getting the core functionality in place, I will likely move right into the plugin API. I'm thinking that things like the statusline, tabline, and file manager could be added as plugins. That would keep the base installation small and allow users to exclude features they won't use.

## Platform Support
I'm developing Gem on macOS, but it should work fine on any Unix or Unix-like system. Right now, I have no *real* plans for supporting Windows, due to Python not having native support for curses in Windows. There is an alternative, that being windows-curses, so I might be inclined to add support for Windows in the future, depending on how much time and effort that will take. Considering this is just a hobby/learning experience for me right now, it's unlikely to happen unless I get really involved in making this a "real" thing.
