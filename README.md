Modifiers shortcuts panel - Blender script
==========================================

New panel in modifiers tab for quicker access to favorite modifiers

![Img1]

*Panel with shortucts to array, mask, subsurf and mirror modifiers*

## Usage

Run [script] inside blender:

1. Open Text Editor view in blender
1. Paste the content of [script]
1. Press **Run script**
1. Select object and go to properties -> modifiers

#### Buttons

* toggle usage of all modifiers during **rendering**
* toggle usage of all modifiers **in viewport**
* toggle usage of all modifiers **in edit mode**
* toggle display of all modifiers **on edit cage**
* **apply all** modifiers
* **add or remove** first modifier to the favorite modifiers list

###### Last tested blender version: 2.72b

###### Script uses scene.common_used_modifiers custom property. Use it if You want to f.e. exchange addon settings between files.

[img1]: https://raw.github.com/Scthe/modifierShortcutsPanel_blender/master/img1.jpg
[script]: modifier_shortcuts_panel.py
