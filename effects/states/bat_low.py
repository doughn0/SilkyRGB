from ...colors import RED, AMBER
from ...effects._base_effect import BaseEffect
from ...device import Device
from ...utilities import dimm, easeOutQuart, mix, sin100, sin100_

_metadata = {
    'name': 'Battery Low',
    'reqs': [],
    'duration': 30
}

class Effect(BaseEffect):
    def __init__(self, dev: Device, initial_tick: int) -> None:
        super().__init__(dev, initial_tick)
        self.start_pct = int(self.dev.BATTERY['percentage'])
    
    def apply(self, t, palettes):

        pct = int(self.dev.BATTERY['percentage'] / self.start_pct * 100)

        fg = AMBER.fg

        t = t - self._TICK - 5

        bg = [0.6,0,0]

        if t < 0:
            self.dev.Raw.all([0,0,0])
        else:
            for z in self.dev.Z.Rings:
                _p = easeOutQuart((t) / 40) if t <= 30 else 1
                for x in range(z.COUNT):
                    td = _p * 400
                    if z.ANGLES[x] <= td - 40:
                        z[x] = bg
                    elif td - 40 <= z.ANGLES[x] < td:
                        __p = ((z.ANGLES[x] - td) / 40) % 1
                        z[x] = dimm(bg, 1-__p)
                    else:
                        z[x] = [0,0,0]

            if t >= 5:
                for z in self.dev.Z.Rings:
                    _p = easeOutQuart(((t-5)) / 60) * pct / 100 if t < 65 else pct / 100
                    for x in range(z.COUNT):
                        td = _p * 400
                        fg1 = dimm(fg, sin100_((t-6)*3 + int(z.ANGLES[x]/3.6))**10*0.6 + 0.4)
                        if z.ANGLES[x] <= td - 40:
                            z[x] = fg1
                        elif td - 40 <= z.ANGLES[x] < td:
                            __p = ((z.ANGLES[x] - td) / 40) % 1
                            z[x] = mix(fg1, 1-__p, bg, __p)
            
            for z in self.dev.Z.Leds:
                z.all(bg)
    
    def framekey(self, t):
        return None