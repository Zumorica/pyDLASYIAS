extends Node2D

signal door_press(new_state)
signal light_press(new_state)

var state = 0

const DOOR = 1
const LIGHT = 2

func update_sprite():
	for children in get_node("Sprite").get_children():
		children.hide()
	get_node("Sprite/%s"%state).show()

func is_door_pressed():
	return state & DOOR
	
func is_light_pressed():
	return state & LIGHT

func press_door_button():
	state ^= DOOR
	emit_signal("door_press", state & DOOR)
	update_sprite()

func press_light_button():
	state ^= LIGHT
	emit_signal("light_press", state & LIGHT)
	update_sprite()
	
func _on_Door_input_event( viewport, event, shape_idx ):
	if event.is_action_pressed("left_click") and not event.is_echo():
		press_door_button()

func _on_Light_input_event( viewport, event, shape_idx ):
	if event.is_action_pressed("left_click") and not event.is_echo():
		press_light_button()