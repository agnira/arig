from math import degrees, pi
import random
import string
from tokenize import String
from bpy import ops, types, context as ctx
from mathutils import Vector

charset = string.ascii_letters+string.digits


def rand_str(length=8) -> str:
    max = len(charset)
    s = ""
    for i in range(length):
        s += str(charset[random.randint(0, max-1)])
    return s


def asign_ik(obj: types.Object, eb: types.ArmatureEditBones,  pb: types.PoseBone, ik: str, target: str, type: str):
    ctx.object.pose.use_mirror_x = False

    pole_angle = pi * 0.0 / 180
    if type == "arm_r":
        pole_angle = pi * 180 / 180
    elif (("leg" in type)):
        pole_angle = pi * 90 / 180
    # create ik target
    ik_target_name = "IK."+target
    if not ((ik_target_name in pb)):
        edit_mode()
        ctx.object.data.use_mirror_x = False
        ik_target = eb.new(ik_target_name)
        ik_target.length = eb[target].length
        ik_target.matrix = eb[target].matrix.copy()
        ik_target.use_deform = False
        object_mode()

    # create pole target
    ik_pole_name = "Pole."+target
    if not ((ik_pole_name in pb)):
        edit_mode()
        ctx.object.data.use_mirror_x = False
        ik_pole = eb.new(ik_pole_name)
        ik_pole.use_deform = False
        ik_pole.parent = eb[ik_target_name]
        ik_pole.use_connect = False
        ik_pole.matrix = eb[ik].matrix.copy()
        if (("arm" in type)):
            ik_pole.head += Vector((0, eb[ik].length, 0))
            ik_pole.tail = ik_pole.head + \
                Vector((0, eb[ik].length/3, 0))
        elif (("leg" in type)):
            ik_pole.head -= Vector((0, eb[ik].length, 0))
            ik_pole.tail = ik_pole.head - \
                Vector((0, eb[ik].length/3, 0))
        object_mode()

    ikc: types.KinematicConstraint = pb[ik].constraints.get("IK")
    if ikc == None:
        ikc = pb[ik].constraints.new('IK')
    ikc.target = obj
    ikc.subtarget = ik_target_name
    ikc.pole_target = obj
    ikc.pole_subtarget = ik_pole_name
    ikc.chain_count = 2
    ikc.use_tail = True
    ikc.use_stretch = True
    ikc.pole_angle = pole_angle
    print(pole_angle)
    print(ikc.pole_angle)

    ct = pb[target].constraints.get('Copy Transforms')
    if ct == None:
        ct = pb[target].constraints.new('COPY_TRANSFORMS')
    ct.target = obj
    ct.subtarget = ik_target_name

def edit_mode():
    ops.object.mode_set(mode='EDIT', toggle=False)

def object_mode():
    ops.object.mode_set(mode='OBJECT', toggle=False)
