import json
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret"

# Load JSON
with open("../tree/reflection-tree.json", encoding="utf-8") as f:
    tree = json.load(f)

# REMOVE invalid nodes (comments)
tree["nodes"] = {k: v for k, v in tree["nodes"].items() if "type" in v}


def init_state():
    session["node_id"] = tree["meta"]["startNode"]
    session["answers"] = {}
    session["axis"] = {
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"others": 0, "self": 0}
    }


def apply_signals(signals):
    for s in signals:
        axis, val = s.split(":")
        session["axis"][axis][val] += 1


def get_dominant(axis):
    a = session["axis"][axis]
    keys = list(a.keys())
    if a[keys[0]] > a[keys[1]]:
        return keys[0]
    elif a[keys[1]] > a[keys[0]]:
        return keys[1]
    return "mixed"


def interpolate(text):
    text = text.replace("{axis1.dominant}", get_dominant("axis1"))
    text = text.replace("{axis2.dominant}", get_dominant("axis2"))
    text = text.replace("{axis3.dominant}", get_dominant("axis3"))

    for q, ans in session["answers"].items():
        text = text.replace(f"{{{q}.answer}}", ans)

    return text


def evaluate_decision(node):
    for cond in node["conditions"]:
        if cond["if"] == "otherwise":
            return cond["next"]

        expr = cond["if"]

        expr = expr.replace("axis1.internal", str(session["axis"]["axis1"]["internal"]))
        expr = expr.replace("axis1.external", str(session["axis"]["axis1"]["external"]))
        expr = expr.replace("axis2.contribution", str(session["axis"]["axis2"]["contribution"]))
        expr = expr.replace("axis2.entitlement", str(session["axis"]["axis2"]["entitlement"]))
        expr = expr.replace("axis3.others", str(session["axis"]["axis3"]["others"]))
        expr = expr.replace("axis3.self", str(session["axis"]["axis3"]["self"]))

        if eval(expr, {"__builtins__": None}, {}):
            return cond["next"]

    return node["conditions"][-1]["next"]


@app.route("/", methods=["GET", "POST"])
def index():
    if "node_id" not in session:
        init_state()

    node_id = session.get("node_id")

    if node_id is None or node_id not in tree["nodes"]:
        return redirect(url_for("reset"))

    node = tree["nodes"][node_id]

    if request.method == "POST":

        if node["type"] == "question":
            try:
                choice = int(request.form["choice"])
            except:
                return redirect(url_for("index"))
            selected = node["options"][choice]

            session["answers"][session["node_id"]] = selected["label"]

            if "signals" in selected:
                apply_signals(selected["signals"])

            session["node_id"] = selected["next"]

        else:
            session["node_id"] = node.get("next")

        return redirect(url_for("index"))

    if node["type"] == "decision":
        session["node_id"] = evaluate_decision(node)
        return redirect(url_for("index"))
    
    if node["type"] == "end":
        return render_template("index.html", node=node, text=node["text"])


    return render_template("index.html", node=node, text=interpolate(node["text"]))


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)