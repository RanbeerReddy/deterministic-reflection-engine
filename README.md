# Deterministic Reflection Agent

This project implements a deterministic, data-driven reflection system built on top of a decision tree.

It evaluates user responses across three behavioral axes:

- **Axis 1 — Locus of Control** (internal vs external)
- **Axis 2 — Orientation** (contribution vs entitlement)
- **Axis 3 — Radius of Concern** (others vs self)

The system is fully deterministic:
- No randomness
- No LLMs
- All behavior is driven by the JSON tree

---

## 📁 Project Structure


project/
│
├── tree/
│ └── reflection-tree.json # Core decision tree (Part A)
│
├── agent/
│ ├── app.py # Flask-based interactive agent
│ ├── generate_transcripts.py # Transcript simulation script
│ └── templates/
│ └── index.html # UI
│
├── transcripts/
│ ├── transcript_external.md # External / Entitled / Self path
│ ├── transcript_internal.md # Internal / Contribution / Others path
│ └── generated_transcripts.md # Auto-generated transcripts
│
├── diagram.md # Mermaid tree diagram
├── writeup.md # Design explanation
└── README.md


---

## 🚀 How to Run the Agent (Web UI)

### 1. Install dependencies


pip install flask


### 2. Run the app


cd agent
python app.py


### 3. Open in browser


http://127.0.0.1:5000


---

## 🧠 How the Agent Works

- Loads the decision tree from `reflection-tree.json`
- Starts from the `startNode`
- Walks node-by-node:
  - `question` → waits for user input
  - `decision` → evaluates conditions (no randomness)
  - `reflection` → shows insight
  - `bridge` → transitions between axes
  - `summary` → final synthesis
- Tracks signals across axes:
  - `axis1: internal / external`
  - `axis2: contribution / entitlement`
  - `axis3: others / self`
- Generates final reflection based on accumulated signals

---

## 📊 How to Generate Transcripts

Transcripts simulate predefined personas through the tree.

### Run:


cd agent
python generate_transcripts.py


### Output:


transcripts/generated_transcripts.md


---

## 🧾 Provided Transcripts

Two example paths are included:

### 1. External / Entitled / Self
- Attributes outcomes externally
- Focuses on recognition and self-balance
- Narrow radius of concern

File:

transcripts/transcript_external.md


---

### 2. Internal / Contribution / Others
- Takes ownership of outcomes
- Contributes beyond assigned role
- Focuses on team and impact

File:

transcripts/transcript_internal.md


---

## 🌳 Understanding the Tree (`reflection-tree.json`)

The tree is the core system.

Each node has a type:

| Type        | Purpose |
|------------|--------|
| `start`     | Entry point |
| `question`  | User selects an option |
| `decision`  | Internal branching logic |
| `reflection`| Insight based on path |
| `bridge`    | Transition between axes |
| `summary`   | Final synthesis |
| `end`       | Session termination |

---

### Signals

Each option emits signals like:


axis1:internal
axis2:contribution
axis3:self


These are accumulated and used in decision nodes:


axis1.internal > axis1.external


---

## ⚙️ Key Properties of the System

- Deterministic execution
- Fully traceable from JSON
- No hidden logic
- Adaptive questioning via clarification nodes
- Reflection based on accumulated behavior, not single answers

---

## 📝 Notes

- The agent is intentionally simple (Flask UI) to focus on logic
- All branching decisions are predefined in the JSON
- The transcript generator uses the same logic as the agent

---

## ✅ Summary

This system demonstrates:
- Structured decision modeling
- Deterministic behavioral evaluation
- Signal-based reasoning
- End-to-end execution from data (JSON → UI → output)