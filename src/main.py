import tello
import time
import pygame
import pygame.display
import pygame.key
import pygame.locals


controls = {
    "w": "forward",
    "s": "back",
    "a": "left",
    "d": "right",
    "e": "rotate",
    # arrow keys for fast turns and altitude adjustments
    "tab": lambda drone, speed: drone.takeoff(),
    "backspace": lambda drone, speed: drone.land(),
}


def run():
    drone = tello.TelloCommand(3)

    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1280, 720))

    speed = 30

    while True:
        time.sleep(0.1)
        for e in pygame.event.get():
            if e.type == pygame.locals.KEYDOWN:
                keyname = pygame.key.name(e.key)
                if keyname in controls:
                    key_handler = controls[keyname]
                    if type(key_handler) == str:
                        getattr(drone, key_handler)(speed)
                    else:
                        key_handler(drone, speed)
            elif e.type == pygame.locals.KEYUP:
                if keyname in controls:
                    key_handler = controls[keyname]
                    if type(key_handler) == str:
                        getattr(drone, key_handler)(0)
                    else:
                        key_handler(drone, 0)


if __name__ == "__main__":
    run()
