extends Camera2D

export var camera_speed = 500

func _ready():
	set_fixed_process(true)
	
func _fixed_process(delta):
	if get_viewport().get_mouse_pos().x > 855 and get_offset().x < 318:
		set_offset(get_offset() + Vector2(camera_speed*delta,0))

	if get_viewport().get_mouse_pos().x < 425 and get_offset().x > 18:
		set_offset(get_offset() - Vector2(camera_speed*delta,0))