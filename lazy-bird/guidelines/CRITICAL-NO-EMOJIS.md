# CRITICAL RULE: ABSOLUTELY NO EMOJIS

**PRIORITY: CRITICAL**
**APPLIES TO: ALL CODE, COMMENTS, DOCUMENTATION, DATA**

---

## THE RULE

**NEVER, EVER USE EMOJIS ANYWHERE**

Period. No exceptions. No discussions.

---

## WHAT THIS MEANS

### EMOJIS = ERRORS

When you see an emoji in:
- Code
- Comments
- Documentation
- Database data
- API responses
- Log messages
- ANY file

YOU SEE A **CRITICAL ERROR** THAT MUST BE FIXED IMMEDIATELY.

---

## WHY NO EMOJIS

1. **Encoding Issues**: Windows uses CP1252, emojis cause UnicodeEncodeError
2. **Cross-Platform**: Not all terminals support emojis
3. **Professionalism**: Code is not a chat app
4. **Searchability**: Emojis break search/grep
5. **Accessibility**: Screen readers struggle with emojis

---

## CORRECT ALTERNATIVES

### Instead of Emojis in Documentation:

WRONG:
```markdown
# Status
- Done
- In Progress
- Failed
```

CORRECT:
```markdown
# Status
- [DONE]
- [IN PROGRESS]
- [FAILED]
```

### Instead of Emojis as Icons (Database):

WRONG:
```python
icon = "lightning bolt emoji"
```

CORRECT:
```python
icon = "lightning"  # Icon name, frontend renders it
```

### Instead of Emojis in Logs:

WRONG:
```python
print("Seeding database...")
```

CORRECT:
```python
print("Seeding database...")
```

### Instead of Emojis in UI Data:

WRONG:
```json
{
  "preset": "speed",
  "icon": "zap emoji"
}
```

CORRECT:
```json
{
  "preset": "speed",
  "icon": "zap"
}
```

---

## ENFORCEMENT

1. **Code Review**: Reject ANY PR with emojis
2. **Linting**: Add emoji detection to linters
3. **Guidelines**: This rule is HIGHER priority than any other guideline
4. **Existing Code**: If you find emojis in existing code, FIX THEM IMMEDIATELY

---

## EXAMPLES OF VIOLATIONS

ALL OF THESE ARE ERRORS:

```python
# ERROR: Emoji in comment

def process():
    pass  # Processing... ERROR

print("Done!")  # ERROR
```

```markdown
# README.md

## Features ERROR

- Fast processing ERROR
- Low cost ERROR
```

```python
# seed_data.py
presets = [
    {"icon": "lightning", "name": "fast"}  # ERROR: Emoji in data
]
```

---

## CORRECT APPROACH

Use words, symbols, or icon names:

```python
# CORRECT: Text markers
# [SUCCESS] Processing complete
# [ERROR] Failed to connect
# [INFO] Starting service

print("[SUCCESS] Database seeded")
print("[ERROR] Connection failed")
```

```python
# CORRECT: Icon names for UI
icon_map = {
    "speed": "lightning",
    "cost": "dollar-sign",
    "quality": "target",
    "balanced": "scale"
}
```

---

## REMEMBER

**EMOJIS ARE NOT "CUTE" OR "VISUAL" OR "USER-FRIENDLY"**

**EMOJIS ARE ERRORS**

When you see one, fix it immediately, no questions asked.

---

**THIS RULE OVERRIDES ALL OTHER GUIDELINES**
