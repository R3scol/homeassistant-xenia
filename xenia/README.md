# Xenia Home Assistant Integration (enhanced)

**Preconfigured for your machine IP:** 192.168.50.3

## Features
- Power switch
- Eco Mode switch
- Steam Mode switch
- Sensors: Brew group temp, Brew set temp, Boiler temp, Pump pressure, Steam/Boiler pressure, Status
- Execute Xenia scripts via service
- Lovelace dashboard included
- iPhone notify placeholder (see instructions)

## Installation (local)
1. Unzip into `/config/custom_components/xenia/`
2. Restart Home Assistant
3. Integrations → Add Integration → Xenia → enter IP `192.168.50.3`

## Notification (iPhone)
Replace `notify.TODO_MOBILE_APP` in automations with your mobile app notify service (e.g. notify.mobile_app_john_s_iphone)

## Steam Mode
Steam mode controls the steam boiler output. Use the Steam switch to enable/disable the steam function.
