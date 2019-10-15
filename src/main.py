import tello


def run():
    robot = tello.TelloCommand()
    robot_state = tello.TelloState()

    print("taking off")
    robot.takeoff()

    print("rotate and sleep")
    robot.rotate(180)

    print("do a little dance")
    robot.left(20)

    print("landing")
    robot.land()
    print(robot_state.recv_data())


if __name__ == "__main__":
    run()
