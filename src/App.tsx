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

  return (
    <>
      <h1>McDonald's optimizer</h1>
      <div className="card">
        <RunButton onClick={() => {}}></RunButton>
      </div>
    </>
  );
}

export default App;
