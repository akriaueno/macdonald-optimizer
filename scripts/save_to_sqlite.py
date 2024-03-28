#!/usr/bin/env python3

import json
import sqlite3
import sys


def create_tables(con):
    with con:
        con.execute("DROP TABLE IF EXISTS menu;")
        con.execute("DROP TABLE IF EXISTS nutrient;")
        con.execute("DROP TABLE IF EXISTS nutrient_type;")
        con.execute(
            "CREATE table menu (id INTEGER PRIMARY KEY, name STRING, price INTEGER);"
        )
        con.execute(
            "CREATE table nutrient_type (id INTEGER PRIMARY KEY, name STRING, unit STREING);",
        )
        con.execute(
            "CREATE table nutrient ("
            "  menu_id INTEGER,"
            "  nutrient_type_id,"
            "  value REAL)"
        )


def insert_data(con, menu_data, nutrient_type_data):
    menus = []
    nutrients = []
    for menu in menu_data:
        menus.append((menu["id"], menu["name"], menu["price"]))
        for nutrient in menu["nutrients"]:
            if nutrient["value"] == "-":
                nutrient["value"] = 0
            nutrients.append((menu["id"], nutrient["id"], nutrient["value"]))
    nutrient_types = []
    for nutrient_type in nutrient_type_data:
        nutrient_types.append(
            (nutrient_type["id"], nutrient_type["name"], nutrient_type["unit"])
        )
    try:
        with con:
            con.executemany("INSERT INTO menu(id, name, price) VALUES (?, ?, ?)", menus)
            con.executemany(
                "INSERT INTO nutrient_type(id, name, unit) VALUES (?, ?, ?)",
                nutrient_types,
            )
            con.executemany(
                "INSERT INTO nutrient(menu_id, nutrient_type_id, value) VALUES (?, ?, ?)",
                nutrients,
            )
    except Exception:
        import traceback

        traceback.print_exc(file=sys.stdout)


def read_data(menu_file, nutrient_file):
    with open(menu_file) as f:
        menu_data = json.load(f)["product_menu"]
    with open(nutrient_file) as f:
        nutrient_type_data = json.load(f)["data"]

    menu_data_slim = []
    for menu in menu_data:
        if "nutrient" not in menu:
            continue
        menu_data_slim.append(
            {
                "id": menu["id"],
                "name": menu["print_name"],
                "price": menu["price"],
                "nutrients": menu["nutrient"],
            }
        )

    nutrient_type_data_slim = []
    for nutrient_type in nutrient_type_data:
        if "unit" not in nutrient_type:
            continue
        nutrient_type_data_slim.append(
            {
                "id": nutrient_type["nutrient_id"],
                "name": nutrient_type["name"],
                "unit": nutrient_type["unit"],
            }
        )

    return menu_data_slim, nutrient_type_data_slim


if __name__ == "__main__":
    menu_file = "../data/product_menu.json"
    nutrient_file = "../data/nutrient.json"
    menu_data, nutrient_type_data = read_data(menu_file, nutrient_file)
    db = "../data/mcdonalds.sqlite"
    con = sqlite3.connect(db)
    create_tables(con)
    insert_data(con, menu_data, nutrient_type_data)
