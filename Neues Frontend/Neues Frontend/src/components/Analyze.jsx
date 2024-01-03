import axios from "axios";
import React, { useEffect, useRef, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";

const Analyze = () => {
  const location = useLocation();
  const fileInputRef = useRef();
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileHistory, setFileHistory] = useState(() => {
    const history = localStorage.getItem("fileHistory");
    return history ? JSON.parse(history) : [];
  });
  const [showAllFiles, setShowAllFiles] = useState(false);
  const [filesToShow, setFilesToShow] = useState(3);

  useEffect(() => {
    // Log the selectedFile state each time it changes to track its updates
    console.log('Selected File State Updated:', selectedFile);
  }, [selectedFile]);

  const updateFileHistory = useCallback((newFileData) => {
    setFileHistory((prevHistory) => {
      const updatedHistory = [newFileData, ...prevHistory];
      localStorage.setItem("fileHistory", JSON.stringify(updatedHistory));
      return updatedHistory;
    });
  }, []);

  const processFile = useCallback(async (file) => {
    if (!(file instanceof File)) {
      console.error('The provided file is not an instance of File.');
      return;
    }
  
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Only PDF files are allowed!");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await axios.post('http://localhost:4000/api/v1/analyze', formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log('Response Data:', response.data);

      // Check for the correct data structure in the response
      if (!response.data || !response.data['Red Flags']) {
        console.error('Unexpected response structure:', response.data);
        return;
      }
    
      const newFileData = {
        name: file.name,
        red_flags: response.data['Red Flags'],
        orange_flags: response.data['Orange Flags'],
        green_flags: response.data['Green Flags'],
      };
  
      if (!fileHistory.some((f) => f.name === file.name)) {
        updateFileHistory(newFileData);
      }
  
      setSelectedFile(newFileData);
    } catch (error) {
      console.error("Error processing file:", error);
      alert(`Error: ${error.message}`);
    }
  }, [fileHistory, updateFileHistory]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    processFile(file);
  };

  useEffect(() => {
    const file = location.state?.selectedFile;
    if (file) {
      processFile(file);
    }
  }, [location.state?.selectedFile, processFile]);
    
  const handleUploadCardClick = () => {
    fileInputRef.current.click();
  };

  const handleHistoryClick = (fileName) => {
    const file = fileHistory.find((f) => f.name === fileName);
    setSelectedFile(file);
  };

  const handleShowAllClick = () => {
    setShowAllFiles((prevShowAll) => !prevShowAll);
    setFilesToShow(fileHistory.length);
  };
  
  const renderFlags = (flags, color) => {
    if (!flags || !Array.isArray(flags)) {
      return null;
    }
  
    return (
      <ul className={`flags-list ${color}-flags`}>
        {flags.map((flag, index) => (
          <li key={index}>
            {flag.name} - {flag.status}
          </li>
        ))}
      </ul>
    );
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
              ref={fileInputRef}
              onChange={handleFileChange}
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
              {/* Red Flags */}
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
                      {selectedFile && renderFlags(selectedFile.red_flags, 'red')}
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
                      {selectedFile && renderFlags(selectedFile.orange_flags, 'orange')}
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
                      {selectedFile && renderFlags(selectedFile.green_flags, 'green')}
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
