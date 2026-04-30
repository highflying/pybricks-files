from pybricks.hubs import CityHub
from pybricks.pupdevices import Remote, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait
from uerrno import ENODEV, ETIMEDOUT

# ---------------------------------------------------------------------------
# COLOUR SENSOR SETTINGS
# ---------------------------------------------------------------------------
# These values define the range of colours the sensor will recognise as a
# "station marker" — e.g. a strip of teal/coloured tiles on the track.
# Colour is described using HSV (Hue, Saturation, Value):
#   Hue (h)        — the colour itself, as a number from 0–360 (e.g. 170–200 is teal)
#   Saturation (s) — how vivid the colour is, 0 (grey) to 100 (pure colour)
#   Value (v)      — brightness, 0 (black) to 100 (full brightness)
#
# If the sensor keeps missing your marker, widen the ranges.
# If it triggers on the wrong colours, narrow them.
# Set debug_colour = True (below) to print live readings while the train runs.
class SensorColour:
    min_h = 170   # Minimum hue   — currently tuned for teal
    max_h = 200   # Maximum hue
    min_s = 80    # Minimum saturation (fairly vivid)
    max_s = 100   # Maximum saturation
    min_v = 50    # Minimum brightness
    max_v = 76    # Maximum brightness

# ---------------------------------------------------------------------------
# TIMING SETTINGS  (all values are in milliseconds, 1000 ms = 1 second)
# ---------------------------------------------------------------------------
stop_interval = 5000       # How long the train pauses at a station (5 seconds)
continue_interval = 2000   # Extra wait after leaving a station before checking buttons again (2 seconds)
                           # this is so the train has a chance to move away from
                           # the coloured tiles it is likely to be over

# ---------------------------------------------------------------------------
# REMOTE CONTROLLER SETTINGS
# ---------------------------------------------------------------------------
# hub_name must exactly match the Bluetooth name of your Powered Up remote.
# controller_timeout is how long (in ms) the hub will wait while trying to
# connect to the remote before giving up and running without it.
#
# - Using a named remote stops someone else's remote from connecting to your train
# - You can rename hubs using the LEGO Powered Up app
hub_name = 'bercont'
controller_timeout = 10000  # 10 seconds

# ---------------------------------------------------------------------------
# DEBUG / DEVELOPMENT OPTIONS
# ---------------------------------------------------------------------------
# Set debug_colour to True to print the raw HSV colour reading every loop tick.
# Useful for working out the right SensorColour ranges for a new marker colour.
# Set back to False for normal operation.
#
# This is only worth setting whem the hub is connected to the Pybricks UI where
# you can see the output
debug_colour = False


# ---------------------------------------------------------------------------
# TRAIN HUB  — the main logic for the train
# ---------------------------------------------------------------------------
# This class manages the motor, the remote controller, and the colour sensor.
# It is created once at the bottom of the file and then its run() method is
# called repeatedly in a loop.
class TrainHub(object):
    def __init__(self):
        self._hub = CityHub()
        self._remote = None
        self.connect_remote()  # Try to pair with the remote on startup

        self._motor = DCMotor(Port.A)  # Motor must be plugged into Port A
        self.has_sensor = False        # Assume no sensor until we detect one
        self.position = 0              # Counts sensor triggers (used for station detection)
        self.stop_at_station = False   # Whether station-stopping is enabled (toggled via remote)

        # Try to connect the colour sensor on Port B.
        # If nothing is plugged in, the train simply runs without station detection.
        try:
            self._sensor = ColorDistanceSensor(Port.B)
            self.has_sensor = True
        except OSError as ex:
            if ex.errno == ENODEV:
                print('No colour sensor')
            else:
                raise RuntimeError

        # Start with the motor off.
        # If the remote connected, wait for the driver to press a button.
        # If no remote, start moving immediately using the last set power level.
        self.power = 0
        if self.remote_connected:
            self.stop()
        else:
            self.start()

    def connect_remote(self):
        """Try to pair with the Powered Up remote. Sets remote_connected accordingly."""
        try:
            self._remote = Remote(name=hub_name, timeout=controller_timeout)
            self.remote_connected = True
            self._hub.light.on(Color.GREEN)       # Hub light green = connected
            self._remote.light.on(Color.GREEN)    # Remote light green = connected
        except OSError as ex:
            if ex.errno == ETIMEDOUT:
                # Remote not found within the timeout — continue without it
                print('Unable to reconnect to remote')
                self.remote_connected = False
                self._hub.light.on(Color.RED)     # Hub light red = no remote
            else:
                raise RuntimeError

    def set_led_colour(self, led_colour):
        """Set the light colour on both the hub and the remote (if connected)."""
        self._hub.light.on(led_colour)
        try:
            if self._remote is not None:
                self._remote.light.on(led_colour)
        except OSError as ex:
            if ex.errno == ENODEV:
                # Remote has been disconnected since we last checked
                self.remote_connected = False
            else:
                raise RuntimeError

    def stop(self):
        """Stop the motor and set lights to red."""
        self._motor.stop()
        self.set_led_colour(Color.RED)

    def start(self):
        """Run the motor at the current power level and update the lights.
        Green = forward, Blue = reverse, Red = stopped (power 0).
        """
        self._motor.dc(self.power)
        if self.power > 0:
            self.set_led_colour(Color.GREEN)
        elif self.power == 0:
            self.set_led_colour(Color.RED)
        else:
            self.set_led_colour(Color.BLUE)

    def pause_at_station(self):
        """Stop the train for stop_interval ms, then resume.
        If the remote has disconnected, try to reconnect while stopped.
        """
        self.stop()
        wait(stop_interval)   # Sit at the station
        self.start()          # Move off again
        if not self.remote_connected:
            # Use the station stop as an opportunity to re-pair with the remote
            self.connect_remote()
        else:
            wait(continue_interval)  # Brief extra pause before resuming button checks

    def run(self):
        """Called every 100 ms. Reads the remote buttons and checks the colour sensor."""

        # --- Remote control ---
        if self.remote_connected:
            try:
                if self._remote is not None:
                    pressed = self._remote.buttons.pressed()

                    # LEFT side buttons control speed WITH station stopping enabled.
                    # RIGHT side buttons control speed WITHOUT station stopping.
                    if Button.LEFT_PLUS in pressed:
                        self.stop_at_station = True
                        if self.power < 100:
                            self.power = self.power + 10  # Speed up (forward)
                        self.start()
                    elif Button.LEFT_MINUS in pressed:
                        self.stop_at_station = True
                        if self.power > -100:
                            self.power = self.power - 10  # Slow down / reverse
                        self.start()
                    elif Button.LEFT in pressed or Button.RIGHT in pressed:
                        # Centre button on either side = emergency stop
                        self.power = 0
                        self.stop()
                    elif Button.RIGHT_PLUS in pressed:
                        self.stop_at_station = False
                        if self.power < 100:
                            self.power = self.power + 10  # Speed up, bypass stations
                        self.start()
                    elif Button.RIGHT_MINUS in pressed:
                        self.stop_at_station = False
                        if self.power > -100:
                            self.power = self.power - 10  # Slow down, bypass stations
                        self.start()

            except OSError as ex:
                if ex.errno == ENODEV:
                    # Remote disconnected mid-run
                    self.remote_connected = False
                else:
                    raise RuntimeError

        # --- Colour sensor / station detection ---
        # Only active when a sensor is fitted AND station stopping is turned on.
        if self.has_sensor and self.stop_at_station:
            colour = self._sensor.hsv()

            if debug_colour:
                print(colour)  # Prints H, S, V values — useful for tuning SensorColour

            # Check whether the reading falls within the defined colour range
            if ( colour.h >= SensorColour.min_h
                and colour.h <= SensorColour.max_h
                and colour.s >= SensorColour.min_s
                and colour.s <= SensorColour.max_s
                and colour.v >= SensorColour.min_v
                and colour.v <= SensorColour.max_v ):

                self.position = self.position + 1

                # position counts consecutive matching readings.
                # Triggering on 1 means the train stops as soon as the marker is seen.
                if self.position == 1:
                    self.pause_at_station()
                    self.position = 0  # Reset so it can trigger again next time


# ---------------------------------------------------------------------------
# STARTUP
# ---------------------------------------------------------------------------
# Create the train (connects to remote, sets up motor and sensor) then loop forever.
train = TrainHub()

while True:
    train.run()
    wait(100)  # Wait 100 ms between each check (~10 times per second)
