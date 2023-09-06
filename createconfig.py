import yaml

default_rules = {
        "blade": {"type": 2, "keywords": [["blade"]]},
        "hub": {"type": 2, "keywords": [["hub"]]},
        "inv_wall": {"type": 1, "keywords": [["wall", "inv"]]},
        "period_lo": {"type": 9, "keywords": [["per", "lo"], ["per", "down"]]},
        "period_up": {"type": 10, "keywords": [["per", "up"], ["per", "hi"]]},
        "shroud": {"type": 2, "keywords": [["shroud"], ["casing"], ["case"]]},
        "splitter": {"type": 2, "keywords": [["splitter"]]},
        "subsonic_inflow": {"type": 4, "keywords": [["inflow"], ["inlet"]]},
        "subsonic_outflow": {"type": 5, "keywords": [["outflow"], ["outlet"]]},
        "visc_wall": {"type": 2, "keywords": [["wall"]]}
    }

def read_yaml_to_dict(filename):
    """
    Input the location of the .yaml file
    Output the data of the .yaml file
    """
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def create_config(mesh_files_seq, input_rules=None):
    """
    Input the mesh file selected in sequence and rules(if any)
    Output the STEP-1 yaml file.
    """
    if input_rules is None:
        rules = default_rules
    else:
        rules = read_yaml_to_dict(input_rules)

    # Strip out the '.cgns' extension from each mesh file
    mesh_files_seq = [file.split('.cgns')[0] for file in mesh_files_seq]

    # Convert the mesh_files to yaml formatted string manually
    mesh_files_string = "mesh_files:\n"
    for file in mesh_files_seq:
        mesh_files_string += f"  - {file}\n"
    
    # Convert the bc_rules to yaml formatted string manually
    bc_rules_string = "bc_rules:\n"
    for key, value in rules.items():
        bc_rules_string += f"  {key}:\n"
        bc_rules_string += f"    type: {value['type']}\n"
        bc_rules_string += "    keywords:\n"
        for item in value['keywords']:
            formatted_keywords = ", ".join([f"\"{word}\"" for word in item])
            bc_rules_string += f"      - [{formatted_keywords}]\n"

    with open('STEP-1-Config.yaml', 'w') as f:
        f.write(mesh_files_string)
        f.write(bc_rules_string)

    return 'STEP-1-Config.yaml created successfully!'
