with open("agent.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """    # Algorithmic check against supported crops and states
    if crop not in VALID_CROPS or state not in VALID_STATES:
        return Event(route="invalid", output="The requested crop or state is not supported or recognized.")"""

new = """    # Algorithmic check against supported crops and states
    if crop not in VALID_CROPS or state not in VALID_STATES:
        return Event(
            route="invalid",
            output=(
                f"The user asked about the crop \x27{crop}\x27 in the state \x27{state}\x27. "
                f"This crop and/or state is not supported or recognized. "
                f"Politely tell the user this specific crop or state is not supported, "
                f"and list the supported crops."
            ),
        )"""

if old in content:
    content = content.replace(old, new)
    with open("agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully: decline message now includes specific crop/state.")
else:
    print("WARNING: exact block not found -- no changes made.")
