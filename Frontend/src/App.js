import React, { useState, useEffect } from "react";
import "./App.css";
import Home from "./pages/Home";
import Error from "./pages/Error";
import Root from "./pages/Root";
import Analyze from "./components/Analyze";
import Impressum from "./components/Impressum";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import DarkModeToggle from "./components/DarkModeToggle";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const isDarkModeEnabled = localStorage.getItem("darkMode") === "true";
    setDarkMode(isDarkModeEnabled);
  }, []);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem("darkMode", newMode.toString());
  };

  const router = createBrowserRouter([
    {
      path: "",
      element: <Root />,
      errorElement: <Error />,
      children: [
        {
          index: true,
          element: <Home />,
        },
        {
          path: "analyze",
          element: <Analyze />,
        },
        {
          path: "impressum",
          element: <Impressum />,
        },
      ],
    },
  ]);

  return (
    <div className={darkMode ? "dark-mode" : "light-mode"}>
      <DarkModeToggle isDarkMode={darkMode} onToggle={toggleDarkMode} />
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
