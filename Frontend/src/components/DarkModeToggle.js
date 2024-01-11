import React from "react";
import './DarkModeToggle.css'

const DarkModeToggle = ({ isDarkMode, onToggle }) => {
  return (
    <div className="div relative flex justify-left overflow-hidden px-4 py-2 lg:flex-row lg:items-center">
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
