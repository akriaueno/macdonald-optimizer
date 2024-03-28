from datetime import datetime
import time
import streamlit as st
import sqlite3
import pandas as pd
from util.solver import get_data, solve
import logging
from io import StringIO


# Streamlitのログエリア用のセッション状態を初期化
if "log" not in st.session_state:
    st.session_state.log = StringIO()


# Streamlitのテキストエリアにログを表示するカスタムロガーハンドラー
# DB接続
con = sqlite3.connect("./data/mcdonalds.sqlite")
menus, nutrients, nutrient_types = get_data(con)

st.title("マクドナルド・オプティマイザー")
st.text("栄養素の目標値を満たしつつ、最小の金額のメニューを提案します。")

st.sidebar.header("栄養素の制約を設定")

exclude_zero_price = st.sidebar.checkbox("0円メニューを禁止", value=True)
max_items_per_menu = st.sidebar.number_input(
    "同じメニューの最大選択個数", min_value=1, value=3, step=1
)

num_of_meals = st.sidebar.number_input("何食分", min_value=1, value=1, step=1)

# 栄養素の目標値
nutrient_targets = [
    {"id": 1, "name": "エネルギー", "target": 2200 / 3 * num_of_meals},
    {"id": 3, "name": "たんぱく質", "target": 81 / 3 * num_of_meals},
    {"id": 4, "name": "脂質", "target": 62 / 3 * num_of_meals},
    {"id": 5, "name": "炭水化物", "target": 320 / 3 * num_of_meals},
    {"id": 8, "name": "カルシウム", "target": 680 / 3 * num_of_meals},
    {"id": 10, "name": "鉄分", "target": 6.8 / 3 * num_of_meals},
    {"id": 11, "name": "ビタミンA", "target": 770 / 3 * num_of_meals},
    {"id": 12, "name": "ビタミンB1", "target": 1.2 / 3 * num_of_meals},
    {"id": 13, "name": "ビタミンB2", "target": 1.4 / 3 * num_of_meals},
    {"id": 15, "name": "ビタミンC", "target": 100 / 3 * num_of_meals},
    {"id": 17, "name": "食物繊維", "target": 19 / 3 * num_of_meals},
    {"id": 18, "name": "食塩相当量", "target": 7 / 3 * num_of_meals},
]

nutrient_limits = {}
for nt in nutrient_targets:
    nutrient_id = nt["id"]
    name = nt["name"]
    target = nt["target"]
    # 目標値の±20%を初期値として設定
    lb = target * 0.8
    ub = target * 1.2

    step = 0.0
    if target < 10:
        step = 0.1
    elif target < 100:
        step = 1.0
    else:
        step = 10.0
    # ユーザーが各栄養素の下限値と上限値を設定できるようにスライダーを設置
    lb, ub = st.sidebar.slider(
        f"{name}の制約",
        0.0,
        float(target * 2),
        (float(lb), float(ub)),
        step,
        format="%.1f",
    )
    nutrient_limits[nutrient_id] = {"lb": lb, "ub": ub}


if st.button("最適化"):
    with st.spinner("計算中"):
        # mip.loggerにカスタムハンドラーを設定
        result = solve(
            menus,
            nutrients,
            nutrient_limits,
            nutrient_types,
            exclude_zero_price=exclude_zero_price,
            max_items_per_menu=max_items_per_menu,
        )

    if result is not None:
        # 結果のためのリストを作成
        rows = []
        total_price = 0
        for menu_id, num in result.items():
            menu_name = menus[menu_id]["name"]
            menu_price = menus[menu_id]["price"]
            item_total_price = menu_price * num
            total_price += item_total_price
            rows.append(
                [
                    menu_name,
                    round(num),
                    f"{menu_price}円",
                    f"{round(item_total_price)}円",
                ]
            )
        rows.append(["合計", "", "", f"{round(total_price)}円"])

        # リストからDataFrameを作成
        df = pd.DataFrame(rows, columns=["メニュー", "個数", "単価", "合計"])
        st.table(df)

        total_nutrients = {nt_id: 0 for nt_id in nutrient_types}
        for menu_id, num in result.items():
            menu_name = menus[menu_id]["name"]
            for nt_id in nutrients[menu_id]:
                total_nutrients[nt_id] += nutrients[menu_id][nt_id] * num

        nutrient_rows = []
        for nt_id, total in total_nutrients.items():
            nutrient_name = nutrient_types[nt_id]["name"]
            unit = nutrient_types[nt_id]["unit"]
            nutrient_rows.append([nutrient_name, f"{total:.2f} {unit}"])

        nutrient_df = pd.DataFrame(nutrient_rows, columns=["栄養素", "総量"])
        st.table(nutrient_df)
    else:
        st.write("解が見つかりませんでした。")
