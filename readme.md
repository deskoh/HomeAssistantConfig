# [Home Assistant](https://www.home-assistant.io/) Configuration

> HA Version: 0.90.1

## Automations

| Name                 | Trigger  | Description   |
|----------------------|----------|---------------|
| Sunrise Routine      | Sunrise  | Disable motion detection automations and sets room status to _Awake_ |
| Sunset Routine       | Sunset   | Enable motion detection automations |
| Bedtime Routine      | 23:00    | Sets room status to _Sleeping_ |
| Room 1 Wakeup Lights | Template | Trigger wake-up lights script and turn off _Dismiss Next Wake-up_ input boolean.
| Room 2 Wakeup Lights | Template | Same as _Room 1 Wakeup Lights_ but for Room 2.|
| Room 1 Switch        | Hue Dimmer Switch | Trigger Python script for Hue Dimmer Switch. |
| Room 2 Switch        | Hue Dimmer Switch | Same as _Room 1 Switch_ but for Room 2. |
| Room 1 Button        | Xiaomi Wireless Switch | Trigger Python script for Button Switch. |
| Room 2 Button 1      | Xiaomi Wireless Switch | Same as _Room 1 Switch_ but for Room 2 Button 1. |
| Room 2 Button 2      | Xiaomi Wireless Switch | Same as _Room 1 Switch_ but for Room 2 Button 2. |
| Room 1 Switch Good Morning | Hue Dimmer Switch | Trigger _Room 1 Good Morning_ script if Room Status is _Sleeping_ and less than 2 hours before sunrise. |
| Room 2 Switch Good Morning | Hue Dimmer Switch | Trigger _Room 2 Good Morning_ script if Room Status is _Sleeping_ and less than 2 hours before sunrise. |
| Cuckoo Clock         | Hourly and Half-hourly | Simulate cuckoo clock chimes using Google Home Mini between 0900 and 2130 and if Room Status is _Awake_ and _deskoh_ is home |
| Room 2 Fan Inputs    | UI Components | Trigger _Xiaomi Fan Control_ Python script for fan control based on UI Components inputs |
| Room 1 TV Channels   | UI Components | Trigger TV Channel change using RM Mini 3 based on UI Components inputs |
| Room 1 Motion Lights | Motion Sensor | Trigger lights if motion is detected. |
| Room 2 Motion Lights | Motion Sensor | Similar to _Room 1 Motion Lights_ but for Room 2. |
| Evening Lights | Contact Sensor | Turn on Room 2 lights until no motion detected. |

### Utility Automations

| Name | Description   |
|------|---------------|
| Let's Encrypt Renewal| Renew Let's Encrypt SSL Certs
| Enable Zigbee joining | Enable new Zigbee devices to join

## Scripts
| Name                 | Trigger  | Description   |
|----------------------|----------|---------------|
| Blink Light          | Android (Tasker)  | Blink lights if message received on phone. |
| Wake Up Lights       | Wake Up Automation  | Fades in lights and play alarm. |
| Good Morning         | Room Good Morning Scripts | Turn on lights, switches off fan and dismisses upcoming Wake Up lights and sets Room Status to _Awake_ |
| Room 1 Good Morning  | Good Morning Automation | Trigger Good Morning script for Room 1 |
| Room 2 Good Morning  | Good Morning Automation | Trigger Good Morning script for Room 2 |
| Good Night           | Google Home Trigger Phrase (IFTTT) | Fades out lights, says random good night phrases, sets Room Status to _Sleeping_ |
| Room 1 Good Night  | Good Night Automation | Trigger Good Night script for Room 1 |
| Room 2 Good Night  | Good Night Automation | Trigger Good Night script for Room 2 |
| 7min Workout       | Plays 7 minute workout prompt on Google Home |

## Devices

### Main Room

* Xiaomi BLE Temperature and Humidity Sensor LYWSDCGQ/01ZM
* [Xiaomi Roborock S5](en.roborock.com)
* Xiaomi Door & Window Contact Sensor MCCGQ01LM

### Room 1

* 2 x Philips Hue Color Lamp LCT007
* Yeelight LED Light Strip YLDD02YL
* Yeelight LED Light Strip YLDD04YL with Extension
* Philips Hue Dimmer Switch RWL020
* Xiaomi Motion Sensor RTCGQ11LM
* Xiaomi Temperature and Humidity Sensor WSDCGQ11LM
* Xiaomi Wireless Switch WXKG01LM
* Broadlink RM Mini 3
* Google Home Mini

### Room 2

* Philips Hue Color Lamp LCT007
* Philips Hue Dimmer Switch RWL021
* Philips Hue White Lamp LWB014
* Xiaomi Motion Sensor RTCGQ11LM
* Xiaomi Temperature and Humidity Sensor WSDCGQ11LM
* Xiami DC Inverter Stand Fan (SA1) ZLBPLDS02ZM
* 2 x Xiaomi Wireless Switch WXKG01LM
* Google Home Mini

## References

[zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt)

[Hass.io Add-on: zigbee2mqtt](https://github.com/danielwelch/hassio-zigbee2mqtt)

[Hue Dimmer Custom Component](https://github.com/robmarkcole/Hue-sensors-HASS)

[Xiaomi Fan Component](https://github.com/syssi/xiaomi_fan)

https://github.com/CCOSTAN/Home-AssistantConfig
