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

  const getRedFlagMessage = () => {
    if (!selectedFile || !selectedFile.red_flags) return '';
    const missingRedFlags = selectedFile.red_flags.filter(flag => flag.status === '✗').map(flag => flag.name);
    return missingRedFlags.length > 0 
      ? `Bitte fügen Sie die folgenden wichtigen Klauseln in Ihr Vertrag ein: ${missingRedFlags.join(', ')}. Diese Klausel/n ist essentiell, da sie für die Gültigkeit des Vertrags unerlässlich ist. Ohne diese Angabe kann der Vertrag rechtlich anfechtbar sein. Ich empfehle dringend, diese Ergänzung vorzunehmen, um jegliche Unklarheiten oder rechtliche Probleme in der Zukunft zu vermeiden.\n`
      : 'Alle essentielle Klauseln sind im Vertrag enthalten.';
  };
  
  const getOrangeFlagMessage = () => {
    if (!selectedFile || !selectedFile.orange_flags) return '';
    const missingOrangeFlags = selectedFile.orange_flags.filter(flag => flag.status === '✗').map(flag => flag.name);
    return missingOrangeFlags.length > 0 
      ? `\nEs wird empfohlen, diese Klauseln zu Ihrem Vertrag hinzufügen zu lassen: ${missingOrangeFlags.join(', ')}. Obwohl diese Klauseln nicht gesetzlich vorgeschrieben sind, sind sie doch äußerst empfehlenswert.`
      : '\nAlle empfohlenen Klauseln sind im Vertrag enthalten.\n';
  };
  
  const getGreenFlagMessage = () => {
    if (!selectedFile || !selectedFile.green_flags) return '';
    const missingGreenFlags = selectedFile.green_flags.filter(flag => flag.status === '✗').map(flag => flag.name);
    return missingGreenFlags.length > 0 
      ? `\nOptionale Klauseln, die Sie in Betracht ziehen können: ${missingGreenFlags.join(', ')}. Diese Klauseln sind zwar nicht zwingend erforderlich, können aber zur Klarheit und Vollständigkeit des Vertrages beitragen.`
      : '\nAlle optionalen Klauseln sind im Vertrag enthalten.';
  };
  

  const processFile = useCallback(async (file) => {
    if (!(file instanceof File)) {
      console.error('The provided file is not an instance of File.');
      return;
    }
  
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Entschuldigen Sie das Missverständnis! Es sind nur PDF-Dateien erlaubt!");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fileName", file.name);
  
    setIsProcessing(true); // NEW 

    try {
      const response = await axios.post('/api/v1/analyze', formData, {
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
            <span className="font-bold text-[#6b21e5]">Aktuelle Datei:</span>{" "}
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
            <p>Neue .pdf Datei hochladen</p>
          </div>
          
          <div>
          <div className="text-left pt-2 pb-2 pl-2 mt-8 relative mx-auto max-w-[450px] font-bold text-left bg-purple-400">
                <label
                  htmlFor="accordion-5"
                  className="relative flex flex-col "
                >
                  <input
                    className="peer hidden"
                    type="checkbox"
                    id="accordion-5"
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
                    <h3 className="text-sm  lg:text-base text-purple-700">
                      Analyse
                    </h3>
                  </div>
                  <div className="max-h-0 overflow-hidden transition-all duration-500 peer-checked:max-h-96">
                    <div className="px-5 font-bold pb-2">
                      <ul className="text-sm">
                      <p>{getRedFlagMessage()}</p>
                      <p>{getOrangeFlagMessage()}</p>
                      <p>{getGreenFlagMessage()}</p>
                      </ul>
                    </div>
                  </div>
                </label>
              </div>
          </div>
        </div>
        <div className="right">
          <div className="relative mx-auto max-w-[450px] ">
            <ul className="">
              {/* Red Flags */}
              <li className="text-left font-bold bg-red-400">
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
              <li className="text-left font-bold bg-orange-400">
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
              <li className="text-left font-bold bg-green-400">
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
