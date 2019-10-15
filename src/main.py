import tello
import time


def run():
    robot = tello.TelloCommand()
    robot_state = tello.TelloState()

    print(robot_state.recv())

    print("taking off")
    robot.takeoff()
    time.sleep(5)
    print(robot_state.recv())

    print("rotate and sleep")
    robot.rotate(180)
    time.sleep(5)
    print(robot_state.recv())

    print("landing")
    robot.land()
    time.sleep(1)
    print(robot_state.recv())


if __name__ == "__main__":
    run()
