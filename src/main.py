import tello
import udpserver
import time
import pygame
import pygame.display
import pygame.key
import pygame.locals


controls = {
    "w": "rc_forward",
    "s": "rc_backward",
    "a": "rc_left",
    "d": "rc_right",
    "e": "rc_rotatec",
    "r": "rc_rotateq",
    "f": "rc_up",
    "g": "rc_down",
    "tab": lambda robot, speed: robot.takeoff(),
    "backspace": lambda robot, speed: robot.land(),
}


def run():
    robot = tello.TelloCommand(3)

    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1280, 720))

    statsdata = udpserver.UDPServer(8890)
    statsdata.recv_start()

    speed = 30

    while True:
        time.sleep(0.5)
        new_stats = statsdata.data
        if new_stats != udpserver.EMPTY:
            print(new_stats)

        for e in pygame.event.get():
            if e.type == pygame.locals.KEYDOWN:
                keyname = pygame.key.name(e.key)
                if keyname in controls:
                    key_handler = controls[keyname]
                    if type(key_handler) == str:
                        getattr(robot, key_handler)(speed)
                    else:
                        key_handler(robot, speed)
            elif e.type == pygame.locals.KEYUP:
                if keyname in controls:
                    key_handler = controls[keyname]
                    if type(key_handler) == str:
                        getattr(robot, key_handler)(0)
                    else:
                        key_handler(robot, 0)


if __name__ == "__main__":
    run()
