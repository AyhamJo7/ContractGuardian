import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Logo from './photos/WhatsApp_Bild_2023-12-14_um_00.34.16_046f8d51-removebg-preview.png'

import UploadFiles from "./components/upload-files.component";

function App() {
  return (
    <div className="container">
      <div>
        <header className="header">
          <img src={Logo} alt="Logo" className="Logo"/>
        </header>
      </div>
      <div className="bg-picture">
        <UploadFiles />
      </div>
    </div>
  );
}

export default App;
