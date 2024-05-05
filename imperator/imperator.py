import os
import random
import csv
from enum import Enum

from krita import Krita, Extension, ManagedColor  # type: ignore

PROVINCE_DEFINITION_FILE = "path/to/definition.csv"
DEFAULT_MAP_FILE = "path/to/default.map"
PROVINCE_SETUP_FILE = "path/to/00_india_region.txt"

class ProvinceType(Enum):
    land = "land"
    sea = "sea"
    impassable_terrain = "impassable_terrain"
    river = "river"


def get_all_colors():
    rgb_tuples = set()
    final_id = 1
    with open(PROVINCE_DEFINITION_FILE, mode="r", encoding="utf-8") as csvfile:
        lines = csvfile.readlines()

    csv_reader = csv.reader(lines, delimiter=";", skipinitialspace=True)
    for row in csv_reader:
        rgb_tuple = tuple(map(int, row[1:4]))
        rgb_tuples.add(rgb_tuple)
        if len(row) > 0 and row[0].isdecimal():
            current_id = int(row[0])
            if current_id > final_id:
                final_id = current_id

    return rgb_tuples, final_id


def update_definition_file(new_id, color):
    with open(PROVINCE_DEFINITION_FILE, mode="r", encoding="utf-8") as file:
        lines = file.read()

    lines += "\n"
    lines += f"{new_id};{color[2]};{color[1]};{color[0]};x;x;;;;;;;;;;;;;;;;;;;,"

    with open(PROVINCE_DEFINITION_FILE, mode="w", encoding="utf-8") as file:
        file.write(lines.replace("\n\n", f"{os.linesep}"))

def update_default_map_file(new_id, province_type: ProvinceType):
    with open(DEFAULT_MAP_FILE, mode="r", encoding="utf-8") as file:
        lines = file.read()

    lines += "\n"
    if province_type.name == "impassable_terrain":
        lines += f"impassable_terrain = LIST {{ {new_id} }}"
    elif province_type.name == "sea":
        lines += f"sea_zones = LIST {{ {new_id} }}"
    elif province_type.name == "river":
        lines += f"river_provinces = LIST {{ {new_id} }}"


    with open(DEFAULT_MAP_FILE, mode="w", encoding="utf-8") as file:
        file.write(lines.replace("\n\n", f"{os.linesep}"))

def update_province_setup_file(new_id, province_type: ProvinceType):
    with open(PROVINCE_SETUP_FILE, mode="r", encoding="utf-8") as file:
        lines = file.read()

    civ_value = 0 if province_type.name != "land" else 10
    province_rank = "" if province_type.name != "land" else "settlement"
    trade_good = "" if province_type.name != "land" else "wood"
    culture = "" if province_type.name != "land" else "magadhi"
    religion = "" if province_type.name != "land" else "buddhism"
    terrain = ""
    pops = ""
    if province_type.name == "impassable_terrain":
        terrain = "impassable_terrain"
    elif province_type.name == "land":
        terrain = "plains"
        pops = "\n\tfreemen = {\n\t\tamount = 1\n\t}"
    elif province_type.name == "river":
        terrain = "riverine_terrain"
    elif province_type.name == "sea":
        terrain = "ocean"

    new_province = f"""{new_id}={{
    barbarian_power=0
    civilization_value={civ_value}
    culture="{culture}"
    province_rank="{province_rank}"
    religion="{religion}"
    terrain="{terrain}"
    trade_goods="{trade_good}"{pops}
}}"""
    lines += "\n"
    lines += new_province

    with open(PROVINCE_SETUP_FILE, mode="w", encoding="utf-8") as file:
        file.write(lines.replace("\n\n", f"{os.linesep}"))

def create_new_province(province_type: ProvinceType):
    all_colors, final_id = get_all_colors()

    while True:
        if province_type.name == "sea" or province_type.name == "river":
            rand_color = (
                random.randint(75, 200),
                random.randint(1, 50),
                random.randint(1, 50),
            )
        elif province_type.name == "impassable_terrain":
            rand_color = (
                random.randint(1, 50),
                random.randint(1, 50),
                random.randint(1, 50),
            )
        else:
            rand_color = (
                random.randint(1, 150),
                random.randint(1, 150),
                random.randint(1, 150),
            )
        if rand_color not in all_colors:
            color = ManagedColor("RGBA", "U8", "")
            color_components = color.components()

            color_components[0] = rand_color[0] / 255
            color_components[1] = rand_color[1] / 255
            color_components[2] = rand_color[2] / 255
            color_components[3] = 1.0  # Alpha component

            view = Krita().activeWindow().activeView()
            color.setComponents(color_components)
            view.setForeGroundColor(color)
            new_id = final_id + 1
            update_definition_file(new_id, rand_color)
            update_province_setup_file(new_id, province_type)
            if province_type.name in ("sea", "impassable_terrain", "river"):
                update_default_map_file(new_id, province_type)
            return


class Imperator(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        self._create_action(window, "Create Land Province", self.create_land_province)
        self._create_action(window, "Create Sea Province", self.create_sea_province)
        self._create_action(window, "Create Impassable Province", self.create_impassable_terrain_province)
        self._create_action(window, "Create River Province", self.create_river_province)

    def _create_action(self, window, name, callback):
        action = window.createAction(name, name, "tools")
        action.triggered.connect(callback)

    def create_land_province(self):
        create_new_province(ProvinceType("land"))

    def create_sea_province(self):
        create_new_province(ProvinceType("sea"))

    def create_impassable_terrain_province(self):
        create_new_province(ProvinceType("impassable_terrain"))

    def create_river_province(self):
        create_new_province(ProvinceType("river"))
