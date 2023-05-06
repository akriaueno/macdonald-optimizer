import { useState } from "react";
import { useEffect } from "react";
import "./App.css";
import { RunButton } from "./components/RunButton";
import { fetchMenu, fetchNutrient } from "./utils/ApiCall";

function App() {
  const [menu, setMenu] = useState({});
  const [nutorient, setNutorient] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const [menuJson, nutrientJson] = await Promise.all([
        fetchMenu(),
        fetchNutrient(),
      ]);
      setMenu(menuJson);
      setNutorient(nutrientJson);
    };
    fetchData();
  }, []);

  const runIP = () => {
    console.log(menu, nutorient);
  };

  return (
    <>
      <h1>McDonald's optimizer</h1>
      <div className="card">
        <div>
          <label htmlFor="objective">目的:</label>
          <select name="objective" id="objective">
            <option value="price">料金</option>
            <option value="weight">総重量</option>
          </select>
          の
          <select name="min-max" id="min-max">
            <option value="minimize">最小化</option>
            <option value="maximize">最大化</option>
          </select>
        </div>
        <div>
          <label htmlFor="constraint">制約条件:</label>
        </div>
        <RunButton onClick={runIP}></RunButton>
      </div>
    </>
  );
}

export default App;
