```mermaid
%%{init: {'theme': 'base'}}%%
graph TD

START([START])

subgraph Axis1 [Axis 1: Locus of Control]
direction TB
A1_Q1[A1_Q1]
A1_Q2[A1_Q2]
A1_Q3[A1_Q3]
A1_D1{A1_D1}
A1_ADAPTIVE[A1_ADAPTIVE]
A1_D2{A1_D2}
A1_REF_INT[[A1_REF_INT]]
A1_REF_EXT[[A1_REF_EXT]]
BRIDGE_1_2(BRIDGE_1_2)
end

subgraph Axis2 [Axis 2: Orientation]
direction TB
A2_Q1[A2_Q1]
A2_Q2[A2_Q2]
A2_D1{A2_D1}
A2_ADAPTIVE[A2_ADAPTIVE]
A2_ADAPTIVE1[A2_ADAPTIVE1]
A2_D2{A2_D2}
A2_REF_CONTRIB[[A2_REF_CONTRIB]]
A2_REF_ENT[[A2_REF_ENT]]
BRIDGE_2_3(BRIDGE_2_3)
end

subgraph Axis3 [Axis 3: Radius]
direction TB
A3_Q1[A3_Q1]
A3_Q2[A3_Q2]
A3_D1{A3_D1}
A3_ADAPTIVE[A3_ADAPTIVE]
A3_ADAPTIVE1[A3_ADAPTIVE1]
A3_D2{A3_D2}
A3_REF_OTHERS[[A3_REF_OTHERS]]
A3_REF_SELF[[A3_REF_SELF]]
end

SUMMARY[[SUMMARY]]
END([END])

START --> A1_Q1
A1_Q1 --> A1_Q2
A1_Q2 --> A1_Q3
A1_Q3 --> A1_D1

A1_D1 -->|internal > external| A1_REF_INT
A1_D1 -->|external > internal| A1_REF_EXT
A1_D1 -->|otherwise| A1_ADAPTIVE

A1_ADAPTIVE --> A1_D2
A1_D2 -->|internal >= external| A1_REF_INT
A1_D2 -->|external > internal| A1_REF_EXT

A1_REF_INT --> BRIDGE_1_2
A1_REF_EXT --> BRIDGE_1_2
BRIDGE_1_2 --> A2_Q1

A2_Q1 --> A2_Q2
A2_Q2 --> A2_D1

A2_D1 -->|contribution > entitlement| A2_REF_CONTRIB
A2_D1 -->|entitlement > contribution| A2_REF_ENT
A2_D1 -->|otherwise| A2_ADAPTIVE

A2_ADAPTIVE --> A2_ADAPTIVE1
A2_ADAPTIVE1 --> A2_D2

A2_D2 -->|contribution >= entitlement| A2_REF_CONTRIB
A2_D2 -->|entitlement > contribution| A2_REF_ENT

A2_REF_CONTRIB --> BRIDGE_2_3
A2_REF_ENT --> BRIDGE_2_3
BRIDGE_2_3 --> A3_Q1

A3_Q1 --> A3_Q2
A3_Q2 --> A3_D1

A3_D1 -->|others > self| A3_REF_OTHERS
A3_D1 -->|self > others| A3_REF_SELF
A3_D1 -->|otherwise| A3_ADAPTIVE

A3_ADAPTIVE --> A3_ADAPTIVE1
A3_ADAPTIVE1 --> A3_D2

A3_D2 -->|others >= self| A3_REF_OTHERS
A3_D2 -->|self > others| A3_REF_SELF

A3_REF_OTHERS --> SUMMARY
A3_REF_SELF --> SUMMARY
SUMMARY --> END
```