# Misc Notes

## Design Standards
* Directional parameters are always ordered as UP, DOWN, LEFT, RIGHT
* Lifetime display of temporary windows is the dumbest thing ever. Lifetime is reduced by 0.5 every update, and displayed as int(lifetime / 2) -- Because an update (without user input) is 250ms, this is the closest I can get to -1/second without doing any real thinking. To make this less stupid to use, I made it so whatever lifetime you pass into the `send_alert` function is doubled, so if you pass in 10, it'll take 10 "seconds" to kill the window. Seconds are actually updates, so if you move the cursor around or type while the window is open, it'll tick down faster.

## Random Ideas
* Waypoints in files, create/delete with some hotkey, cycle forward/backward through them with another hotkey, display symbol in the gutter

## Misc.

```

*****  *   *  *   *
  *    **  *  *  *
  *    * * *  ***
  *    *  **  *  *
*****  *   *  *   *

```
