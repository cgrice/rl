import tdl

PANEL_HEIGHT = 20

class Interface(object):

    def __init__(self, console, starty):
        self.root = console
        self.panel = tdl.Console(console.width, PANEL_HEIGHT)

    def render(self):
        # panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
        return True

    def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
        #render a bar (HP, experience, etc). first calculate the width of the bar
        bar_width = int(float(value) / maximum * total_width)
    
        #render the background first
        panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
    
        #now render the bar on top
        if bar_width > 0:
            panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
    
        #finally, some centered text with the values
        text = name + ': ' + str(value) + '/' + str(maximum)
        x_centered = x + (total_width-len(text))//2
        panel.draw_str(x_centered, y, text, fg=colors.white, bg=None)