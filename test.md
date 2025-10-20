{'Init': [{'trigger': 'Homed', 'condition': '!isScoringTestMode()', 'destination': 'Idle'}, {'trigger': 'Homed', 'condition': 'isScoringTestMode()', 'destination': 'TestMode'}, {'trigger': 'ForceInit', 'destination': 'Idle'}], 'Idle': [{'trigger': 'StartWarmup', 'condition': 'hasGamePiece()', 'destination': 'Warmup'}, {'trigger': 'TestModeEntered', 'condition': 'isScoringTestMode()', 'destination': 'TestMode'}], 'TestMode': [{'trigger': 'TestModeExitted', 'condition': '!isScoringTestMode()', 'destination': 'Idle'}], 'Warmup': [{'trigger': 'WarmupCancelled', 'destination': 'Idle'}, {'trigger': 'WarmupReady', 'condition': 'hasGamePiece() && warmupReady()', 'destination': 'Score'}], 'Score': [{'trigger': 'DoneScoring', 'condition': '!hasGamePiece()', 'destination': 'Idle'}, {'trigger': 'WarmupCancelled', 'destination': 'Idle'}]}
```mermaid
flowchart LR

classDef state font-size:40px,padding:10px

    Init -->|Homed| InitCondition0{"!isScoringTestMode()"}
    InitCondition0{"!isScoringTestMode()"} -.->|true| Idle
    InitCondition1{"isScoringTestMode()"} -.->|true| TestMode
    InitCondition0{"!isScoringTestMode()"} -.->|false| InitCondition1{"isScoringTestMode()"}
    Init -->|ForceInit| Idle
    Idle -->|StartWarmup| IdleCondition0{"hasGamePiece()"}
    IdleCondition0{"hasGamePiece()"} -.->|true| Warmup
    Idle -->|TestModeEntered| IdleCondition1{"isScoringTestMode()"}
    IdleCondition1{"isScoringTestMode()"} -.->|true| TestMode
    TestMode -->|TestModeExitted| TestModeCondition0{"!isScoringTestMode()"}
    TestModeCondition0{"!isScoringTestMode()"} -.->|true| Idle
    Warmup -->|WarmupCancelled| Idle
    Warmup -->|WarmupReady| WarmupCondition0{"hasGamePiece() && warmupReady()"}
    WarmupCondition0{"hasGamePiece() && warmupReady()"} -.->|true| Score
    Score -->|DoneScoring| ScoreCondition0{"!hasGamePiece()"}
    ScoreCondition0{"!hasGamePiece()"} -.->|true| Idle
    Score -->|WarmupCancelled| Idle
```
