bl_info = {
    "name": "Sapling Randomizer",
    "author": "Thomas Radeke",
    "version": (0, 1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Create",
    "description": "Generate multiple randomized \"Sapling\" curves at the same time.",
    "warning": "Needs the \"Sapling Tree Gen\" add-on to be activated.",
    "wiki_url": "https://github.com/ThomasRadeke/sapling-randomizer/wiki",
    "category": "Add Curve",
}

import os, bpy, random, math, add_curve_sapling
from bpy.props import *

class SaplingRandomizerOperator(bpy.types.Operator):
    bl_idname = "curve.sapling_randomizer"
    bl_label = "Sapling Randomizer"
    
    # Fix missing "bend" property in Sapling, which would otherwise prevent
    # execution of tree_add()
    add_curve_sapling.AddTree.bend = 0.0
    
    def getPresets(self, context):
        # get Sapling presets
        sapling_presets = []
        for p in add_curve_sapling.getPresetpaths():
            sapling_presets = sapling_presets + [a for a in os.listdir(p) if a[-3:] == '.py']
                
        # Prepare enum item list from filenames
        preset_items = []
        for s in sapling_presets:
            preset_items.append((s, s, 'Use "'+s+'" as preset'))
        return preset_items
    
    # Define class properties that will show up as UI elements on the dialog
    presets: EnumProperty(name="Preset", description="", items=getPresets)
    num_trees: IntProperty(name="Number of Saplings", description="Number of trees that will be generated by Sapling", default=10, min=1)
    spread: FloatProperty(name="Spread", description="Area in which Saplings will be created", unit='LENGTH')
    relative_spread: BoolProperty(name="Relative Spread", description="Make spread depend on number of Saplings", default=True)
    randomseed: IntProperty(name="Random Seed", description="Starting seed that will be passed to Sapling when generating trees", default=0)
    max_branch_levels: IntProperty(name="Maximum Branch Levels", description="Maximum branch levels to import from the preset", default=2) 
    show_leaves: BoolProperty(name="Generate Leaves", description="Generate leaves for all generated Saplings", default=True)
    # leaf shape enum copied directly from Sapling.
    leaf_shape: EnumProperty(name="Leaf Shape", items=(('hex', 'Hexagonal', '0'), ('rect', 'Rectangular', '1'),
               ('dFace', 'DupliFaces', '2'), ('dVert', 'DupliVerts', '3')), default='hex')
    create_collection: BoolProperty(name="Create Collection", description="Create a new Collection for the new randomized objects", default=True)
    create_materials: BoolProperty(name="Create Materials", description="Create and assign tree trunk and leaf materials to all generated objects.", default=True)
    prepare_for_particles: BoolProperty(name="For Particle Systems", description="Prepare generated objects for use in particle systems.", default=False)
    
    # Run the actual code upon pressing "OK" on the dialog
    def execute(self, context):
        
        # decide whether "spread" will be relative or absolute
        if self.relative_spread:
            spread = math.sqrt(self.num_trees)*self.spread
        else:
            spread = self.spread
        
        # get window_manager context to make updating the progress indicator less code
        wm = bpy.context.window_manager
        
        # get list of current objects
        objects_before = bpy.data.objects.values()
        
        # start up the random generator with a new seed
        random.seed(self.randomseed)
        
        # start progress indicator
        wm.progress_begin(0, self.num_trees)
        
        # generate a number of trees
        for s in range(0, self.num_trees):
            #add_curve_sapling.ImportData.filename = 'japanese_maple.py'
            
            # use Sapling's own ImportData class to read the preset files into the "settings" list
            add_curve_sapling.ImportData.filename = self.presets
            add_curve_sapling.ImportData.execute(add_curve_sapling.ImportData, bpy.context)
            
            # have to override the preset values after reading them
            if add_curve_sapling.settings["levels"] > self.max_branch_levels:
                add_curve_sapling.settings["levels"] = self.max_branch_levels
            add_curve_sapling.settings["limitImport"] = False
            add_curve_sapling.settings["do_update"] = True
            add_curve_sapling.settings["bevel"] = True
            add_curve_sapling.settings["prune"] = False
            add_curve_sapling.settings["showLeaves"] = self.show_leaves
            add_curve_sapling.settings["leafShape"] = self.leaf_shape
            add_curve_sapling.settings["useArm"] = False
            add_curve_sapling.settings["seed"] = self.randomseed+s
            
            # run the actual tree generating code
            obj = bpy.ops.curve.tree_add(
                limitImport=False,
                do_update=True,
                bevel=True,
                prune=False,
                showLeaves=self.show_leaves,
                leafShape=self.leaf_shape,
                useArm=False,
                seed=self.randomseed+s
            )
            # update the progress indicator after each tree
            wm.progress_update(s)
            
        # tell the progress indicator we're finished
        wm.progress_end()
        
        # make object list after generating
        objects_after = bpy.data.objects.values()
        newobjects = [object for object in objects_after if object not in objects_before]
        
        # set up basic materials
        if self.create_materials:
            # trunk
            trunk_material = bpy.data.materials.new("Sapling Trunk")
            trunk_material.diffuse_color = (0.0508761, 0.0450703, 0.0371111, 1) # dark brown
            trunk_material.roughness = 1.0
            trunk_material.specular_intensity = 0.0
            
            # leaves
            leaf_material = bpy.data.materials.new("Sapling Leaves")
            leaf_material.diffuse_color = (0.024514, 0.0508761, 0.0196054, 1) # darkish green
            leaf_material.roughness = 0.3
            leaf_material.specular_intensity = 0.5
        
        # since we cannot tell Sapling where to put its new trees, we have to iterate through all new "tree" objects
        # and move them randomly after generating them
        
        # also prepare a list of potentially joined meshes
        join_meshes = []
        for obj in newobjects:
            
            # some operators require selections, so first deselect everything
            bpy.ops.object.select_all(action='DESELECT')
            
            # process trunks
            if obj.type == 'CURVE':
                cursor = bpy.context.scene.cursor.location
                x = (random.random() * spread) - spread/2 + cursor[0] 
                y = (random.random() * spread) - spread/2 + cursor[1]
                obj.location = (x, y, cursor[2])
                
                if self.create_materials:
                    obj.data.materials.append(trunk_material)
                
                # if prepare_for_particles, convert curve to mesh and add mesh to list
                # of objects that need to be joined with their leaves
                if self.prepare_for_particles:
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.convert(target='MESH')
                    join_meshes.append(obj)
            
            # leaves
            if obj.type == 'MESH' and self.create_materials:
                obj.data.materials.append(leaf_material)
        
            # if prepare_for_particles, fix the wrongly-rotated axis by rotating the object by
            # 90° on X, applying the rotation and rotating it back by 90°
            if self.prepare_for_particles:
                obj.rotation_euler = (-1.5708,0,0)
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
                obj.rotation_euler = (1.5708,0,0)
        
        # in case we want to prepare the trees for particle systems, go through the previously
        # prepared list of converted meshes, join their leaves to them and construct
        # a new list with just the final joined objects
        joined = []
        if self.prepare_for_particles:
            for mesh in join_meshes:
                bpy.ops.object.select_all(action='DESELECT')
                child = mesh.children[0]
                child.select_set(True)
                mesh.select_set(True)
                bpy.context.view_layer.objects.active = mesh
                bpy.ops.object.join()
                joined.append(mesh)
        
        if self.create_collection:
            # make new collection
            newcol = bpy.data.collections.new("Randomized "+self.presets)
            bpy.context.scene.collection.children.link(newcol)

            # if the objects have been prepared for particle systems, the "newobjects" list
            # has now changed drastically. Replace it with the list of prepared meshes.
            if self.prepare_for_particles:
                newobjects = joined
                
            # move new objects into collection
            for objref in newobjects:
                #print(objref)
                # link new object to new collection
                newcol.objects.link(objref)
                # remove object from scene collection
                bpy.context.scene.collection.objects.unlink(objref)
        
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}
    
    # update the dialog when checkboxes are used
    #def check(self, context):
    #    return True
    
    # set some defaults before popping up the dialog, then pop up the dialog
    def invoke(self, context, event):
        self.num_trees = 10
        self.randomseed = 0
        self.leaf_shape='hex'
        self.relative_spread = True
        self.spread = 3.0
        self.create_collection = True
        return context.window_manager.invoke_props_dialog(self)

# register the operator so it can be called from the class below
bpy.utils.register_class(SaplingRandomizerOperator)

# make an entry in the UI so the randomizer can be called with a button
# instead of just the quick menu
class PANEL_PT_SaplingRandomizer(bpy.types.Panel):
    bl_label = "Sapling Randomizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    #bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("curve.sapling_randomizer")
    
def register():
    bpy.utils.register_class(PANEL_PT_SaplingRandomizer)
    
def unregister():
    bpy.utils.unregister_class(PANEL_PT_SaplingRandomizer)
    
if __name__ == "__main__":
    register()
