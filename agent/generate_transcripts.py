import json
import os

with open("../tree/reflection-tree.json", encoding="utf-8") as f:
    tree = json.load(f)

tree["nodes"] = {k: v for k, v in tree["nodes"].items() if "type" in v}


def simulate(path_choices, persona_name):
    state = {
        "node_id": tree["meta"]["startNode"],
        "axis": {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"others": 0, "self": 0}
        },
        "log": []
    }

    def apply(signals):
        for s in signals:
            axis, val = s.split(":")
            state["axis"][axis][val] += 1

    def eval_cond(expr):
        expr = expr.replace("axis1.internal", str(state["axis"]["axis1"]["internal"]))
        expr = expr.replace("axis1.external", str(state["axis"]["axis1"]["external"]))
        expr = expr.replace("axis2.contribution", str(state["axis"]["axis2"]["contribution"]))
        expr = expr.replace("axis2.entitlement", str(state["axis"]["axis2"]["entitlement"]))
        expr = expr.replace("axis3.others", str(state["axis"]["axis3"]["others"]))
        expr = expr.replace("axis3.self", str(state["axis"]["axis3"]["self"]))
        return eval(expr, {"__builtins__": None}, {})

    while True:
        node = tree["nodes"][state["node_id"]]

        if node["type"] == "question":
            state["log"].append(f"\nQ: {node['text']}")

            choice = path_choices.get(state["node_id"], 0)
            opt = node["options"][choice]

            state["log"].append(f"A: {opt['label']}")

            if "signals" in opt:
                apply(opt["signals"])

            state["node_id"] = opt["next"]

        elif node["type"] == "decision":
            for cond in node["conditions"]:
                if cond["if"] == "otherwise" or eval_cond(cond["if"]):
                    state["log"].append(f"→ Decision: {cond['if']}")
                    state["node_id"] = cond["next"]
                    break

        elif node["type"] == "reflection":
            state["log"].append(f"\nReflection: {node['text']}")
            state["node_id"] = node.get("next")

        elif node["type"] == "summary":
            state["log"].append(f"\nFINAL SUMMARY:\n{node['text']}")
            state["node_id"] = node.get("next")

        elif node["type"] == "end":
            break

        else:
            state["node_id"] = node.get("next")

    # Add axis summary
    axis_summary = "\n\nAxis Tallies:\n"
    for axis, values in state["axis"].items():
        axis_summary += f"{axis}: {values}\n"

    transcript = f"# {persona_name}\n"
    transcript += "\n".join(state["log"])
    transcript += axis_summary

    return transcript


# Persona 1 (external / entitlement / self)
persona1 = {
    "A1_Q1": 1,
    "A1_Q2": 1,
    "A1_Q3": 2,
    "A2_Q1": 2,
    "A2_Q2": 2,
    "A3_Q1": 2,
    "A3_Q2": 0
}

# Persona 2 (internal / contribution / others)
persona2 = {
    "A1_Q1": 0,
    "A1_Q2": 0,
    "A1_Q3": 0,
    "A2_Q1": 0,
    "A2_Q2": 0,
    "A3_Q1": 0,
    "A3_Q2": 1
}


t1 = simulate(persona1, "Transcript 1 — External / Entitled / Self")
t2 = simulate(persona2, "Transcript 2 — Internal / Contribution / Others")

final_output = t1 + "\n\n" + "="*60 + "\n\n" + t2


# SAVE FILE
output_dir = "../transcripts"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "generated_transcripts.md")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"\nTranscripts saved to: {output_path}")