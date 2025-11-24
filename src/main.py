"""
West of Loathing Save editor
"""

# MARK: Library
import os
from pathlib import Path
from typing import TypedDict

from absfuyu.util.path import DirectoryBase

DEFAULT_PATH = Path(os.getenv("USERPROFILE", "")).joinpath(
    "Appdata", "LocalLow", "Asymmetric Software", "West of Loathing"
)


# MARK: Data format
class _SaveDataPlayer(TypedDict):
    flags: dict
    dailyflags: dict
    items: dict
    gear: dict
    effects: dict
    skills: dict
    stores: dict
    properties: list


class SaveData(TypedDict):
    """Main save data"""

    PLAYER: _SaveDataPlayer
    WAA_ID: str


# MARK: Save editor
class WoLSE(DirectoryBase):
    pass


# MARK: Run
if __name__ == "__main__":
    from rich import print

    print(DEFAULT_PATH)
