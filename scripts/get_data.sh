#!/usr/bin/env bash

menu_json_url="https://www.mcdonalds.co.jp/api/v1/product_menu.json"
menu_json_file="../data/product_menu.json"

nutrient_json_url="https://www.mcdonalds.co.jp/products/check_common_data/data/nutrient.json"
nutrient_json_file="../data/nutrient.json"

curl -so $menu_json_file $menu_json_url
curl -so $nutrient_json_file $nutrient_json_url