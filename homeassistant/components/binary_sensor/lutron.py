"""
Support for binary sensor using RPi GPIO.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.lutron/
"""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDevice, DOMAIN, PLATFORM_SCHEMA)
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.components.lutron import (
    LutronDevice, LUTRON_DEVICES, LUTRON_GROUPS, LUTRON_CONTROLLER)

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup Lutron Pico Remotes."""
    area_devs = {}
    devs = []
    for (area_name, device) in hass.data[LUTRON_DEVICES]['binary_sensor']:
        dev = LutronPicoButton(hass, area_name, device, hass.data[LUTRON_CONTROLLER])
        area_devs.setdefault(area_name, []).append(dev)
        devs.append(dev)
    add_devices(devs, True)

    for area in area_devs:
        if area not in hass.data[LUTRON_GROUPS]:
            continue
        grp = hass.data[LUTRON_GROUPS][area]
        ids = list(grp.tracking) + [dev.entity_id for dev in area_devs[area]]
        grp.update_tracked_entity_ids(ids)

    return True

class LutronPicoButton(LutronDevice, BinarySensorDevice):
    """Representation of a Lutron Pico Remote Button"""

    def __init__(self, hass, area_name, lutron_device, controller):
        """Initialize the remote."""
        self._prev_button_state = 0;
        LutronDevice.__init__(self, hass, DOMAIN, area_name, lutron_device,
                              controller)

#    @property
#    def device_state_attributes(self):
#        """Return the state attributes."""
#        attr = {}
#        attr['Lutron Integration ID'] = self._lutron_device.id
#        return attr

    @property
    def is_on(self):
        """Return true if device is on."""
        return bool(self._lutron_device.pressed)

    def update(self):
        """Called when forcing a refresh of the device."""
        if self._prev_button_state is None:
            self._prev_button_state = self._lutron_device.pressed
