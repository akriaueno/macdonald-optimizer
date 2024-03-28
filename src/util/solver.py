import mip
import sqlite3


def get_data(con):
    sql = """
    SELECT menu.id, menu.name, menu.price, nutrient_type.id, nutrient_type.name, nutrient.value, nutrient_type.unit FROM menu
      JOIN nutrient ON menu.id=nutrient.menu_id
      JOIN nutrient_type ON nutrient.nutrient_type_id=nutrient_type.id
    ORDER BY menu.id, nutrient_type.id;"""
    with con:
        cur = con.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    menus = {}
    nutrients = {}
    nutrient_types = {}
    for item in result:
        (
            id,
            name,
            price,
            nutrient_type_id,
            nutrient_type_name,
            nutrient_value,
            nutrient_type_unit,
        ) = item
        if id not in nutrients:
            nutrients[id] = {}
        menus[id] = {"name": name, "price": price}
        nutrients[id][nutrient_type_id] = nutrient_value
        nutrient_types[nutrient_type_id] = {
            "name": nutrient_type_name,
            "unit": nutrient_type_unit,
        }
    return menus, nutrients, nutrient_types


def solve(menus, nutrients, nutrient_targets):
    m = mip.Model()
    # Variables
    x = {id: m.add_var(name=f"{id}", var_type=mip.INTEGER) for id in menus.keys()}
    # Objective
    m.objective = mip.minimize(
        mip.xsum(val["price"] * x[id] for id, val in menus.items())
    )
    lb_diff = 0.1
    ub_diff = 0.1
    # Constraints
    for nt in nutrient_targets:
        nutrient_id = nt["id"]
        target = nt["target"]
        m.add_constr(
            mip.xsum(
                nutrients[menu_id][nutrient_id] * x[menu_id] for menu_id in menus.keys()
            )
            >= target * (1 - lb_diff)
        )
        m.add_constr(
            mip.xsum(
                nutrients[menu_id][nutrient_id] * x[menu_id] for menu_id in menus.keys()
            )
            <= target * (1 + ub_diff)
        )
    m.optimize()

    if not m.num_solutions:
        return
    result = {}
    for v in m.vars:
        if v.x > 0.99:
            menu_id = int(v.name)
            result[menu_id] = v.x
    return result


def print_result(menus, nutrients, nutrient_types, iresult):
    price = 0
    nutrient_values = {
        id: {"name": nt["name"], "value": 0} for id, nt in nutrient_types.items()
    }
    for menu_id, num in result.items():
        menu_name = menus[menu_id]["name"]
        menu_price = menus[menu_id]["price"]
        price += menu_price * num
        print(f"{menu_name}: {round(num)}個")
        for nutrient_type_id, nt in nutrient_types.items():
            nutrient_values[nutrient_type_id]["value"] += (
                nutrients[menu_id][nutrient_type_id] * num
            )
    print("-" * 20)
    for nutrient_type_id, nutrient_value in nutrient_values.items():
        name = nutrient_value["name"]
        value = nutrient_value["value"]
        unit = nutrient_types[nutrient_type_id]["unit"]
        print(f"{name}: {value:.1f}{unit}")
    print("-" * 20)
    print(f"最安値: {round(price)}円")


if __name__ == "__main__":
    db = "./data/mcdonalds.sqlite"
    con = sqlite3.connect(db)
    menus, nutrients, nutrient_types = get_data(con)
    # https://www.caa.go.jp/policies/policy/food_labeling/information/research/2019/pdf/food_labeling_cms206_200424_01.pdf
    nutrient_targets = [
        {"id": 1, "name": "エネルギー", "target": 2200},
        {"id": 3, "name": "たんぱく質", "target": 81},
        {"id": 4, "name": "脂質", "target": 62},
        {"id": 5, "name": "炭水化物", "target": 320},
        {"id": 8, "name": "カルシウム", "target": 680},
        {"id": 10, "name": "鉄", "target": 6.8},
        {"id": 11, "name": "ビタミンA", "target": 770},
        {"id": 12, "name": "ビタミンB1", "target": 1.2},
        {"id": 13, "name": "ビタミンB2", "target": 1.4},
        {"id": 15, "name": "ビタミンC", "target": 100},
        {"id": 17, "name": "食物繊維", "target": 19},
        {"id": 18, "name": "食塩相当量", "target": 7},
    ]
    result = solve(menus, nutrients, nutrient_targets)
    if result is None:
        print("no solution")
    else:
        print_result(menus, nutrients, nutrient_types, result)
