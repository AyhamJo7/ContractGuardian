import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <div className="w-full flex justify-center items-center py-4 text-[#6b21e5]">
      <Link to={"impressum"}>Impressum/Haftungsauschluss</Link>
    </div>
  );
};

export default Footer;
