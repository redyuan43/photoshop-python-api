#!/usr/bin/env python
"""Helper script to run a recorded Photoshop action."""

from photoshop import Session

ACTION_NAME = "ApplyCyanotype"
ACTION_SET = "MyHuePresets"


def main() -> None:
    with Session() as ps:
        script = f'app.doAction("{ACTION_NAME}", "{ACTION_SET}");'
        ps.app.doJavaScript(script)
        print(f"[OK] 已执行动作 {ACTION_SET}/{ACTION_NAME}")


if __name__ == "__main__":
    main()
