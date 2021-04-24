###############################################################################
# Single: Toggle light
###############################################################################
# Script Parameters
button = data.get('button', '')
click = data.get('click', '')


def toggle_entity(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'toggle', service_data, False)


def turn_off(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'turn_off', service_data, False)

def activate_scene(hass, scene):
    service_data = {'entity_id': scene}
    hass.services.call('scene', 'turn_on', service_data, False)

if button == 'Room1 Button':
    if click == 'single':
        toggle_entity(hass, 'light', 'light.room_1_lights')
    elif click == 'double':
        # toggle_tv(hass)
        toggle_entity(hass, 'switch', 'switch.room1_tv')
    elif click == 'triple':
        service_data = {'entity_id': 'media_player.room_1_speaker',
                        'message': 'Setting lights to maximum brightness'}
        hass.services.call('tts', 'google_translate_say', service_data, False)
        activate_scene(hass, 'scene.room_1_white')
    elif click == 'quadruple':
        turn_off(hass, 'light', 'light.room_1_lights')
        turn_off(hass, 'switch', 'switch.room1_tv')
    elif click == 'long':
        hass.services.call('script', 'room1_good_night', {}, False)
elif button == 'Room2 Button1' or button == 'Room2 Button2':
    # Button 1
    if click == 'single' and button == 'Room2 Button1':
        toggle_entity(hass, 'light', 'light.room_2_lights')
    # Button 2
    elif click == 'single' and button == 'Room2 Button2':
        # Toggle Lamp 3 (with max brightness)
        light_states = hass.states.get('light.lamp_3')
        if light_states.state == 'off':
            service_data = {'entity_id': 'light.lamp_3',
                            'brightness': 255, 'color_temp': 153}
            hass.services.call('light', 'turn_on', service_data, False)
        else:
            service_data = {'entity_id': 'light.lamp_3'}
            hass.services.call('light', 'turn_off', service_data, False)
    elif click == 'double':
        toggle_entity(hass, 'fan', 'fan.xiaomi_fan')
    elif click == 'triple':
        service_data = {'entity_id': 'media_player.room_2_speaker',
                        'message': 'Activating night scene'}
        hass.services.call('tts', 'google_translate_say', service_data, False)
        activate_scene(hass, 'scene.night')
    elif click == 'quadruple':
        turn_off(hass, 'light', 'light.room_2_lights')
        turn_off(hass, 'fan', 'fan.xiaomi_fan')
    elif click == 'long':
        hass.services.call('script', 'room2_good_night', {}, False)
