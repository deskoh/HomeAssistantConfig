###############################################################################
# Mi 6-button Switch
# Button Pair 1:
# - Single-Click: Turn off/on lights. Cycle lights if already on.
# - Double-Click: Cycle room scenes
# - Triple-Click: Turn on all lights
# - Hold: Set lights to max brightness and reset next scene cycle (so that double click selects 1st scene)
# Button Pair 2:
# - Single-Click: Toggle Fan
# - Double-Click: Cycle fan speed
# Button Pair 3:
# - Single-Click: Toggle TV
# - Double-Click: Cycle channels
# - Triple-Click: Turn on/off alarm
# - Hold: Turn off/on next alarm
###############################################################################

# Script Parameters
action = data.get('action', '')
light_group = data.get('light_group', 'group.room_1_lights')
input_scene = data.get('input_select_scene', 'input_select.room_1_scene')
input_alarm = data.get('input_alarm', 'input_boolean.room1_wakeup_dismiss')
speaker = data.get('speaker', 'media_player.room1_speaker')

def turn_on(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'turn_on', service_data, False)

def turn_off(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'turn_off', service_data, False)

def toggle_entity(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'toggle', service_data, False)

def tts(hass, speaker, message):
    service_data = {'entity_id': speaker, 'message': message, 'cache': 'false'}
    hass.services.call('tts', 'google_say', service_data, False)

light_states = hass.states.get(light_group)

if action == 'button_1_single':
    turn_off(hass, 'light', light_group)
elif action == 'button_2_single':
    if light_states.state == 'off':
        turn_on(hass, 'light', light_group)
    else:
        # Cycle lights
        light_group_states = hass.states.get(light_group)
        light_group_attr = light_group_states.attributes.copy()
        lights = light_group_attr['entity_id']
        light = lights[0]
        # Get next lights to turn on
        for i in range(len(lights)):
            l_states = hass.states.get(lights[i])
            if l_states.state == 'on':
                light = lights[(i + 1) % len(lights)]
                break
        # Turn off remaining lights
        for l in lights[0:]:
            # logger.warn(l + ' compare ' + light + str(light == l))
            if l == light: turn_on(hass, 'light', l)
            else: turn_off(hass, 'light', l)
elif action == 'button_1_double' or action == 'button_2_double':
    # Cycle room scenes
    scene = hass.states.get(input_scene).state
    turn_on(hass, 'scene', scene)

    service_data = {'entity_id': input_scene}
    hass.services.call('input_select', 'select_next', service_data, False)
elif action == 'button_2_triple':
    # Turn on all lights
    light_group_states = hass.states.get(light_group)
    light_group_attr = light_group_states.attributes.copy()
    lights = light_group_attr['entity_id']
    for l in lights[0:]:
        turn_on(hass, 'light', l)
elif action == 'button_2_hold':
    # Set lights to max brightness and reset next scene cycle
    service_data = {'entity_id': light_group, 'brightness': 255}
    hass.services.call('light', 'turn_on', service_data, False)

    scene_states = hass.states.get(input_scene)
    scene_attr = scene_states.attributes.copy()
    service_data = {
        'entity_id': input_scene,
        'option': scene_attr['options'][0]
    }
    hass.services.call('input_select', 'select_option', service_data, False)
elif action == 'button_3_single' or action == 'button_4_single':
    # Toggle Fan
    toggle_entity(hass, 'switch', 'switch.novita_fan')
elif action == 'button_3_double' or action == 'button_4_double':
    # Cycle fan speed
    if action == 'button_3_double': turn_off(hass, 'switch', 'switch.novita_fan_speed')
    else: turn_on(hass, 'switch', 'switch.novita_fan_speed')
elif action == 'button_5_single' or action == 'button_6_single':
    # Toggle TV
    toggle_entity(hass, 'switch', 'switch.room1_tv')
elif action == 'button_5_double' or action == 'button_6_double':
    # Cycle channels (TODO)
    action = 'select_next' if action == 'button_5_double' else 'select_previous'
    service_data = {'entity_id': 'input_select.room1_tv_channels'}
    hass.services.call('input_select', action, service_data, False)
elif action == 'button_5_triple' or action == 'button_6_triple':
    # Turn on/off alarm
    if action == 'button_5_triple': turn_off(hass, 'input_boolean', 'input_boolean.room1_wakeup_enabled')
    else: turn_on(hass, 'input_boolean', 'input_boolean.room1_wakeup_enabled')
    state = hass.states.get('input_boolean.room1_wakeup_enabled').state
    message = 'Alarm is {}!'.format(state)
    tts(hass, speaker, message)
elif action == 'button_5_hold' or action == 'button_6_hold':
    # Turn off/on next alarm
    if action == 'button_5_hold': turn_off(hass, 'input_boolean', input_alarm)
    else: turn_on(hass, 'input_boolean', input_alarm)
    state = hass.states.get(input_alarm).state
    message = 'Upcoming alarm is {}!'.format(state)
    tts(hass, speaker, message)
