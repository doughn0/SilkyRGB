#!/bin/bash

# Determine python site-package folder
PYTHON_PATH=$(python -c "import sys; print('\n'.join(sys.path))" | grep site-packages)
SILKY_RGB_PATH="$PYTHON_PATH/silkyrgb"

# Remove a previous installation of Silky RGB
if [ -d "$SILKY_RGB_PATH" ]; then
  echo "Removing previous Silky RGB installation from $SILKY_RGB_PATH"
  rm -Rf $SILKY_RGB_PATH;
fi

# Install Silky RGB
echo "Installing Silky RGB in $SILKY_RGB_PATH"

mkdir $SILKY_RGB_PATH
cp ../*.py               $SILKY_RGB_PATH
cp -r ../__pycache__     $SILKY_RGB_PATH
cp -r ../device_configs  $SILKY_RGB_PATH
cp -r ../drivers         $SILKY_RGB_PATH
cp -r ../effects         $SILKY_RGB_PATH

chmod +x "$SILKY_RGB_PATH"/*.py
chmod +x "$SILKY_RGB_PATH"/drivers/*.py
chmod +x "$SILKY_RGB_PATH"/effects/*.py
chmod +x "$SILKY_RGB_PATH"/effects/modes/*.py
chmod +x "$SILKY_RGB_PATH"/effects/notifications/*.py

# Remove legacy Knulli RGB if it is still present to avoid any conflicts
if [ -f /etc/init.d/S28rgbled ]; then
  echo "Shutting down legacy RGB service"
  /etc/init.d/S28rgbled stop
  echo "Removing legacy RGB service"
  rm -f /etc/init.d/S28rgbled
fi

if [ -f /etc/init.d/S28rgbled ]; then
echo "Removing legacy RGB control"
  rm -f /usr/bin/knulli-rgb-led
fi

if [ -f /etc/init.d/S28rgbled ]; then
  echo "Removing legacy RGB daemon"
  rm -f /usr/bin/knulli-rgb-led-daemon
fi

if [ -f /usr/share/emulationstation/scripts/achievements/led.sh ]; then
  echo "Removing legacy RGB led hook"
  rm -f /usr/share/emulationstation/scripts/achievements/led.sh
fi

# Remove a previous version of the Silky RGB service
if [ -f /etc/init.d/S98rgbled ]; then
  echo "Shutting down previous Silky RGB service"
  /etc/init.d/S98rgbled stop
  echo "Removing previous Silky RGB service"
  rm -f /etc/init.d/S98rgbled
fi

# Install the Silky RGB service
cp ./S98rgbled /etc/init.d/S98rgbled
chmod +x /etc/init.d/S98rgbled
echo "Installed Silky RGB service at /etc/init.d/S98rgbled"

# Remove a previous version of the Silky RGB launch command
if [ -f /usr/bin/knulli-rgb ]; then
  echo "Removing previous Silky RGB launch command"
  rm -f /usr/bin/knulli-rgb
fi

# Install the Silky RGB service
cp ./knulli-rgb /usr/bin/knulli-rgb
chmod +x /usr/bin/knulli-rgb
echo "Installed Silky RGB launch command at /usr/bin/knulli-rgb"

# Install the Silky RGB hook
if [ -f /usr/share/emulationstation/scripts/achievements/rgb.sh ]; then
  echo "Removing previous RGB led hook"
  rm -f /usr/share/emulationstation/scripts/achievements/rgb.sh
fi

cp ./rgb.sh /usr/share/emulationstation/scripts/achievements/rgb.sh

knulli-save-overlay

echo "Launching Silky RGB service"
/etc/init.d/S98rgbled start