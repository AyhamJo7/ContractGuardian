import "./App.css";
import Home from "./pages/Home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Error from "./pages/Error";
import Root from "./pages/Root";
import Analyze from "./components/Analyze";
import Impressum from "./components/Impressum";

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

function App() {
  return <RouterProvider router={router}></RouterProvider>;
}

export default App;
