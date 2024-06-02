import app
import math
from tildagonos import tildagonos

from system.eventbus import eventbus
from system.patterndisplay.events import *
from app_components import clear_background

from events.input import Buttons, BUTTON_TYPES

inner_radius = 100
X = 0
Y = 1

class PentApp(app.App):

    def __init__(self):
        self.button_states = Buttons(self)
        self.n = 5
        self.offset = 0
        self.points = PentApp.genpoints(self.n, self.offset)
        eventbus.emit(PatternDisable())
        for i in range(12):
            tildagonos.leds[i+1] = (0, 0, 0)

    @staticmethod
    def genpoints(n, offset):
        coll = [
            [int(inner_radius * math.cos(th + offset)), int(inner_radius * math.sin(th + offset))]
            for th in
            [(math.pi * 2 / n) * x for x in range(0,n)]
        ]
        return PentApp._circular(coll)

    @staticmethod
    def _circular(points):
        while True:
            for point in points:
                yield point
        
    def update(self, delta):
        if delta != 0:
            self.offset = self.offset + 2/delta
        self.points = PentApp.genpoints(self.n, self.offset)

        for i in range(12):
            tildagonos.leds[i+1] = (int(255 * math.sin(self.offset)) , 0, 0)

        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The "off" pattern doesn't overwrite LEDs with (0,0,0) so we do just in case
            for i in range(12):
                tildagonos.leds[i+1] = (0, 0, 0)
            # The default pattern isn't re-enabled unless you enable it
            eventbus.emit(PatternEnable())
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()
        ctx.line_width = 5
        ctx.rgb(1,1,1).begin_path()
        for _ in range(0,self.n):
            this = next(self.points)
            next(self.points)
            that = next(self.points)
            ctx.move_to(this[X], this[Y])
            ctx.line_to(that[X], that[Y])

        ctx.stroke()
        
        ctx.restore()
        
__app_export__ = PentApp
