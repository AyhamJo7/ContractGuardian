import React, { useRef, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { BsCloudUpload } from "react-icons/bs";
import { IoIosSearch } from "react-icons/io";
import { FaCircleCheck } from "react-icons/fa6";
import { useNavigate } from "react-router-dom";
import { useAnimate, motion, delay } from "framer-motion";

const Home = () => {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleUploadCardClick = () => {
    fileInputRef.current.click();
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleUploadedFile(file);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    handleUploadedFile(file);
  };

  const handleUploadedFile = (file) => {
    const allowedExtensions = [".pdf"];

    if (file) {
      const fileName = file.name;
      const fileNameParts = fileName.split(".");
      const fileExtension = `.${
        fileNameParts[fileNameParts.length - 1]
      }`.toLowerCase();

      if (allowedExtensions.includes(fileExtension)) {
        navigate("analyze", { state: { selectedFile: file } });
      } else {
        alert("Only pdf files are allowed!");
      }
    }
  };

  return (
    <div className="mt-6 px-5">
      <div className="flex justify-center items-center md:gap-[50px]">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="w-full pt-14 pb-5 bg-white shadow-2xl shadow-blue flex flex-col flex-1 justify-center items-center rounded-2xl  md:max-w-[320px] max-h-[160px] hover:cursor-pointer "
          onClick={handleUploadCardClick}
        >
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleFileDrop}
            className="flex justify-center items-center flex-col"
          >
            <FaPlus style={{ color: "#6112e3", fontSize: "1.5rem" }} />
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <p className="text-center font-bold mt-3 text-[#6b21e5]">
            Klicken Sie hier, um Ihr  <br /> .pdf hochzuladen
            </p>
          </div>
        </motion.div>
        <div className="img max-w-[370px]">
          <motion.img
            initial={{ opacity: 0, scale: 0.3 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 }}
            className="responsive-image w-[100%]"
            src="images/vector.jpg"
            alt=""
          />
        </div>
      </div>
      <motion.h1
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="text-xl font-bold text-center mt-14 text-[#6b21e5]"
      >
        Wie funktioniert es
      </motion.h1>
      <motion.div
        variants={{
          visible: { transition: { staggerChildren: 0.05 } },
        }}
        className="cards mb-5 flex flex-wrap justify-center gap-10 mt-8"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="card flex flex-col pt-5 pb-5 items-center w-full md:max-w-[250px] max-h-[300px] bg-white shadow-black rounded-2xl"
        >
          <BsCloudUpload style={{ fontSize: "2.5rem", textAlign: "center" }} />
          <h2 className="text-center mt-2 text-md font-extrabold">
          Laden Sie Ihren GmbH-Vertrag hoch
          </h2>
          <p className="text-center font-bold text-sm mt-3  px-[16px]">
          Übertragen Sie Ihren .pdf-Vertrag ganz einfach mit der intuitiven Upload-Funktion
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
          className="card flex flex-col pt-5 pb-5 items-center w-full md:max-w-[250px] max-h-[300px] bg-white shadow-black rounded-2xl"
        >
          <IoIosSearch style={{ fontSize: "2.5rem", textAlign: "center" }} />
          <h2 className="text-center mt-2 text-md font-extrabold">
          Lassen Sie Ihren Vertrag von unserem System analysieren
          </h2>
          <p className="text-center font-bold text-sm mt-3  px-[16px]">
          Unser System analysiert Ihren Vertrag auf fehlende zwingende oder empfohlene Klauseln
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7 }}
          className="card flex flex-col pt-5 pb-5 items-center w-full md:max-w-[250px] max-h-[300px] bg-white shadow-black rounded-2xl"
        >
          <FaCircleCheck style={{ fontSize: "2.5rem", textAlign: "center" }} />
          <h2 className="text-center mt-2 text-md font-extrabold">
          Ergebnisse in weniger als einer Minute
          </h2>
          <p className="text-center font-bold text-sm mt-3  px-[16px]">
          Erhalten Sie intuitives Echtzeit-Feedback zu den Klauseln Ihres Vertrags
          </p>
        </motion.div>
      </motion.div>
      <div className="disclaimer my-10 flex justify-center">
        <p className="max-w-[1000px] font-bold text-sm text-center">
        Haftungsausschluss: Dieses Werkzeug dient ausschließlich zu Informationszwecken. Es bietet eine Analyse von GmbH-Verträgen auf mögliche fehlende Klauseln. Es stellt keine Rechtsberatung dar. Wir übernehmen keine Garantie für die Genauigkeit oder Vollständigkeit. Benutzer sollten sich für Beratung an Rechtsprofis wenden. Die Nutzung dieses Werkzeugs erfolgt auf eigenes Risiko, und wir haften nicht für etwaige Folgen. Mit der Nutzung dieses Werkzeugs stimmen Sie diesen Bedingungen zu.
        </p>
      </div>
    </div>
  );
};

export default Home;
