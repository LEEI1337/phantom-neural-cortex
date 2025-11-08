# LAYER 3 - Rover Orchestration

**Erbt von:** LAYER-0 + LAYER-1 + LAYER-2
**Gilt für:** Tasks die über Rover laufen

## Rover-Spezifische Regeln
- Git Worktree Isolation (PFLICHT)
- Docker Container für Execution
- Test Validation VOR Merge
- Automatisches Cleanup nach Task

## Rover CLI Format
```bash
rover task "description" --agent <claude|gemini|copilot>
```

**Nächster Layer:** LAYER-4.md (Lazy Bird)
