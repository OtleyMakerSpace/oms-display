# Otley Maker Space "attract" display

Displays a slide show of images during the day. Blanks the screen at night.

Image file names are currently hard-coded, 5 images, but easy to add/remove images.

---

Hostname: `display-pi`

GitHub repository: https://github.com/DavidFrankland/oms-display

Document:
- how to connect
- how to edit the image list

## Startup

in file `~/.config/autostart/oms-display.desktop`

```
[Desktop Entry]
Type=Application
Name=oms-display
Exec=/home/pi/oms-display.sh
```

## Configuration

in file `~/oms-display/settings.ini`

```
[settings]

# whether to switch off the display hardware for blanking the screen
enable blanking = true

# how long (in seconds) each slide is displayed
slide time = 10

# the start hour, when slides will begin to be displayed (0-23)
# the start hour can be after the end hour, if you want a display that runs after midnight
start hour = 8

# the end hour, when a blank screen will be shown (0-23)
end hour = 22
```

To investigate:
- DPMI blanking
- automate the list of images
- samba share (need to be able to refresh the images)
- animation effects
- intelligent resize
