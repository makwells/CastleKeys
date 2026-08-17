#animations.py 
from PySide6.QtCore import *

"""
    Interface animations. 
    Animations can be configured in the config file or in the settings. 
"""
class Animations:
    # startup window opening animation
    def startup_window_opening_animation(self, start_value, end_value, duration): 

        #if in config.toml startup_animations = true
        if self.config["view"]["window_startup_animations"]: 
            self.startup_anim = QPropertyAnimation(self, b"windowOpacity")
            self.startup_anim.setDuration(duration)                         #duration(ms)
            self.startup_anim.setStartValue(start_value)                    #start value 
            self.startup_anim.setEndValue(end_value)                        #end value
            self.startup_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)   #smooth
            self.startup_anim.start()                                       #start animation

        #if in config.toml startup_animations = false
        else: return 

    #TODO Добавить анимацию при переходе между менюшками, переход на главный экран итд. 