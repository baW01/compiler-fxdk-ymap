import json
import xml.etree.ElementTree as ET
import math
import os

def matrix_to_quaternion(matrix):
    r00, r01, r02 = matrix[0]
    r10, r11, r12 = matrix[1]
    r20, r21, r22 = matrix[2]

    trace = r00 + r11 + r22

    if trace > 0:
        qw = math.sqrt(1 + trace) / 2
        qx = (r21 - r12) / (4 * qw)
        qy = (r02 - r20) / (4 * qw)
        qz = (r10 - r01) / (4 * qw)
    elif r00 > r11 and r00 > r22:
        qx = math.sqrt(1 + r00 - r11 - r22) / 2
        qw = (r21 - r12) / (4 * qx)
        qy = (r01 + r10) / (4 * qx)
        qz = (r02 + r20) / (4 * qx)
    elif r11 > r22:
        qy = math.sqrt(1 + r11 - r00 - r22) / 2
        qw = (r02 - r20) / (4 * qy)
        qx = (r01 + r10) / (4 * qy)
        qz = (r12 + r21) / (4 * qy)
    else:
        qz = math.sqrt(1 + r22 - r00 - r11) / 2
        qw = (r10 - r01) / (4 * qz)
        qx = (r02 + r20) / (4 * qz)
        qy = (r12 + r21) / (4 * qz)

    return qx, qy, qz, qw

def fxworld_to_ymap(input_file, output_file):
    with open(input_file, 'r') as f:
        fxworld_data = json.load(f)

    root = ET.Element("CMapData")

    ET.SubElement(root, "name", xmlns_p2="http://www.w3.org/2001/XMLSchema-instance", p2_nil="true")
    ET.SubElement(root, "parent", xmlns_p2="http://www.w3.org/2001/XMLSchema-instance", p2_nil="true")
    ET.SubElement(root, "flags", value="0")
    ET.SubElement(root, "contentFlags", value="65")
    ET.SubElement(root, "streamingExtentsMin", x="-12570.9473", y="-10749.5654", z="-987.0895")
    ET.SubElement(root, "streamingExtentsMax", x="7429.053", y="9250.435", z="5012.91064")
    ET.SubElement(root, "entitiesExtentsMin", x="-12570.9473", y="-10749.5654", z="-987.0895")
    ET.SubElement(root, "entitiesExtentsMax", x="7429.053", y="9250.435", z="5012.91064")

    entities = ET.SubElement(root, "entities")

    if 'additions' in fxworld_data:
        for obj_id, obj_data in fxworld_data['additions'].items():
            item = ET.SubElement(entities, "Item", type="CEntityDef")

            mdl = obj_data.get('mdl', "unknown_model")
            mat = obj_data.get('mat', [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
            x, y, z = mat[12], mat[13], mat[14]

            rotation_matrix = [
                [mat[0], mat[1], mat[2]],
                [mat[4], mat[5], mat[6]],
                [mat[8], mat[9], mat[10]]
            ]
            qx, qy, qz, qw = matrix_to_quaternion(rotation_matrix)

            ET.SubElement(item, "archetypeName").text = mdl
            ET.SubElement(item, "flags", value="32")
            ET.SubElement(item, "guid", value="0")
            ET.SubElement(item, "position", x=str(x), y=str(y), z=str(z))
            ET.SubElement(item, "rotation", x=str(qx), y=str(qy), z=str(qz), w=str(qw))

            # Add other attributes
            ET.SubElement(item, "scaleXY", value="1")
            ET.SubElement(item, "scaleZ", value="1")
            ET.SubElement(item, "parentIndex", value="-1")
            ET.SubElement(item, "lodDist", value="500")
            ET.SubElement(item, "childLodDist", value="500")
            ET.SubElement(item, "lodLevel").text = "LODTYPES_DEPTH_HD"
            ET.SubElement(item, "numChildren", value="0")
            ET.SubElement(item, "priorityLevel").text = "PRI_REQUIRED"
            ET.SubElement(item, "ambientOcclusionMultiplier", value="255")
            ET.SubElement(item, "artificialAmbientOcclusion", value="255")
            ET.SubElement(item, "tintValue", value="0")

    ET.SubElement(root, "containerLods")
    ET.SubElement(root, "boxOccluders")
    ET.SubElement(root, "occludeModels")
    ET.SubElement(root, "physicsDictionaries")
    ET.SubElement(root, "instancedData")
    ET.SubElement(root, "timeCycleModifiers")
    ET.SubElement(root, "carGenerators")
    ET.SubElement(root, "LodLightsSoa")
    ET.SubElement(root, "DistantLodLightsSoa")

    block = ET.SubElement(root, "block")
    ET.SubElement(block, "version", value="0")
    ET.SubElement(block, "flags", value="0")
    ET.SubElement(block, "time").text = "21 grudnia 2024 21:25"

    tree = ET.ElementTree(root)
    with open(output_file, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)

def main():
    print("FXWorld to YMAP Converter")
    print("==========================")
    input_file = input("Enter the path to the input .fxworld file: ").strip()

    if not input_file.endswith(".fxworld"):
        print("Error: Input file must have the .fxworld extension.")
        return

    output_file = input_file.replace(".fxworld", ".ymap.xml")

    if not os.path.isfile(input_file):
        print(f"Error: The input file '{input_file}' does not exist.")
        return

    try:
        fxworld_to_ymap(input_file, output_file)
        print(f"Successfully converted '{input_file}' to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
