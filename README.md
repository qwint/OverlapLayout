# Overlap Layout for Qtile

This layout will tile two visible windows that each cover 60% of the screen and overlap in the middle.


## Support

Config:
* `border_focus`: Focused Border Color
* `border_normal`: Unfocused Border Color
* `margin`: added px padding on each side of the windows
* `border_width`: px size of window borders
* `single_side_left`: if the main - without a stack - window should be placed on the left or right

Commands:
* `next`/`previous`: cycles through the windows
* `left`: moves focus to the left, noops if already on the left
* `right`: moves focus to the right, noops if already on the right
* `up`/`down`: cycles through the off-stack, bringing to front the new focus
* `shuffle_left`: moves the current focused window to the left, noops if already on the left
* `shuffle_right`: moves the current focused window to the right, noops if already on the right
* `flip`: changes which side of the screen is the main window and which is the off-stack
