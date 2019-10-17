import tello
import udpserver
import time
import pygame
import pygame.display
import pygame.key
import pygame.locals

SPEED = 30

controls = {
    "w": lambda robot, speed: robot.rc_forward(speed),
    "s": lambda robot, speed: robot.rc_backward(speed),
    "a": lambda robot, speed: robot.rc_left(speed),
    "d": lambda robot, speed: robot.rc_right(speed),
    "left": lambda robot, speed: robot.rc_rotatec(speed),
    "right": lambda robot, speed: robot.rc_rotateq(speed),
    "up": lambda robot, speed: robot.rc_up(speed),
    "down": lambda robot, speed: robot.rc_down(speed),
    "e": lambda robot, speed: adjust_speed(10),
    "q": lambda robot, speed: adjust_speed(-10),
    "tab": lambda robot, speed: robot.takeoff(),
    "backspace": lambda robot, speed: robot.land(),
    "r": lambda robot, speed: robot.streamon(),
    "t": lambda robot, speed: robot.flip("f"),
    "y": lambda robot, speed: robot.flip("b"),
}


def adjust_speed(n: int):
    global SPEED
    SPEED += n
    print("speed is {}".format(SPEED))


def run():
    global SPEED

    robot = tello.TelloCommand(3)

    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1280, 720))

    statsdata = udpserver.UDPServer(8890)
    statsdata.recv_start()

    videodata = udpserver.UDPServer(11111)
    videodata.recv_start()

    while True:
        time.sleep(0.5)
        new_stats = statsdata.data
        if new_stats != udpserver.EMPTY:
            print(new_stats)

        for e in pygame.event.get():
            if e.type == pygame.locals.KEYDOWN:
                keyname = pygame.key.name(e.key)
                if keyname in controls:
                    controls[keyname](robot, SPEED)
            elif e.type == pygame.locals.KEYUP:
                if keyname in controls:
                    key_handler = controls[keyname]
                    controls[keyname](robot, 0)


if __name__ == "__main__":
    run()
