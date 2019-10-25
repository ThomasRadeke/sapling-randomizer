# Sapling Randomizer
This Blender add-on allows to create multiple random trees at the same time, based on the built-in "Sapling" tree generator.

## Download
1. Download:
  - [sapling-randomizer_0.1.2.zip](https://github.com/ThomasRadeke/sapling-randomizer/raw/master/sapling-randomizer-0.1.2.zip) (Blender 2.80)
  - [sapling-randomizer_0.1.0.zip](https://rahdick.at/projects/02_projects/2018-04-06_blender_addon_sapling_randomizer/sapling-randomizer_0.1.0.zip) (Blender 2.7x)
  - If the direct links don't work, please visit the [project website](https://rahdick.at/en/02_projects/2018-04-06_blender_addon_sapling_randomizer) and download from there.
2. In Blender, go to User Preferences > Add-Ons, click the "Install Add-on from File…" button on the bottom of the dialog and choose the downloaded ZIP file.
3. Find BOTH "Sapling Tree Gen" AND "Sapling Randomizer" and enable them. This add-on uses the built-in "Sapling Tree Gen" to generate the trees, so it must be enabled.

## Version 0.1.2 changes
- Fixed Blender 2.80 Python API warnings
- Added option for putting new objects into a collection
- Added option for creating and assigning materials for trunks and leaves
- Added option for preparing generated trees for use in particle systems
- 3D cursor position is now taken into account

## Installation via GitHub
1. Download and unpack the thing.
2. Find the "sapling-randomizer" directory inside. It should only have a single .py file.
3. (A) Copy the whole directory (not just the Python file!) to your Blender Scripts directory or (B) pack the "sapling-randomizer" directory as a ZIP file again and install it via Blender's add-on manager.
4. In Blender's add-on manager, find BOTH "Sapling Tree Gen" AND "Sapling Randomizer" and enable them. This add-on uses the built-in "Sapling Tree Gen" to generate the trees, so it must be enabled.

## Usage
When you have successfully enabled both add-ons, you can invoke the Sapling Randomizer using two methods:
- 3D view > Tool Shelf > "Create" tab - you'll find a "Sapling Randomizer" button. Press it.
- Using the quick menu (F3). Just type "Sapling Randomizer" and hit return.

For more detail, head over to the [wiki](https://github.com/ThomasRadeke/sapling-randomizer/wiki).

## Known issues
I'm not primarily a software developer, so please use the add-on with caution.
- Some options are VERY SLOW, e.g. the "Maximum Branch Levels" control. Try with a low number of trees first. This depends on "Sapling"; can't do anything about it. Sorry!
- Most options of the original "Sapling" add-on are not accessible through SR. However, you can save presets with "Sapling" and use them with SR.
