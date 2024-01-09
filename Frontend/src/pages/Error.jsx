import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Error = () => {
  return (
    <div>
      <Navbar />
      <div className="min-h-screen flex justify-center items-center">
        <p className="text-2xl font-bold">404 Not Found</p>
      </div>
      <Footer />
    </div>
  );
};

export default Error;
