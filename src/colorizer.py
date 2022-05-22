# Ink Editor - colorizer.py
# github.com/leftbones/ink

import curses, re
from logger import log

# Colorizer
class Colorizer:
    def __init__(self, terminal):
        self.terminal = terminal

        self.color_cache = []
        self.pair_cache = []

        self.color_idx = 0
        self.pair_idx = 1

        self.default_fg = 'f8f8f2'
        self.default_bg = '282a36'

        self.transparent_bg = self.terminal.config.transparentbg

    # Converts a hex code (string) to an rgb code (tuple)
    def hex_to_rgb(self, color):
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        return rgb

    # Check if a color already exists in the cache
    def color_exists(self, color):
        for cc in self.color_cache:
            if cc == color: return True
        return False

    # Parse text (I guess this is technically a lexer) for tags and strings, returns a list
    def parse_text(self, text):
        pos = 0
        tokens = []

        while pos < len(text):
            if text[pos] == '<':
                token = ''
                while text[pos] != '>':
                    token += text[pos]
                    pos += 1
                token += '>'
                tokens.append(token)
                pos += 1
            else:
                token = ''
                while text[pos] != '<':
                    token += text[pos]
                    pos += 1
                    if pos == len(text): break
                tokens.append(token)

        return tokens

    # Find and return a color pair matching a hex code, add a color or color pair if necessary
    def get_pair(self, fg_hex=None, bg_hex=None):
        if not fg_hex: fg_rgb = self.hex_to_rgb(self.default_fg)
        else: fg_rgb = self.hex_to_rgb(fg_hex)

        if not bg_hex: bg_rgb = self.hex_to_rgb(self.default_bg)
        else: bg_rgb = self.hex_to_rgb(bg_hex)

        if not self.color_exists(fg_rgb):
            curses.init_color(self.color_idx, int(fg_rgb[0]/0.255), int(fg_rgb[1]/0.255), int(fg_rgb[2]/0.255))
            fg_color = self.color_idx
            self.color_cache.append(fg_rgb)
            self.color_idx += 1
        else: fg_color = self.color_cache.index(fg_rgb)


        if self.transparent_bg: bg_color = -1
        else:
            if not self.color_exists(bg_rgb):
                curses.init_color(self.color_idx, int(bg_rgb[0]/0.255), int(bg_rgb[1]/0.255), int(bg_rgb[2]/0.255))
                bg_color = self.color_idx
                self.color_cache.append(bg_rgb)
                self.color_idx += 1
            else: bg_color = self.color_cache.index(bg_rgb)

        pair_exists = False
        for pair in self.pair_cache:
            if pair[1] == fg_color and pair[2] == bg_color:
                pair_exists = True
                pair = pair[0]
                break

        if not pair_exists:
            curses.init_pair(self.pair_idx, fg_color, bg_color)
            pair = self.pair_idx
            self.pair_cache.append([self.pair_idx, fg_color, bg_color])
            self.pair_idx += 1

        return pair

    # Print text to the window with the specified colors, adds the colors to the cache if they are not initialized
    def print(self, window, row, col, text, fg_hex, bg_hex=None):
        pair = self.get_pair(fg_hex, bg_hex)

        i = 0
        for char in text[::-1]:
            window.screen.insch(row, col + i, char, curses.color_pair(pair))

    # Parse text for tags then print to the window with the specified attributes and colors
    def print_syntax(self, window, row, col, text):
        tokens = self.parse_text(text)
        pair = curses.color_pair(0)

        i = 0
        for token in tokens:
            if token.startswith('<ink_color_on'):
                try:
                    color = re.findall('\ (.*?)\>', token)[0]
                    pair = curses.color_pair(self.get_pair(color))
                except Exception as e:
                    log.write(e)
                    pair = curses.color_pair(0)
                    pass
            elif token == '<ink_color_off>':
                pair == curses.color_pair(0)
            elif token == '\n':
                pass
            else:
                for char in token:
                    window.screen.insch(row, col + i, char, pair)
                    i += 1


# Testing
def main(screen):
    color = Colorizer()
    color.print(screen, 0, 0, "Hopefully this is cyan", "00ffff")
    color.print(screen, 1, 0, "Hopefully this is magenta", "ff00ff")
    color.print(screen, 2, 0, "Hopefully this is yellow", "ffff00")
    color.print(screen, 3, 0, "Hopefully this is black", "000000")

#    color.tprint(screen, 5, 0, "This [bold]text[/bold] [underline]tags[/underline] [dim]in[/dim] it")

    color.tprint(screen, 7, 0, "[color=#ffff00]int[/color] num [color=#ff00ff]=[/color] [color=#00ffff]123[/color];")

    screen.getch()

if __name__ == '__main__':
    curses.wrapper(main)
