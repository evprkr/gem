# Misc. Notes

## Planned Changes
* Move Buffer and Cursor to their own classes outside of Editor
* Change buffer naming scheme for better readability
* Switch 'x' and 'y' to 'rows' and 'cols' in as many contexts as possible

## Known Bugs
* Cursor sometimes flickers in odd places when redrawing the screen during scrolling
* Lines with a length of zero visual glitches and sometimes crashes when the cursor moves to them. I noticed that blank lines in a loaded text file have a length of 1, likely '\n'. That's fine, but if you backspace or delete that line break, it causes the weird glitches because the line now has a length of 0.
