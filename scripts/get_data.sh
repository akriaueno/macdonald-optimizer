#!/usr/bin/env bash

set -eux

script_dir=$(cd $(dirname $0) &&  pwd)
project_dir=$(cd "$script_dir/.." &&  pwd)
data_dir=$(cd $project_dir/public/data && pwd)

cd $project_dir

menu_json_url="https://www.mcdonalds.co.jp/api/v1/product_menu.json"
menu_json_file="$data_dir/product_menu.json"

nutrient_json_url="https://www.mcdonalds.co.jp/products/check_common_data/data/nutrient.json"
nutrient_json_file="$data_dir/nutrient.json"

curl -so $menu_json_file $menu_json_url
curl -so $nutrient_json_file $nutrient_json_url
