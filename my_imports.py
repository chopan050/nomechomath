from manim import ReplacementTransform, ValueTracker, tempconfig, XKCD

RT = ReplacementTransform

class VT(ValueTracker):
    def __invert__(self):
        return self.get_value()

    def __lshift__(self, other):
        return self.animate.set_value(other)

config = {
    "preview": True,
    "frame_rate": 60,
    "pixel_width": 1080,
    "pixel_height": 1920,
    "background_color": XKCD.MAIZE,
    # "disable_caching": True,
}

def render(scene_class):
    with tempconfig(config):
        scene_class().render()

def get_dims(scene):
    return scene.camera.frame_height, scene.camera.frame_width