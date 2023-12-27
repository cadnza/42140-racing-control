from umath import floor
from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.tools import wait, StopWatch

# Initialize the hub, motors, and remote
hub = TechnicHub()
left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)
remote = Remote()

# Initialize stopwatch
sw = StopWatch()

# Set inactivity timeout
timeout_mins = 2
timeout_ms = timeout_mins * 60 * 1000

# Set speeds and speed index
speeds = [400, 800, 2000]
speed_index = 2  # TODO: Make this variable

# Set turn parameter ratio
turn_parameter_ratio = 2

# Set time elapse colors in descending order to time elapsed to inactivity
elapse_colors = [
	Color.WHITE,
	Color.VIOLET,
	Color.BLUE,
	Color.GREEN,
	Color.YELLOW,
	Color.ORANGE,
	Color.RED,
]

# Get buttons pressed
pressed = remote.buttons.pressed()

# Open program loop
while True:

	# Get previously pressed buttons
	pressed_previous = pressed
	pressed = remote.buttons.pressed()

	# Set speed variables
	working_speed = speeds[speed_index]
	speed_left = working_speed
	speed_right = working_speed

	# Set turn parameter
	turn_parameter = working_speed / turn_parameter_ratio

	# Parse steering buttons
	# No change
	if pressed == pressed_previous:
		pass
	# Both forward and reverse pressed
	elif Button.LEFT_PLUS in pressed and Button.LEFT_MINUS in pressed:
		pass
	# Forward pressed
	elif Button.LEFT_PLUS in pressed:
		# Left turn pressed
		if Button.RIGHT_PLUS in pressed:
			speed_left -= turn_parameter
			speed_right += turn_parameter
		# Right turn pressed
		if Button.RIGHT_MINUS in pressed:
			speed_left += turn_parameter
			speed_right -= turn_parameter
		# Commit
		left_motor.run(speed_left)
		right_motor.run(speed_right)
	# Reverse pressed
	elif Button.LEFT_MINUS in pressed:
		# Left turn pressed
		if Button.RIGHT_PLUS in pressed:
			speed_left -= turn_parameter
			speed_right += turn_parameter
		# Right turn pressed
		if Button.RIGHT_MINUS in pressed:
			speed_left += turn_parameter
			speed_right -= turn_parameter
		# Commit
		left_motor.run(-speed_left)
		right_motor.run(-speed_right)
	# Neither forward or backward pressed
	else:
		# Both or neither of left turn and right turn pressed
		if (Button.RIGHT_PLUS in pressed and Button.RIGHT_MINUS in pressed) or (Button.RIGHT_PLUS not in pressed and Button.RIGHT_MINUS not in pressed):
			left_motor.brake()
			right_motor.brake()
		# Left turn pressed
		if Button.RIGHT_MINUS in pressed:
			left_motor.run(turn_parameter)
			right_motor.run(-turn_parameter)
		# Right turn pressed
		if Button.RIGHT_PLUS in pressed:
			left_motor.run(-turn_parameter)
			right_motor.run(turn_parameter)

	# Color lights on vehicle and remote according to timeout
	index_current_timeout_color = floor(
		sw.time() / (timeout_ms / len(elapse_colors))
	)
	hub.light.on(elapse_colors[index_current_timeout_color])
	remote.light.on(elapse_colors[index_current_timeout_color])

	# Shut down on timeout
	if pressed:
		sw.reset()
	if sw.time() > timeout_ms:
		hub.system.shutdown()

	# Be nice to the CPU
	wait(10)
