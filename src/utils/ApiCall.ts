const MENU_URL = "https://www.mcdonalds.co.jp/api/v1/product_menu.json";
const NUTRIENT_URL =
  "https://www.mcdonalds.co.jp/products/check_common_data/data/nutrient.json";

const cacedApiCall = async (url: string, onError: () => void) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
    }
    const json = await response.json();
    return json;
  } catch (error) {
    onError();
  }
};

export const fetchMenu = async () => {
  const onErrorFetchMenu = () => {
    console.error("error fetchMenu");
    alert("メニューの取得に失敗しました");
  };
  return cacedApiCall(MENU_URL, onErrorFetchMenu);
};

export const fetchNutrient = async () => {
  const onErrorFetchNutrient = () => {
    console.error("error fetchNutrient");
    alert("栄養素の取得に失敗しました");
  };
  return cacedApiCall(NUTRIENT_URL, onErrorFetchNutrient);
};