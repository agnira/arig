from glob import glob
from pickle import FALSE
from re import A
from bpy import types, context, props
import mathutils
from . import common

class ARIG_OT_register_rig(types.Operator):
    bl_idname = "arig.register_rig"
    bl_label = "Register Rig"
    bl_description = "Register your rig to Arig Tool"

    def execute(self, context:context):
        obj = context.active_object
        arm = obj.data
        pb = obj.pose.bones
        bg = obj.pose.bone_groups
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
        arm["hips"] = "Hips"
        arm["spine"] = "Spine"
        arm["hand_ik_l"] = True
        arm["hand_ik_r"] = True
        #

        # ik controller
        common.asign_ik(obj, eb, pb, arm["forearm_l"], arm["hand_l"], "arm_l", context)
        common.asign_ik(obj, eb, pb, arm["forearm_r"], arm["hand_r"], "arm_r", context)
        common.asign_ik(obj, eb, pb, arm["leg_l"], arm["foot_l"], "leg_l", context)
        common.asign_ik(obj, eb, pb, arm["leg_r"], arm["foot_r"], "leg_r", context)

        # hide unused bone
        pb[arm["forearm_l"]].bone.hide = True
        pb[arm["forearm_l"]].parent.bone.hide = True
        pb[arm["hand_l"]].bone.hide = True
        pb[arm["forearm_r"]].bone.hide = True
        pb[arm["forearm_r"]].parent.bone.hide = True
        pb[arm["hand_r"]].bone.hide = True
        pb[arm["leg_l"]].bone.hide = True
        pb[arm["leg_l"]].parent.bone.hide = True
        pb[arm["foot_l"]].bone.hide = True
        pb[arm["leg_r"]].bone.hide = True
        pb[arm["leg_r"]].parent.bone.hide = True
        pb[arm["foot_r"]].bone.hide = True
        pb[arm["hips"]].bone.hide = True

        # torso root ctrl
        ## create ctrl
        torso_ctrl_name = "Ctrl.Torso"
        if not ((torso_ctrl_name in pb)):
            common.edit_mode()
            spine_ori : types.Bone = eb[arm["spine"]]
            context.object.data.use_mirror_x = False
            torso_ctrl = eb.new(torso_ctrl_name)
            torso_ctrl.length = spine_ori.length
            torso_ctrl.matrix = spine_ori.matrix.copy()
            torso_ctrl.tail = spine_ori.head + mathutils.Vector((0, spine_ori.length*2, 0))
            torso_ctrl.use_deform = False
            torso_ctrl.use_connect = False
            spine_ori.use_connect = False
            spine_ori.parent = torso_ctrl
            common.object_mode()

        # hips controller
        ## create ctrl
        hips_ctrl_name = "Ctrl."+arm["hips"]
        if not ((hips_ctrl_name in pb)):
            common.edit_mode()
            hips_ori : types.Bone = eb[arm["hips"]]
            context.object.data.use_mirror_x = False
            hips_ctrl = eb.new(hips_ctrl_name)
            hips_ctrl.length = hips_ori.length
            hips_ctrl.head = hips_ori.tail
            hips_ctrl.tail = hips_ori.head
            hips_ctrl.use_deform = False
            hips_ctrl.parent = eb["Ctrl.Torso"]
            hips_ori.parent = hips_ctrl
            common.object_mode()

        # create bone group
        if not bg.get("arig_mid"):
            gr1 = bg.new(name="arig_mid")
            gr1.color_set = "THEME01"
        if not bg.get("arig_ik"):
            gr2 = bg.new(name="arig_ik")
            gr2.color_set = "THEME04"
        if not bg.get("arig_fk"):
            gr3 = bg.new(name="arig_fk")
            gr3.color_set = "THEME03"

        bone: types.PoseBone
        for bone in pb :
            if not any(s.lower() in bone.name for s in (".r", ".l", "left", "right", "-r", "-l", "_r", "_l")):
                bone.bone_group = bg["arig_mid"]
            if any(s in bone.name for s in ("Pole.", "IK.")):
                bone.bone_group = bg["arig_ik"]
            
        for bone in pb :
            if bone.bone_group == None :
                bone.bone_group = bg["arig_fk"]

        return {'FINISHED'}

class ARIG_OT_unregister_rig(types.Operator):
    bl_idname = "arig.unregister_rig"
    bl_label = "Unregister Rig"
    bl_description = "Remove all Arig realted tool"

    def execute(self, context):
        obj = context.active_object
        arm = obj.data
        pb = obj.pose.bones
        eb: types.ArmatureEditBones = obj.data.edit_bones

        # return bone hirearki
        common.edit_mode()
        eb[arm["spine"]].parent = eb[arm["hips"]]
        # cleanup
        bone: types.EditBone
        for bone in eb :
            if any(s in bone.name for s in ("IK.", "Pole.", "Ctrl.")):
                eb.remove(bone)
        common.object_mode()
        bone: types.PoseBone
        for bone in pb:
            bone.bone_group = None
            bone.bone.hide = False
            for c in bone.constraints:
                bone.constraints.remove(c)  # Remove constraint

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
        del arm["hips"]
        del arm["spine"]

        return {'FINISHED'}

class ARIG_OT_ik_fk(types.Operator):
    bl_idname = "arig.ik_fk"
    bl_label = "Switch IK FK"
    bl_description = "If on/true the bone is asign as IK"

    bone : props.StringProperty(name="bone")
    @classmethod
    def poll(cls, context: context):
        return context.object is not None
    def execute(self, context: context):
        obj = context.active_object
        arm = obj.data
        pb = obj.pose.bones
        if self.bone == "hand_l":
            if arm["hand_ik_l"]:
                common.switch_ik_fk(arm= arm, pb=pb, ik=arm["forearm_l"], ct=arm["hand_l"], ikt="hand_ik_l", influence=0)
            else :
                common.switch_ik_fk(arm=arm, pb=pb, ik=arm["forearm_l"], ct=arm["hand_l"], ikt="hand_ik_l", influence=1)
        if self.bone == "hand_r":
            if arm["hand_ik_r"]:
                common.switch_ik_fk(arm=arm, pb=pb, ik=arm["forearm_r"], ct=arm["hand_r"], ikt="hand_ik_r", influence=0)
            else :
                common.switch_ik_fk(arm=arm, pb=pb, ik=arm["forearm_r"], ct=arm["hand_r"], ikt="hand_ik_r", influence=1)
        return {'FINISHED'}
        

class ARIG_OT_gen_from_mesh(types.Operator):
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
