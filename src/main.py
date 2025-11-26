# /// script
# requires-python = ">=3.11"
# ///


__app_name__ = "West of Loathing Save Editor"
__author__ = "AbsoluteWinter"
__license__ = "GPL-3.0"
__version__ = "0.4.0"
__version_build__ = "20251126"

# TODO
# - Unlock all setting
# - Unlock all elvibrato language


# MARK: Library
# ------------------------------------------------------------------------------------------------------------------------------------
import json
import os
import tkinter as tk
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from tkinter import filedialog, ttk
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

ELV_WORDS = """\
TOILET,DESTINATION,INCREASE,SOLAR,OFFLINE,MUNICIPAL,INSUFFICIENT,DECLOAKER,SEDATIVE,INITIALIZE,CONTAINMENT,ORIENTATION,BEACON,REACTOR,
DRONE,TIMESQUEEZER,TEMPERATURE,FACILITY,SECONDARY,PIPELINE,ADJUSTMENT,EQUIPMENT,MACHINE,INSERT,RETURN,CACHE,REFRESHMENT,SOURCE,DETECTED,
UPDATED,TOGGLE,MILITARY,FLUID,WEST,BROOCH,ARRAY,LOCAL,CANNON,SOUTH,WEATHER,SELECT,CLOTHING,HEADWEAR,CENTRAL,BRACELET,CONSTRUCTION,
SUSTENANCE,POSITRONIC,RESONATOR,QUICKGATE,PERSONNEL,ANTIPSYCHOTIC,EMERGENCY,EXTRATERRESTRIAL,TELEPORTER,CHRONOKEY,FABRICATION,CORRUPTION,
PLANETARY,ROBERTO,TERMINAL,MAGNITUDE,GARBAGE,ORGANIC,MAINTENANCE,STORAGE,LEGSWEAR,PRIMARY,DESTRUCTION,EAST,AUDITORY,BRIDGE,FOOTWEAR,
COFFEEMAKER,ONLINE,DISPOSAL,NORTH,MATTER,EDUCATION,CURRENT,NUISANCE,DECREASE,SYSTEM,POWER
"""

CONFIG: dict[str, str] = {
    "option_stupidwalking": "1",
    "option_sepiatone": "1",
    "collect_hat_hat_barelyenchanted": "1",
    "tutskip": "1",
    "tutskip_maxmeat": "1337",
    "tutskip_turnip": "1",
    "tutskip_board": "1",
    "tutskip_deputypistol": "1",
    "tutskip_nastyring": "1",
    "tutskip_shovel": "1",
    "tutskip_crowbar": "1",
    "tutskip_skinningknife": "1",
    "tutskip_cavalrysaber": "1",
    "tutskip_sherfbadge": "1",
    "tutskip_silvercufflinks": "1",
    "tutskip_pocketwatch": "1",
    "tutskip_honorable": "1",
    "tutskip_ruthless": "1",
    "tutskip_goblintongue": "1",
    "tutskip_quest_curly": "1",
    "tutskip_susie": "1",
    "tutskip_alice": "1",
    "tutskip_gary": "1",
    "tutskip_darkhorse": "1",
    "tutskip_palehorse": "1",
    "tutskip_crazyhorse": "1",
    "tutskip_hardmode": "1",
    "tutskip_maxneedles": "3",
    "bonebridge": "1",
    "collect_hat_quest_billhelmet": "1",
    "collect_hat_hat_sloppychef": "1",
    "collect_hat_hat_fakepope": "1",
    "collect_hat_hat_cavalry": "1",
    "collect_hat_hat_oldmilitary": "1",
    "collect_hat_hat_hippy": "1",
    "collect_hat_hat_gasmask": "1",
    "collect_hat_hat_prototype": "1",
    "collect_hat_hat_silverturnip": "1",
    "collect_hat_hat_crackerjack": "1",
    "collect_hat_hat_elvheadband": "1",
    "collect_hat_hat_ghosthat": "1",
    "collect_hat_hat_chef": "1",
    "collect_hat_hat_kurtzfit": "1",
    "collect_hat_hat_viking": "1",
    "collect_hat_hat_blackhood": "1",
    "collect_hat_hat_robertomask": "1",
    "collect_hat_hat_robertoleader": "1",
    "collect_hat_hat_elv": "1",
    "collect_hat_hat_necrocrown": "1",
    "collect_hat_hat_mining": "1",
    "collect_hat_hat_yeasty": "1",
    "collect_hat_hat_spittoon": "1",
    "collect_hat_hat_burning": "1",
    "collect_hat_hat_electric": "1",
    "collect_hat_hat_hexrock": "1",
    "collect_hat_hat_4gallon": "1",
    "collect_hat_hat_floppyderby": "1",
    "collect_hat_hat_hard": "1",
}

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
    >>> engine.unlock_all_config()
    >>> engine.unlock_all_skill_perk()
    >>> engine.unlock_el_vibrato_words()
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
        self._config_data: dict[str, str] = {}
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
    # ------------------------------------
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
        info = {v: fl.get(v, "0") for v in keys}
        return info

    def select_save(self, save_number: int) -> None:
        if save_number > len(self.available_saves):
            raise ValueError("Invalid save slot")

        self._load_save_data(slot=save_number)

    # Save
    # ------------------------------------
    def save(self) -> None:
        save_data = json.dumps(self._save_data, indent=2)
        with self._selected_save.open("w", encoding="utf-8") as f:
            f.write(save_data)

    # Config data
    # ------------------------------------
    def unlock_all_config(self) -> None:
        """
        Unlock all game perma flag/config
        - Stupid walking option
        - Nostalgia option
        - Pardner option: Pete, Susie, Alice, Gary
        - Hard mode option
        - Honorable, Ruthless
        - All prologue unlockable items
        - All horses
        - 1337 Meat
        """
        if not self.status == StatusCode.OK:
            return None

        path = list(self.source_path.glob("*permaflags-*.json"))[0]
        with path.open("r", encoding="utf-8") as file:
            self._config_data = json.load(file)

        for k, v in CONFIG.items():
            if k not in self._config_data:
                self._config_data[k] = v

        with path.open("w", encoding="utf-8") as file:
            file.write(json.dumps(self._config_data, indent=2))

    # Skills and perks
    # ------------------------------------
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

    # Stat
    # ------------------------------------
    def set_xp(self, value: int) -> None:
        if isinstance(value, int):
            value = str(value)
        self._save_data["PLAYER"]["flags"]["xp"] = value

    def set_meat(self, value: int) -> None:
        if isinstance(value, int):
            value = str(value)
        self._save_data["PLAYER"]["flags"]["meat"] = value

    # Word
    # ------------------------------------
    def unlock_el_vibrato_words(self) -> None:
        """
        Unlock all El Vibrato words (normally unlocked by using punchcard)
        """
        words = [x.strip() for x in ELV_WORDS.split(",")]
        base = "word_elvibrato_"

        for x in words:
            key = f"{base}{x}"
            if not key in self._save_data["PLAYER"]["flags"]:
                self._save_data["PLAYER"]["flags"][key] = "1"


# MARK: GUI
# ------------------------------------------------------------------------------------------------------------------------------------
class SaveEditorGUI:
    """
    West of Loathing Save Editor - GUI
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"{__app_name__} by {__author__}")
        self.root.geometry("500x400")

        self._create_variables()
        self.create_widgets()

    # Variables
    # ------------------------------------
    def _create_variables(self) -> None:
        self.folder_var = tk.StringVar(value=DEFAULT_PATH.resolve())
        self.slot_var = tk.StringVar()
        self.input1_var = tk.StringVar()
        self.input2_var = tk.StringVar()
        self.cb1_var = tk.BooleanVar()
        self.cb2_var = tk.BooleanVar()

        self.save_engine = None

    # Main UI
    # ------------------------------------
    def create_widgets(self) -> None:

        # Folder Group
        folder_group = ttk.LabelFrame(self.root, text="Save Folder Selection")
        folder_group.pack(fill="x", padx=10, pady=8)

        ttk.Label(folder_group, text="Folder:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(folder_group, textvariable=self.folder_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Button(folder_group, text="Browse", command=self.browse_folder).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(folder_group, text="Load", command=self.load_folder).grid(
            row=0, column=3, padx=5
        )

        # Slot Group
        slot_group = ttk.LabelFrame(self.root, text="Save Slot")
        slot_group.pack(fill="x", padx=10, pady=8)

        ttk.Label(slot_group, text="Slot:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.slot_dropdown = ttk.Combobox(
            slot_group, textvariable=self.slot_var, values=[""], width=40
        )
        self.slot_dropdown.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(slot_group, text="Select", command=self.select_slot).grid(
            row=0, column=2, padx=5
        )

        # Inputs Group
        input_group = ttk.LabelFrame(self.root, text="XP & Meat")
        input_group.pack(fill="x", padx=10, pady=8)

        ttk.Label(input_group, text="XP:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        ttk.Entry(input_group, textvariable=self.input1_var, width=25).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(input_group, text="Meat:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        ttk.Entry(input_group, textvariable=self.input2_var, width=25).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Checkbox Group
        cb_group = ttk.LabelFrame(self.root, text="Skill & Perk")
        cb_group.pack(fill="x", padx=10, pady=8)

        ttk.Checkbutton(cb_group, text="Unlock all skills", variable=self.cb1_var).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Checkbutton(cb_group, text="Unlock all perks", variable=self.cb2_var).grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )

        # Save Button
        ttk.Button(self.root, text="Save", command=self.save_action).pack(pady=12)

    # Button Actions
    # ------------------------------------
    def browse_folder(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)

    def load_folder(self) -> None:
        print("Load folder:", self.folder_var.get())

        self.save_engine = WoLSE(self.folder_var.get())
        ss = [
            f"{i} - {x.stem}"
            for i, x in enumerate(self.save_engine.available_saves, start=1)
        ]
        self.slot_dropdown.config(values=ss)

    def select_slot(self) -> None:
        print("Selected slot:", self.slot_var.get())
        num = int(self.slot_var.get().split(" - ")[0])
        print(num)
        self.save_engine.select_save(num - 1)

        info = self.save_engine._read_info()
        self.input1_var.set(info.get("xp", "0"))
        self.input2_var.set(info.get("meat", "0"))

    def save_action(self) -> None:
        print("--- Saving Data ---")
        print("Folder:", self.folder_var.get())
        print("Slot:", self.slot_var.get())
        print("XP:", self.input1_var.get())
        print("Meat:", self.input2_var.get())
        print("Unlock all skills:", self.cb1_var.get())
        print("Unlock all perks:", self.cb2_var.get())

        self.save_engine.set_xp(self.input1_var.get())
        self.save_engine.set_meat(self.input2_var.get())

        unlock_sk = self.cb1_var.get()
        unlock_p = self.cb2_var.get()

        if unlock_sk:
            self.save_engine.unlock_all_class_skills()
        if unlock_p:
            self.save_engine.unlock_all_perks()
        self.save_engine.save()


# MARK: Run
# ------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()
    app = SaveEditorGUI(root)
    root.mainloop()
