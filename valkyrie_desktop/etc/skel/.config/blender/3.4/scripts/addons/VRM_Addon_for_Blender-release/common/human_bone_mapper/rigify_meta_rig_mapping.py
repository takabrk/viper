from typing import Dict

from ..vrm1.human_bone import HumanBoneSpecification, HumanBoneSpecifications

mapping: Dict[str, HumanBoneSpecification] = {
    "spine.006": HumanBoneSpecifications.HEAD,
    "spine.001": HumanBoneSpecifications.SPINE,
    "spine": HumanBoneSpecifications.HIPS,
    "upper_arm.R": HumanBoneSpecifications.RIGHT_UPPER_ARM,
    "forearm.R": HumanBoneSpecifications.RIGHT_LOWER_ARM,
    "hand.R": HumanBoneSpecifications.RIGHT_HAND,
    "upper_arm.L": HumanBoneSpecifications.LEFT_UPPER_ARM,
    "forearm.L": HumanBoneSpecifications.LEFT_LOWER_ARM,
    "hand.L": HumanBoneSpecifications.LEFT_HAND,
    "thigh.R": HumanBoneSpecifications.RIGHT_UPPER_LEG,
    "shin.R": HumanBoneSpecifications.RIGHT_LOWER_LEG,
    "foot.R": HumanBoneSpecifications.RIGHT_FOOT,
    "thigh.L": HumanBoneSpecifications.LEFT_UPPER_LEG,
    "shin.L": HumanBoneSpecifications.LEFT_LOWER_LEG,
    "foot.L": HumanBoneSpecifications.LEFT_FOOT,
    "eye.R": HumanBoneSpecifications.RIGHT_EYE,
    "eye.L": HumanBoneSpecifications.LEFT_EYE,
    "jaw": HumanBoneSpecifications.JAW,
    "spine.004": HumanBoneSpecifications.NECK,
    "shoulder.L": HumanBoneSpecifications.LEFT_SHOULDER,
    "shoulder.R": HumanBoneSpecifications.RIGHT_SHOULDER,
    "spine.003": HumanBoneSpecifications.UPPER_CHEST,
    "spine.002": HumanBoneSpecifications.CHEST,
    "toe.R": HumanBoneSpecifications.RIGHT_TOES,
    "toe.L": HumanBoneSpecifications.LEFT_TOES,
    "thumb.01.L": HumanBoneSpecifications.LEFT_THUMB_METACARPAL,
    "thumb.02.L": HumanBoneSpecifications.LEFT_THUMB_PROXIMAL,
    "thumb.03.L": HumanBoneSpecifications.LEFT_THUMB_DISTAL,
    "f_index.01.L": HumanBoneSpecifications.LEFT_INDEX_PROXIMAL,
    "f_index.02.L": HumanBoneSpecifications.LEFT_INDEX_INTERMEDIATE,
    "f_index.03.L": HumanBoneSpecifications.LEFT_INDEX_DISTAL,
    "f_middle.01.L": HumanBoneSpecifications.LEFT_MIDDLE_PROXIMAL,
    "f_middle.02.L": HumanBoneSpecifications.LEFT_MIDDLE_INTERMEDIATE,
    "f_middle.03.L": HumanBoneSpecifications.LEFT_MIDDLE_DISTAL,
    "f_ring.01.L": HumanBoneSpecifications.LEFT_RING_PROXIMAL,
    "f_ring.02.L": HumanBoneSpecifications.LEFT_RING_INTERMEDIATE,
    "f_ring.03.L": HumanBoneSpecifications.LEFT_RING_DISTAL,
    "f_pinky.01.L": HumanBoneSpecifications.LEFT_LITTLE_PROXIMAL,
    "f_pinky.02.L": HumanBoneSpecifications.LEFT_LITTLE_INTERMEDIATE,
    "f_pinky.03.L": HumanBoneSpecifications.LEFT_LITTLE_DISTAL,
    "thumb.01.R": HumanBoneSpecifications.RIGHT_THUMB_METACARPAL,
    "thumb.02.R": HumanBoneSpecifications.RIGHT_THUMB_PROXIMAL,
    "thumb.03.R": HumanBoneSpecifications.RIGHT_THUMB_DISTAL,
    "f_index.01.R": HumanBoneSpecifications.RIGHT_INDEX_PROXIMAL,
    "f_index.02.R": HumanBoneSpecifications.RIGHT_INDEX_INTERMEDIATE,
    "f_index.03.R": HumanBoneSpecifications.RIGHT_INDEX_DISTAL,
    "f_middle.01.R": HumanBoneSpecifications.RIGHT_MIDDLE_PROXIMAL,
    "f_middle.02.R": HumanBoneSpecifications.RIGHT_MIDDLE_INTERMEDIATE,
    "f_middle.03.R": HumanBoneSpecifications.RIGHT_MIDDLE_DISTAL,
    "f_ring.01.R": HumanBoneSpecifications.RIGHT_RING_PROXIMAL,
    "f_ring.02.R": HumanBoneSpecifications.RIGHT_RING_INTERMEDIATE,
    "f_ring.03.R": HumanBoneSpecifications.RIGHT_RING_DISTAL,
    "f_pinky.01.R": HumanBoneSpecifications.RIGHT_LITTLE_PROXIMAL,
    "f_pinky.02.R": HumanBoneSpecifications.RIGHT_LITTLE_INTERMEDIATE,
    "f_pinky.03.R": HumanBoneSpecifications.RIGHT_LITTLE_DISTAL,
}

config = ("Rigify Meta-Rig", mapping)
