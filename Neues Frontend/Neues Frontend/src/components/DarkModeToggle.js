import React from "react";
import './DarkModeToggle.css'

const DarkModeToggle = ({ isDarkMode, onToggle }) => {
  return (
    <div className="container">
      <input
        id="checkbox"
        type="checkbox"
        checked={isDarkMode}
        onChange={onToggle}
      />
      <label className="label" htmlFor="checkbox"></label>
    </div>
  );
};

export default DarkModeToggle;
