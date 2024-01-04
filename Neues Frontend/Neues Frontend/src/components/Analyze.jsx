import axios from "axios";
import React, { useEffect, useRef, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";

const Analyze = () => {
  const location = useLocation();
  const fileInputRef = useRef();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false); // NEW


  useEffect(() => {
    // Log the selectedFile state each time it changes to track its updates
    console.log('Selected File State Updated:', selectedFile);
  }, [selectedFile]);

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
  
    setIsProcessing(true); // NEW 


    try {
      const response = await axios.post('http://localhost:4000/api/v1/analyze', formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log('Response Data:', response.data);

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
  
      setSelectedFile(newFileData);

      // On successful response  
      setSelectedFile(newFileData);
      setIsProcessing(false); // Hide loader when processing is done


    } catch (error) {
      console.error("Error processing file:", error);
      alert(`Error: ${error.message}`);

      setIsProcessing(false); // Hide loader in case of error

    }
  }, []);

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
          {/* Overlay Loader */}
    {isProcessing && (
      <div className="absolute inset-0 flex justify-center items-center bg-white bg-opacity-50 z-50">
        <div className="loader"></div>
      </div>
    )}
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
        </div>
        <div className="right">
          <div className="relative mx-auto max-w-[450px] ">
            <ul className="">
              {/* Red Flags */}
              <li className="text-left bg-red-400">
                <label
                  htmlFor="accordion-2"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-2"
                    defaultChecked // This sets the checkbox to checked by default

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
                      Red Flags (Pflicht Klauseln)
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 font-bold pb-2">
                      <ul className="text-sm">
                      {selectedFile && renderFlags(selectedFile.red_flags, 'red')}
                      </ul>
                    </div>
                  </div>
                </label>
              </li>
              <li className="text-left bg-orange-400">
                <label
                  htmlFor="accordion-3"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-3"
                    defaultChecked // This sets the checkbox to checked by default
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
                    <h3 className="text-sm text-orange-700 lg:text-base">
                      Orange Flags (Empfohlene Klauseln)
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 font-bold pb-2">
                      <ul className="text-sm">
                      {selectedFile && renderFlags(selectedFile.orange_flags, 'orange')}
                      </ul>
                    </div>
                  </div>
                </label>
              </li>
              <li className="text-left bg-green-400">
                <label
                  htmlFor="accordion-4"
                  className="relative flex flex-col border-b-[1px] border-gray-300"
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-4"
                    defaultChecked // This sets the checkbox to checked by default
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
                      Green Flags (Optinale Klauseln)
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 font-bold pb-2">
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
