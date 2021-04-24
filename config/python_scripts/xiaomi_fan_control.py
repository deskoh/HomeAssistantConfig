# Script Parameters
fan = data.get('fan', '')
input_id = data.get('input_id', '')
state = data.get('state', '')
speed_input = data.get('speed_input', 'input_number.room2_fan_speed')

if input_id.endswith('fan_speed'):
    service_data = {'entity_id': fan, 'speed': int(float(state))}
    hass.services.call('fan', 'set_speed', service_data, False)
elif input_id.endswith('swing_angle'):
    service_data = {'entity_id': fan, 'angle': int(state)}
    hass.services.call(
        'fan', 'xiaomi_miio_set_oscillation_angle', service_data, False)
elif input_id.endswith('natural_mode'):
    service_data = {'entity_id': fan}

    if state == 'on':
        service_name = 'xiaomi_miio_set_natural_mode_on'
    else:
        service_name = 'xiaomi_miio_set_natural_mode_off'
    hass.services.call('fan', service_name, service_data, False)

    # Sync speed
    speed = int(float(hass.states.get(speed_input).state))
    service_data = {'entity_id': fan, 'speed': speed}
    hass.services.call('fan', 'set_speed', service_data, False)
