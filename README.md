# Otley Maker Space "attract" display

Displays a slide show of images during the day. Blanks the screen at night.

Uses [GL Transitions](https://gl-transitions.com/) for nice transition effects between images. Available GL Transitions gallery is [here](https://gl-transitions.com/gallery)

On Mondays (except bank holidays (configurable)), displays [Wharfedale Men's Shed](https://wharfedalemensshed.org.uk/) images.

On the last Sunday of the month (can be disabled), displays [Repair Café](https://www.repaircafe.org/en/cafe/leeds-repair-cafe-network/) images.

Displays Otley Maker Space images on other days.

Downloads the bank holidays from https://www.gov.uk/bank-holidays if needed.

Optionally publishes MQTT messages which specify which "theme" is being used. This is used to sync the RGB LED matrix display theme to this one.

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
Exec=/home/pi/oms-display/start.sh
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
enable-repair-cafe = true
images-folder = images
override-theme = 
oms-theme = oms
wms-theme = wms
repair-cafe-theme = repair-cafe

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

**enable-repair-cafe** : Whether to show the Repair Café images on the last Sunday of the month. Set this to false if we are not doing a Repair Café this month.

**images-folder**: The base folder where the images are stored. Contains subfolders for the various image themes.

**override-theme**: Use this to override the daily theme for testing porposes. Leave blank for normal functionality.

**oms-theme**: The theme and subfolder name for Otley Maker Space images.

**wms-theme**: The theme and subfolder name for Wharfedale Men's Shed images.

**repair-cafe-theme**: The theme and subfolder name for Repair Café images.

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
