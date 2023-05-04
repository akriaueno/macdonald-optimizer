import { useState } from "react";
import "./App.css";
import { FetchButton } from "./components/FetchButton";
import { fetchMenu, fetchNutrient } from "./utils/ApiCall";

function App() {
  const [menu, setMenu] = useState({});

  const fetchData = async () => {
    console.log("Fetching menu");
    const res = await Promise.all([fetchMenu(), fetchNutrient()]);
    console.log({ res });
  };

  return (
    <>
      <h1>McDland's&trade; optimizer</h1>
      <div className="card">
        <FetchButton onClick={fetchData}></FetchButton>
      </div>
    </>
  );
}

export default App;
