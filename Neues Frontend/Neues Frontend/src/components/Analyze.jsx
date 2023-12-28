import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";

const Analyze = () => {
  const location = useLocation();
  const fileInputRef = useRef();

  let fileHistory = localStorage.getItem("fileHistory")
    ? JSON.parse(localStorage.getItem("fileHistory"))
    : [
        {
          name: "",
          red_flags: [],
          orange_flags: [],
          green_flags: [],
        },
      ];

  const fileFromHome = location.state?.selectedFile;

  const [selectedFile, setSelectedFile] = useState({
    name: fileHistory[0].name,
    red_flags: fileHistory[0].red_flags,
    orange_flags: fileHistory[0].orange_flags,
    green_flags: fileHistory[0].green_flags,
  });

  const [showAllFiles, setShowAllFiles] = useState(false);
  const [filesToShow, setFilesToShow] = useState(3); // Number of files to display initially

  const handleShowAllClick = () => {
    setShowAllFiles(true);
    setFilesToShow(fileHistory.length); // Show all files
  };

  const handleUploadCardClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (file) => {
    const allowedExtensions = [".pdf"];

    if (file) {
      const fileNameParts = file.name.split(".");
      const fileExtension = `.${
        fileNameParts[fileNameParts.length - 1]
      }`.toLowerCase();

      if (allowedExtensions.includes(fileExtension)) {
        const formData = new FormData();
        formData.append("pdfFile", file); // Sending the file as 'pdfFile'

        await axios
          .post(`http://localhost:4000/api/v1/post`, formData, {
            headers: {
              "Content-Type": "multipart/form-data", // Setting proper headers for form data
            },
          })
          .then((res) => {
            console.log("pdf data: ", res.data);
            const result = res.data.result;

            // Update selectedFile state while keeping the file name intact
            setSelectedFile({
              name: file.name,
              red_flags: result.red_flags,
              orange_flags: result.orange_flags,
              green_flags: result.green_flags,
            });

            const existingFileIndex = fileHistory.findIndex(
              (item) => item.name === file.name
            );

            if (existingFileIndex !== -1) {
              // Update existing file's content in fileHistory
              fileHistory[existingFileIndex] = {
                name: file.name,
                red_flags: result.red_flags,
                orange_flags: result.orange_flags,
                green_flags: result.green_flags,
              };
            } else {
              // Add a new item to fileHistory
              fileHistory.unshift({
                name: file.name,
                red_flags: result.red_flags,
                orange_flags: result.orange_flags,
                green_flags: result.green_flags,
              });
            }

            localStorage.setItem("fileHistory", JSON.stringify(fileHistory));
          })
          .catch((error) => {
            console.error("Error uploading file: ", error);
          });
      } else {
        alert("Only pdf files are allowed!");
      }
    }
  };

  const handleUploadFile = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    handleFileChange(file);
  };

  useEffect(() => {
    handleFileChange(fileFromHome);
  }, [fileFromHome]);

  const handleHistoryClick = (fileName) => {
    const file = fileHistory.find((f) => f.name === fileName);
    setSelectedFile(file);
  };

  return (
    <div className="w-full flex justify-center min-h-screen">
      <div className="mt-5 flex flex-col md:flex-row md:justify-between w-[1000px] px-5">
        <div className="leftSect mb-8">
          <p className="text-[#6b21e5] font-semibold">
            <span className="font-bold text-[#6b21e5]">Current File:</span>{" "}
            {selectedFile && selectedFile.name}
          </p>
          <div
            onClick={handleUploadCardClick}
            className="mt-5 gb-white px-4 flex justify-center py-2 rounded-full shadow-blue text-[#6b21e5] font-bold hover:cursor-pointer"
          >
            <input
              type="file"
              className=""
              ref={fileInputRef}
              onChange={handleUploadFile}
              style={{ display: "none" }}
            />
            <p>Upload New File</p>
          </div>
          <div>
            <h2 className="mt-5 font-bold text-[#6b21e5] mb-2">
              File history{" "}
            </h2>
            {fileHistory.length === 0 ? (
              <p className="font-semibold text-[#6b21e5]">Empty</p>
            ) : (
              <>
                {fileHistory.slice(0, filesToShow).map((file, index) => (
                  <p
                    key={index}
                    onClick={(e) => handleHistoryClick(file.name)}
                    className="font-semibold text-[#6b21e5] cursor-pointer mb-2"
                  >
                    {file.name ? file.name : ""}
                  </p>
                ))}
                {!showAllFiles && fileHistory.length > 4 && (
                  <button
                    onClick={handleShowAllClick}
                    className="text-[#6b21e5]"
                  >
                    Show All
                  </button>
                )}
              </>
            )}
          </div>
        </div>
        <div className="right">
          <div className="relative mx-auto max-w-[450px] ">
            <ul className="">
              <li className="text-left bg-red-300">
                <label
                  htmlFor="accordion-2"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-2"
                  />
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="absolute right-0 top-4 ml-auto mr-5 h-4 text-gray-500 transition peer-checked:rotate-180"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                  <div className="relative ml-4 cursor-pointer select-none py-2 items-center pr-12">
                    <h3 className="text-sm  lg:text-base text-red-700">
                      Red Flags
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 pb-2">
                      <ul className="text-sm">
                        {selectedFile.red_flags.length !== 0
                          ? selectedFile.red_flags.map((red) => <li>{red}</li>)
                          : "Empty"}
                      </ul>
                    </div>
                  </div>
                </label>
              </li>
              <li className="text-left bg-orange-300">
                <label
                  htmlFor="accordion-3"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-3"
                  />
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="absolute right-0 top-4 ml-auto mr-5 h-4 text-gray-500 transition peer-checked:rotate-180"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                  <div className="relative ml-4 cursor-pointer select-none items-center py-2 pr-12">
                    <h3 className="text-sm text-orange-600 lg:text-base">
                      Orange Flags
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 pb-2">
                      <ul className="text-sm">
                        {selectedFile.orange_flags.length !== 0
                          ? selectedFile.orange_flags.map((orange) => (
                              <li>{orange}</li>
                            ))
                          : "Empty"}
                      </ul>
                    </div>
                  </div>
                </label>
              </li>
              <li className="text-left bg-green-300">
                <label
                  htmlFor="accordion-4"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-4"
                  />
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="absolute right-0 top-4 ml-auto mr-5 h-4 text-gray-500 transition peer-checked:rotate-180"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                  <div className="relative ml-4 cursor-pointer select-none items-center py-2 pr-12">
                    <h3 className="text-sm text-green-700 lg:text-base">
                      Green Flags
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 pb-2">
                      <ul className="text-sm">
                        {selectedFile.green_flags.length !== 0
                          ? selectedFile.green_flags.map((green) => (
                              <li>{green}</li>
                            ))
                          : "Empty"}
                      </ul>
                    </div>
                  </div>
                </label>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analyze;
