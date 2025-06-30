- **For marimo notebooks**: See `MARIMO_RULES.md` for specific marimo conventions

### 🚨 CRITICAL MARIMO RULE - NEVER VIOLATE

**BEFORE writing ANY marimo cell, check:**
1. Are you putting `mo.md()`, `mo.ui.table()`, or ANY display function inside `if`, `try`, `for`, `while`, or `with` blocks?
2. If YES → STOP! You must prepare content inside control blocks, then display OUTSIDE them.

**Template pattern:**
```python
@app.cell
def _(mo):
    # Prepare content inside control blocks
    if condition:
        content = "success message"
    else:
        content = "error message"
    
    # Display OUTSIDE control blocks, BEFORE return
    mo.md(content)
    return
```

**Use notebooks/TEMPLATE.py as starting point for new marimo notebooks.**
