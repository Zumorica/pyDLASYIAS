extends Node2D

func change_background(new_bg):
	for child in get_node("Background").get_children():
		if not child extends AnimatedSprite:
			child.hide()
	get_node("Background/%s"%new_bg).show()

func _on_Left_buttons_door_press( new_state ):
	if new_state:
		get_node("Left_door").play("default")
	else:
		get_node("Left_door").play("reversed")

func _on_Left_buttons_light_press( new_state ):
	if new_state:
		if get_node("Right_buttons").is_light_pressed():
			get_node("Right_buttons").press_light_button()
		change_background("Left")
	else:
		change_background("Normal")

func _on_Right_buttons_door_press( new_state ):
	if new_state:
		get_node("Right_door").play("default")
	else:
		get_node("Right_door").play("reversed")

func _on_Right_buttons_light_press( new_state ):
	if new_state:
		if get_node("Left_buttons").is_light_pressed():
			get_node("Left_buttons").press_light_button()
		change_background("Right")
	else:
		change_background("Normal")

func _on_CameraEnterButton_input_event( viewport, event, shape_idx ):
	print(event)
