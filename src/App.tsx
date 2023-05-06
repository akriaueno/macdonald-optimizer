import { useState } from "react";
import { useEffect } from "react";
import "./App.css";
import { RunButton } from "./components/RunButton";
import { fetchMenu, fetchNutrient } from "./utils/ApiCall";
import GLPKJS from "glpk.js";
import type { GLPK } from "glpk.js";

interface Nutrient {
  id: string;
  name: string;
  unit: string;
  amount: number | null;
}

interface Menu {
  id: string;
  name: string;
  price: number;
  nutorients: Array<Nutrient>;
}

interface LPVariable {
  name: string;
  coef: number;
}

interface RawMenu {
  product_menu: Array<{
    id: string;
    web_name: string;
    price: string;
  }>;
}

interface RawNutrient {
  data: Array<{
    nutrient_id: string;
    name: string;
    unit: string;
  }>;
}

function App() {
  const [rawMenu, setMenu] = useState({} as RawMenu);
  const [rawNutorient, setNutorient] = useState({} as RawNutrient);

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

  const _getMenu = (): Array<Menu> => {
    const menus: Array<Menu> = [];
    const nutorientsTemplate: Array<Nutrient> = [];
    for (const rawN of rawNutorient.data) {
      const n: Nutrient = {
        id: rawN.nutrient_id,
        name: rawN.name,
        unit: rawN.unit,
        amount: null,
      };
      nutorientsTemplate.push(n);
    }
    for (const m of rawMenu.product_menu) {
      menus.push({
        id: m.id,
        name: m.web_name,
        price: Number(m.price),
        nutorients: nutorientsTemplate,
      });
    }
    console.log(menus);
    return menus;
  };

  const _genObjectiveVars = (menus: Array<Menu>): Array<LPVariable> => {
    const variable: Array<LPVariable> = [];
    for (const menu of menus) {
      variable.push({
        name: menu.id,
        coef: menu.price,
      });
    }
    return variable;
  };

  const runIP = async () => {
    console.log(rawMenu, rawNutorient);
    const menu: Array<Menu> = _getMenu();
    const objectiveVars = _genObjectiveVars(menu);
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore glpk.jsのpackage.jsonのmainが無視されてdist/glpk.jsではなくdist/glpk.d.tsが読み込まれてエラーになる
    const glpk: GLPK = await GLPKJS();

    const options = {
      msglev: glpk.GLP_MSG_ALL,
      presol: true,
      cb: {
        call: (progress: any) => console.log(progress),
        each: 1,
      },
    };
    const up_to_one_constraints = objectiveVars.map((v) => {
      return {
        name: `upto_one_constraint_${v.name}`,
        vars: [{ name: v.name, coef: 1.0 }],
        bnds: { type: glpk.GLP_DB, ub: 1.0, lb: 0.0 },
      };
    });

    const problem = {
      name: "IP",
      generals: objectiveVars.map((v) => v.name),
      objective: {
        direction: glpk.GLP_MIN,
        name: "obj",
        vars: objectiveVars,
      },
      subjectTo: [
        ...up_to_one_constraints,
        {
          name: "five_items_constraint",
          vars: objectiveVars.map((v) => {
            return { name: v.name, coef: 1.0 };
          }),
          bnds: { type: glpk.GLP_DB, ub: 5.0, lb: 4.9 },
        },
      ],
    };
    console.log({ problem });
    const p = await glpk.write(problem);
    console.log(p);
    const res = await glpk.solve(problem, options);
    console.log(res.result);
    Object.keys(res.result.vars).forEach((id) => {
      const num = res.result.vars[id];
      if (num > 0) {
        console.log(id, num);
      }
    });
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
