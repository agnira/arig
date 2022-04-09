from bpy import types

class UI_PT_AR_Arig(types.Panel):
    bl_idname = "UI_PT_AR_Arig"
    bl_label = "Asign Rig"
    bl_category = "arig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # get data
        obj = context.active_object

        layout = self.layout

        if obj.type == "ARMATURE" :
            arm = obj.data            
            status = "Not-Registered"

            if arm.get("arig_id") :
                status = "Registered"

            row = layout.row(align=True)
            row.label(text=obj.name + " : " + status)
            
            if status == "Not-Registered" :
                row = layout.row(align=True)
                row.operator("arig.register_rig", text="Register Rig")

            if status == "Registered" :
                row = layout.row(align=True)
                row.operator("arig.unregister_rig", text="Unregister Rig")

            # for bone in arm.bones:
            #     row = layout.row(align=True)
            #     row.label(text=bone.name)



class UI_PT_Gen_Arig(types.Panel):
    bl_idname = "UI_PT_Gen_Arig"
    bl_label = "Generator"
    bl_category = "arig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, _):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('arig.gen_from_mesh', text= 'Flow from mesh', text_ctxt='Generate rig flow from mesh. This is can be usefull for creating hair or cloth rig')