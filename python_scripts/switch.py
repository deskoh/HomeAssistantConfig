###############################################################################
# Hue Dimmer Switch
# Button 1:
# - If lights off, turn on lights.
# - If lights on, cycle room scenes
# - If hold, set all lights to max brightness and reset next scene cycle (so that next click selects 1st scene)
# Button 2:
# - If lights on, click or hold to increase brightness
# - Else increase fan speed, hold to toggle oscillation
# Button 3:
# - If lights on, click or hold to decrease brightness
# - Else decrease fan speed, hold to toggle natural mode
# Button 4:
# - Turn off lights if on, else announce time.
# - If hold, toggle upcoming alarm if lights on, else turn off fan.
###############################################################################
# Script Parameters
switch_entity = data.get('switch_entity', 'sensor.bedroom_1_switch')
input_scene = data.get('input_select_scene', 'input_select.room_1_scene')
input_alarm = data.get('input_alarm', 'input_boolean.room1_wakeup_dismiss')
light_group = data.get('light_group', 'group.room_1_lights')
fan_inputs = data.get('fan_inputs')
speaker = data.get('speaker', 'media_player.room1_speaker')


def turn_on(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'turn_on', service_data, False)


def turn_off(hass, entity, entity_id):
    service_data = {'entity_id': entity_id}
    hass.services.call(entity, 'turn_off', service_data, False)


def tts(hass, speaker, message):
    service_data = {'entity_id': speaker, 'message': message, 'cache': 'false'}
    hass.services.call('tts', 'google_say', service_data, False)


if fan_inputs is not None:
    has_fan = True
    [fan, fan_speed, fan_swing, fan_natural] = fan_inputs
else:
    has_fan = False

light_states = hass.states.get(light_group)
switch_state = hass.states.get(switch_entity).state

if switch_state == '1_click_up':
    if light_states.state == 'off':
        turn_on(hass, 'light', light_group)
    elif light_states.state == 'on':
        scene = hass.states.get(input_scene).state
        turn_on(hass, 'scene', scene)

        service_data = {'entity_id': input_scene}
        hass.services.call('input_select', 'select_next', service_data, False)
elif switch_state == '1_hold_up':
    service_data = {'entity_id': light_group, 'brightness': 255}
    hass.services.call('light', 'turn_on', service_data, False)

    scene_states = hass.states.get(input_scene)
    scene_attr = scene_states.attributes.copy()
    service_data = {
        'entity_id': input_scene,
        'option': scene_attr['options'][0]
    }
    hass.services.call('input_select', 'select_option', service_data, False)
elif switch_state == '4_hold_up':
    if (light_states.state == 'on'):
        service_data = {'entity_id': input_alarm}
        hass.services.call('input_boolean', 'toggle', service_data, False)
        state = hass.states.get(input_alarm).state
        message = 'Upcoming alarm is {}!'.format(state)
        tts(hass, speaker, message)
    elif has_fan:
        service_data = {'entity_id': fan}
        hass.services.call('fan', 'toggle', service_data, False)
elif switch_state == '2_click_up' or switch_state == '3_click_up' or switch_state == '2_hold_up' or switch_state == '3_hold_up':
    if (light_states.state == 'off') and has_fan:
        # Fan control
        if switch_state == '2_click_up' or switch_state == '3_click_up':
            # Fan speed control
            change = 10 if switch_state == '2_click_up' else -10
            speed = int(float(hass.states.get(fan_speed).state)) + change
            if speed > 100:
                speed = 100
            if speed < 1:
                speed = 1
            service_data = {'entity_id': fan_speed, 'value': speed}
            hass.services.call('input_number', 'set_value',
                               service_data, False)
            tts(hass, speaker, speed)
        elif switch_state == '2_hold_up':
            # Fan oscillating control
            swing_angle = hass.states.get(fan_swing).state
            service_data = {'entity_id': fan_swing}
            if swing_angle == '0':
                message = 'Fan oscillation on'
                service_data = {'entity_id': fan_swing, 'option': '30'}
            else:
                message = 'Fan oscillation off'
                service_data = {'entity_id': fan_swing, 'option': '0'}

            hass.services.call(
                'input_select', 'select_option', service_data, False)
            service_data = {'entity_id': speaker, 'message': message}
            hass.services.call('tts', 'google_say', service_data, False)
        elif switch_state == '3_hold_up':
            # Fan natural mode control
            natural_mode = hass.states.get(fan_natural).state
            if natural_mode == 'on':
                tts(hass, speaker, 'Fan natural mode off')
                turn_off(hass, 'input_boolean', fan_natural)
            else:
                tts(hass, speaker, 'Fan natural mode on')
                turn_on(hass, 'input_boolean', fan_natural)
    else:
        # Lights dimming control
        change = 25 if (
            switch_state == '2_click_up' or switch_state == '2_hold') else -25
        if light_states.state == 'on':
            light_group_attr = light_states.attributes.copy()
            lights = light_group_attr['entity_id']
            for l in lights[0:]:
                # To handle case when light is off
                brightness = 25
                l_states = hass.states.get(l)
                if l_states.state == 'on':
                    attr = l_states.attributes.copy()
                    brightness = attr['brightness'] + change
                    if brightness > 255:
                        brightness = 255
                    if brightness < 0:
                        brightness = 0
                # logger.warn('Changing brightness for ' + l + ' to ' + str(brightness))
                service_data = {
                    'entity_id': l,
                    'brightness': brightness
                }
                hass.services.call('light', 'turn_on', service_data, False)
elif switch_state == '4_click_up':
    if light_states.state == 'on':
        turn_off(hass, 'light', light_group)
    else:
        now = datetime.datetime.now()
        # message = 'The time now is {:%H:%M %p}'.format(now)
        message = '{:02d}:{:02d}'.format(now.hour, now.minute)
        tts(hass, speaker, message)
