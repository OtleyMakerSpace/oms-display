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

To investigate:
- DPMI blanking
- automate the list of images
- samba share (need to be able to refresh the images)
- animation effects
- intelligent resize
