from math import fabs
from sqlite3 import connect
from bpy import context, types
import bmesh
from . import common


class ARIG_OT_register_rig(types.Operator):
    bl_idname = "arig.register_rig"
    bl_label = "Register Rig"
    bl_description = "Register your rig to Arig Tool"

    def execute(self, context):
        obj = context.active_object
        arm = obj.data
        pb = obj.pose.bones
        eb: types.ArmatureEditBones = obj.data.edit_bones

        arm["arig_id"] = common.rand_str()

        # asign rig to arig standard
        arm["forearm_l"] = "ForeArm.L"
        arm["forearm_r"] = "ForeArm.R"
        arm["hand_l"] = "Hand.L"
        arm["hand_r"] = "Hand.R"
        arm["leg_l"] = "Leg.L"
        arm["leg_r"] = "Leg.R"
        arm["foot_l"] = "Foot.L"
        arm["foot_r"] = "Foot.R"
        #

        common.asign_ik(obj, eb, pb, arm["forearm_l"], arm["hand_l"], "arm_l")
        common.asign_ik(obj, eb, pb, arm["forearm_r"], arm["hand_r"], "arm_r")
        common.asign_ik(obj, eb, pb, arm["leg_l"], arm["foot_l"], "leg_l")
        common.asign_ik(obj, eb, pb, arm["leg_r"], arm["foot_r"], "leg_r")

        return {'FINISHED'}

class ARIG_OT_unregister_rig(types.Operator):
    bl_idname = "arig.unregister_rig"
    bl_label = "Unregister Rig"
    bl_description = "Remove all Arig realted tool"

    def execute(self, _):
        obj = context.active_object
        arm = obj.data
        pb = obj.pose.bones
        eb: types.ArmatureEditBones = obj.data.edit_bones

        # remove all custom prop
        del arm["arig_id"]
        del arm["forearm_l"]
        del arm["forearm_r"]
        del arm["hand_l"]
        del arm["hand_r"]
        del arm["leg_l"]
        del arm["leg_r"]
        del arm["foot_l"]
        del arm["foot_r"]
        common.edit_mode()
        bone: types.EditBone
        for bone in eb :
            if any(s in bone.name for s in ("IK.", "Pole.")):
                eb.remove(bone)
        common.object_mode()

        for bone in pb:
            for c in bone.constraints:
                bone.constraints.remove(c)  # Remove constraint

        return {'FINISHED'}



        



class ARIG_OT_gen_from_mesh(bpy.types.Operator):
    bl_idname = "arig.gen_from_mesh"
    bl_label = "Generate Rig From Mesh"
    bl_description = "Generate rig flow from mesh. This is can be usefull for creating hair or cloth rig"

    def execute(self, context):
        print(context.selected_objects)
        print(context.active_object.data.name)

        # v = bpy.types.MeshVertex{}
        # for i, v in bpy.data.meshes[bpy.context.active_object.data.name].vertices:
        #     print(v.co)
        # print(bpy.data.meshes[bpy.context.active_object.data.name].vertices)
        # if len(bpy.context.selected_objects) == 1 :
        #     baseObject = bpy.context.selected_objects[0].name
        #     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
        #     bpy.context.active_object.name =  '_ar_temp_'+baseObject

        # print("test2")
        return {'FINISHED'}
