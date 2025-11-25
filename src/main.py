# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
# ]
# ///


__app_name__ = "West of Loathing Save Editor"
__author__ = "AbsoluteWinter"
__license__ = "GPL-3.0"
__version__ = "0.1.0"
__version_build__ = "20251125"


# MARK: Library
# ------------------------------------------------------------------------------------------------------------------------------------
import json
import os
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Literal, TypedDict, cast

# MARK: Setup
# ------------------------------------------------------------------------------------------------------------------------------------
DEFAULT_PATH = Path(os.getenv("USERPROFILE", "")).joinpath(
    "Appdata", "LocalLow", "Asymmetric Software", "West of Loathing"
)


class StatusCode(StrEnum):
    OK = "OK"
    ERROR = "ERROR"


SKILL_CATEGORY: dict[int, str] = {
    0: "all",
    1: "cow puncher",
    2: "beanslinger",
    3: "snake oiler",
    4: "necromancer",
}


@dataclass
class Skill:
    id: str
    max_lvl: Literal[1, 3, 5, 7]
    category: Literal[0, 1, 2, 3, 4]
    is_perk: bool = field(default=False)


SKILLS_AND_PERKS: list[tuple] = [
    ("badmedicine", 5, 3),
    ("beangolem", 5, 2),
    ("beanshield", 5, 2),
    ("beanwall", 5, 2),
    ("beefup", 5, 1),
    ("bloodbeans", 5, 2),
    ("stomp", 5, 1),
    ("butterbean", 5, 2),
    ("darkhowdy", 3, 4),
    ("deadeye", 7, 3),
    ("summonsnake", 5, 3),
    ("dickerin", 5, 0),
    ("pokercheatin", 5, 0),
    ("fanhammer", 5, 3),
    ("first_aid", 5, 1),
    ("foragin", 3, 0),
    ("goodmedicine", 5, 3),
    ("gore", 5, 1),
    ("blizzard", 5, 2),
    ("spectralskull", 3, 4),
    ("haymaker", 5, 1),
    ("hellbender", 7, 2),
    ("hornswogglin", 5, 3),
    ("intimidatin", 5, 1),
    ("lavafava", 5, 2),
    ("leatherworkery", 3, 1),
    ("lockpickin", 3, 0),
    ("cookery", 3, 2),
    ("moo", 5, 1),
    ("outfoxin", 5, 2),
    ("potionery", 3, 3),
    ("quickdraw", 5, 3),
    ("rainofteeth", 3, 4),
    ("safecrackin", 5, 0),
    ("shootenanny", 5, 3),
    ("snakewhip", 5, 3),
    ("strongmedicine", 5, 3),
    ("onetwothree", 5, 1),
    ("thickskin", 5, 1),
    ("tough_customer", 7, 1),
    ("usetheoldbean", 5, 2),
    ("vampiricyodel", 3, 4),
    ("wary", 5, 2),
    ("anatomy", 1, 0, True),
    ("skullwhisperer", 1, 0, True),
    ("hedgenewsperk", 1, 0, True),
    ("bigspleen", 1, 3, True),
    ("bovicusboon", 1, 0, True),
    ("hedgeperk", 1, 0, True),
    ("brawny", 1, 1, True),
    ("cowrruption", 1, 0, True),
    ("duellaw", 1, 0, True),
    ("vigilant", 1, 1, True),
    ("poisoner", 1, 3, True),
    ("silversmithin", 1, 0, True),
    ("horsefriend", 1, 0, True),
    ("gluttonforpunishment", 1, 0, True),
    ("goblintongue", 1, 0, True),
    ("greenthumb", 1, 0, True),
    ("gunlaw", 1, 0, True),
    ("cairnperk_mus", 1, 0, True),
    ("cairnperk_mox", 1, 0, True),
    ("hedgingyourbets", 1, 0, True),
    ("honorable", 1, 0, True),
    ("kelloggpower", 1, 0, True),
    ("kurtzmox", 1, 0, True),
    ("kurtzmyst", 1, 0, True),
    ("kurtzmuscle", 1, 0, True),
    ("toiletmaster", 1, 0, True),
    ("minesplainer", 1, 0, True),
    ("cactusskin", 1, 0, True),
    ("book_boots", 1, 0, True),
    ("mycology", 1, 0, True),
    ("percussive", 1, 0, True),
    ("book_brewery", 1, 0, True),
    ("summonskeleton1", 1, 4, True),
    ("summonskeleton3", 1, 4, True),
    ("summonskeleton2", 1, 4, True),
    ("book_curiosity", 1, 0, True),
    ("ruthless", 1, 0, True),
    ("silvertongue", 1, 0, True),
    ("cairnperk_myst", 1, 0, True),
    ("spitfree", 1, 0, True),
    ("spittoonhand", 1, 0, True),
    ("walkingstupid", 1, 0, True),
    ("book_cook", 1, 0, True),
    ("uncanny", 1, 2, True),
    ("unlimitedbones", 1, 0, True),
    ("unlimitedgrain", 1, 0, True),
    ("richvein", 1, 0, True),
    ("book_tanner", 1, 0, True),
]


# MARK: Data format
# ------------------------------------------------------------------------------------------------------------------------------------
_SaveDataPlayerFlags = TypedDict(
    "_SaveDataPlayerFlags",
    {"firstname": str, "lastname": str, "class": str, "xp": str, "meat": str},
)


class _SaveDataPlayerGear(TypedDict):
    hat: int
    lapel: int
    pistol: int
    weapon: int
    offhand: int
    ring: int
    pants: int
    boots: int


class _SaveDataPlayer(TypedDict):
    flags: _SaveDataPlayerFlags
    dailyflags: dict[str, str]
    items: dict[str, dict[str, str]]
    gear: _SaveDataPlayerGear
    effects: dict[str, int]
    skills: dict[str, int]
    stores: dict[str, dict[str, str | dict[str, dict[str, str]]]]
    properties: list[str]


class SaveData(TypedDict):
    """Main save data"""

    PLAYER: _SaveDataPlayer
    WAA_ID: str


# MARK: Save editor
# ------------------------------------------------------------------------------------------------------------------------------------
class WoLSE:
    """
    West of Loathing Save Editor


    Usage:
    ------
    >>> engine = WoLSE(<path to save folder>)
    >>> engine.select_save(<save slot>)
    >>> engine.unlock_all_skill_perk()
    >>> engine.save()
    """

    STRONG_ENCHANTMENT: ClassVar = {
        "enchantments": {
            "muscle": "20",
            "mysticality": "20",
            "moxie": "20",
            "maxhp": "50",
            "maxap": "2",
            "armor": "20",
            "meleebonus": "20",
            "spellbonus": "20",
            "rangedbonus": "20",
            "speed": "5",
            "meatbonus": "20",
            "itembonus": "20",
            "hotresist": "-40",
            "coldresist": "-40",
            "spookyresist": "-40",
            "stenchresist": "-40",
            "sleazeresist": "-40",
            "id": "enchantments",
        }
    }
    SKILLS: ClassVar = [Skill(*x) for x in SKILLS_AND_PERKS]

    def __init__(self, source_path: str | Path | None = None) -> None:
        self.source_path = DEFAULT_PATH if source_path is None else Path(source_path)

        self.status = StatusCode.OK
        if not self.source_path.exists():
            self.status = StatusCode.ERROR

        # Post
        self._save_data: SaveData = {}
        self._selected_save = None

    def __repr__(self) -> str:
        cname = self.__class__.__name__

        try:
            info = self._read_info()
            name = f"{info['firstname']} {info['lastname']}"
            fname = f"{name} the {SKILL_CATEGORY.get(int(info['class'])).title()}"
            xp = int(info["xp"])
            meat = int(info["meat"])
            return f"{cname}({fname} |  XP: {xp:,}, M: {meat:,})"
        except Exception:
            return f"{cname}({self._selected_save})"

    # Load
    @property
    def available_saves(self) -> list[Path]:
        """Available save files"""
        if self.status == StatusCode.OK:
            paths = list(self.source_path.glob("*save-*.json"))
            return paths
        return []

    def _load_save_data(self, slot: int) -> None:
        with self.available_saves[slot].open("r", encoding="utf-8") as file:
            self._save_data = cast(SaveData, json.load(file))
        self._selected_save = self.available_saves[slot]

    def _read_info(self) -> _SaveDataPlayerFlags:
        """
        Read basic save info

        Returns
        -------
        _SaveDataPlayerFlags
            Save info (name, class, xp, meat)
        """
        keys = ["firstname", "lastname", "class", "xp", "meat"]
        fl = self._save_data["PLAYER"]["flags"]
        info = {v: fl[v] for v in keys}
        return info

    def select_save(self, save_number: int) -> None:
        if save_number > len(self.available_saves):
            raise ValueError("Invalid save slot")

        self._load_save_data(slot=save_number)

    # Save
    def save(self) -> None:
        save_data = json.dumps(self._save_data, indent=2)
        with self._selected_save.open("w", encoding="utf-8") as f:
            f.write(save_data)

    # Skills and perks
    def _unlock_sp(self, skill: Skill, max_level: bool = False) -> None:
        """
        Unlock a skill or perk
        """
        mlvl = skill.max_lvl if max_level else 1
        self._save_data["PLAYER"]["skills"][skill.id] = mlvl

    def _unlock_all_skills_and_perks(
        self,
        include_necro: bool = True,
        include_perk: bool = True,
        perk_only: bool = False,
        max_level: bool = True,
        class_resticted: bool = True,
    ) -> None:
        """
        Unlock all skills and perks for save file

        Parameters
        ----------
        include_necro : bool, optional
            Include Necromancy skills and perks (positive ones), by default ``True``

        include_perk : bool, optional
            Include perks, by default ``True``

        perk_only : bool, optional
            Only unlock perks (will overwrite ``include_perk``), by default ``False``

        max_level : bool, optional
            Unlock everything to its max level, by default ``True``

        class_resticted : bool, optional
            Only unlock skills and perks that suitable for character's class, by default ``True``


        Example:
        --------
        To unlock everything
        >>> _unlock_all_skills_and_perks(max_level=True, class_resticted=False)
        """
        plr_class = int(self._read_info()["class"])
        plr_sk = self._save_data["PLAYER"]["skills"]

        for x in self.SKILLS:
            # Check if exist
            if not max_level and x.id in plr_sk:
                continue

            # Class restriction check
            if class_resticted:
                cate = (plr_class, 0, 4) if include_necro else (plr_class, 0)
                if not x.category in cate:
                    continue

            # Perk filtering
            if perk_only:
                include_perk = True
                if not x.is_perk:
                    continue

            if not include_perk and x.is_perk:
                continue

            self._unlock_sp(x, max_level=max_level)

    def unlock_all_perks(self) -> None:
        self._unlock_all_skills_and_perks(
            max_level=False,
            include_necro=False,
            perk_only=True,
            class_resticted=True,
        )

    def unlock_all_class_skills(self) -> None:
        self._unlock_all_skills_and_perks(
            max_level=False,
            include_necro=False,
            include_perk=False,
            class_resticted=True,
        )

    def unlock_all_necro_skills(self) -> None:
        """
        Unlock all necromancer skills and perks (positive ones)
        """
        plr_sk = self._save_data["PLAYER"]["skills"]
        for x in self.SKILLS:
            if x.category == 4 and x.id not in plr_sk:
                self._unlock_sp(x, max_level=False)

    def unlock_all_skill_perk(self) -> None:
        """
        Unlock every skills and perks
        """
        self._unlock_all_skills_and_perks(max_level=True, class_resticted=False)


# MARK: Run
# ------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    pass
