# Otley Maker Space "attract" display

Displays a slide show of images during the day. Blanks the screen at night.

Uses [GL Transitions](https://gl-transitions.com/) for nice transition effects between images. Available GL Transitions gallery is [here](https://gl-transitions.com/gallery)


Displays [Wharfedale Men's Shed](https://wharfedalemensshed.org.uk/) images on Mondays (except bank holidays (configurable)), Otley Maker Space images on other days.

Downloads the bank holidays from https://www.gov.uk/bank-holidays if needed.

Optionally publishes MQTT messages which specify which set of daily images is being displayed. This is used to sync the RGB LED matrix display theme to this one.

The slide show runs on a Raspberry Pi, which reboots at the end of the night.

---

Hostname: `display-pi`

GitHub repository: https://github.com/OtleyMakerSpace/oms-display

## Startup

in file `~/.config/autostart/oms-display.desktop`

```ini
[Desktop Entry]
Type=Application
Name=oms-display
Exec=/home/pi/oms-display.sh
```

## Configuration

Settings are stored in the file `settings.ini`. An example looks like:

```ini
[settings]
enable-blanking = true
slide-time = 10
transition-time = 1.5
start-hour = 8
end-hour = 22
enable-reboot = false
handle-bank-holidays = false
oms-images-folder = oms-images
wms-images-folder = wms-images

[mqtt]
enable = true
host = localhost
```

The `[settings]` section contains global settings:

**enable-blanking** (true/false): Whether to switch off the display during the blank period. If this is true, the display will enter a standby mode to save power.

**slide-time**: How long (in seconds) each slide is displayed.

**transition-time**: The duration of the transition between slides

**start-hour** (0-23): The hour of the day when slides will begin to be displayed, e.g. setting this to `8` will start the slide show at 8:00.

**end-hour** (0-23): The hour of the day when the slide show stops and a blank screen is displayed, e.g. setting this to `22` will end the slide show at 22:00.

It is possible to set the start hour later than the end hour if you would like a display that runs beyond midnight, e.g. setting the start hour to `22` and the end hour to `2` will display the slide show from 22:00 to 2:00.

**enable-reboot** (true/false): Whether to reboot at the end of the night.

**handle-bank-holidays** (true/false): Whether to account for bank holidays on Mondays. If this is true, Mondays are treated as Wharfedale Men's Shed days only if it is not a bank holiday. If false, all Mondays are Wharfedale Men's Shed days.

**oms-images-folder**: The folder where the Otley Maker Space images are stored. Ensure that only image files are in here. The images in this folder will be displayed in the order of their filenames (sorted alphabetically).

**wms-images-folder**: The folder where the Wharfedale Men's Shed images are stored.

The `[mqtt]` section contains MQTT-specific settings:

**enable** (true/false): Whether to publish MQTT messages for updating the LED matrix display.

**host**: The MQTT broker to use.


## To do

Document:
- how to connect
- image file format (1680x1050, PGM, PPM, GIF, PNG format)

Investigate:
- samba share (need to be able to refresh the images)
- intelligent resize/zoom
