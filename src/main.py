import tello


def run():
    robot = tello.TelloCommand()

    print("taking off")
    robot.takeoff()

    print("rotate and sleep")
    robot.rotate(180)

    print("do a little dance")
    robot.left(20)

    print("landing")
    robot.land()


if __name__ == "__main__":
    run()
