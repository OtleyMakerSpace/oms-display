# Otley Maker Space "attract" display

Displays a slide show of images during the day. Blanks the screen at night.

The slide show runs on a Raspberry Pi, which reboots at midnight.

---

Hostname: `display-pi`

GitHub repository: https://github.com/DavidFrankland/oms-display

## Startup

in file `~/.config/autostart/oms-display.desktop`

```
[Desktop Entry]
Type=Application
Name=oms-display
Exec=/home/pi/oms-display.sh
```

## Configuration

Settings are stored in the file `~/oms-display/settings.ini`. An example looks like:

```
[settings]
enable-blanking = true
slide-time = 10
start-hour = 8
end-hour = 22
images-folder = images
```

**enable-blanking** (true/false): Whether to switch off the display during the blank period. If this is set, the display will enter a standby mode to save power.

**slide-time**: How long (in seconds) each slide is displayed.

**start-hour** (0-23): The hour of the day when slides will begin to be displayed, e.g. setting this to `8` will start the slide show at 8:00.

**end-hour** (0-23): The hour of the day when the slide show stops and a blank screen is displayed, e.g. setting this to `22` will end the slide show at 22:00.

It is possible to set the start hour later than the end hour if you would like a display that runs beyond midnight, e.g. setting the start hour to `22` and the end hour to `2` will display the slide show from 22:00 to 2:00.

**images-folder**: The folder where the images are stored. Ensure that only image files are in here. The images in this folder will be displayed in the order of their filenames (sorted alphabetically).

## To do

Document:
- how to connect

Investigate:
- DPMI blanking ([see here](https://raspberrypi.stackexchange.com/questions/59898/how-can-i-blank-the-screen-from-the-command-line-over-ssh))
- display different images for Wharfedale Men's Shed on Mondays
- samba share (need to be able to refresh the images)
- animation effects ([GL Transitions](https://gl-transitions.com/)?)
- intelligent resize/zoom
