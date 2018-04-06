# Sapling Randomizer
This Blender add-on allows to create multiple random trees at the same time, based on the built-in "Sapling" tree generator.

## Installation
1. Download and unpack the thing.
2. Find the "sapling-randomizer" directory inside. It should only have a single .py file.
3. (A) Copy the whole directory (not just the Python file!) to your Blender Scripts directory or (B) pack the "sapling-randomizer" directory as a ZIP file again and install it via Blender's add-on manager.
4. In Blender's add-on manager, find BOTH "Sapling Tree Gen" AND "Sapling Randomizer" and enable them. This add-on uses the built-in "Sapling Tree Gen" to generate the trees, so it must be enabled.

## Usage
When you have successfully enabled both add-ons, you can invoke the Sapling Randomizer using two methods:
- 3D view > Tool Shelf > "Create" tab, on the very bottom, you'll find a "Sapling Randomizer" button. Press it.
- Using the quick menu (Space). Just type "Sapling Randomizer" and hit return.
For more detail, head over to the [wiki](https://github.com/ThomasRadeke/sapling-randomizer/wiki).

## Known issues
This is the very first release and I'm not primarily a software developer, so please use the add-on with caution.
- Some options are VERY SLOW, e.g. the "Maximum Branch Levels" control. Try with a low number of trees first. This depends on "Sapling"; can't do anything about it. Sorry!
- Most options of the original "Sapling" add-on are not accessible through SR. However, you can save presets with "Sapling" and use them with SR.
- Currently, the preset selection dropdown will only show .py files that are located in the "curve_add_sapling/presets/" directory, inside your Blender install location.
- Using this add-on in a scene which has existing "Tree" objects will randomize their location, too. To avoid this, just generate new trees on a new layer/scene and move them into the final location when you're done. (This is because the original "Sapling" add-on doesn't allow generated object names to be changed via script, so I have no easy way to tell them apart.)
- 3D cursor location is currently ignored.
