import React, { useState } from 'react';

const GptApiHandler = ({ onFetchGptText }) => {
  const [generatedText, setGeneratedText] = useState('');

  const handleGenerateText = async () => {
    try {
      // This is where you would make the API call to GPT
      // For the sake of this example, I'm just setting a static string
      // You would replace this with your actual API call logic
      const newText = 'This is the generated text from GPT based on the analysis.';
      setGeneratedText(newText);
      
      // If you have a callback to pass the text up to a parent component
      if(onFetchGptText) {
        onFetchGptText(newText);
      }
    } catch (error) {
      console.error('Error fetching text from GPT:', error);
      // Handle the error state here
    }
  };

  return (
    <div>
      <button onClick={handleGenerateText}>Generate Text</button>
      <div>
        <p>Generated Text:</p>
        <div>{generatedText}</div>
      </div>
    </div>
  );
};

export default GptApiHandler;
