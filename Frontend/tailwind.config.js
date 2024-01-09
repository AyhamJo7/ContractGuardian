/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      // Add your custom colors
      colors: {
        'custom-purple': '#6b21e5', // Example custom color
        // Add more custom colors here
      },
      // Add custom max-height values
      maxHeight: {
        '96': '24rem', // 24rem is just an example value
        // Add more custom max-heights here
      },
      // Add custom spacing, fontSize, borderColor, etc.
      spacing: {
        '128': '32rem', // Example custom spacing
        // Add more custom spacings here
      },
      fontSize: {
        'custom-size': '2.25rem', // Example custom font size
        // Add more custom font sizes here
      },
      // Any other theme extensions...
    },
  },
  plugins: [
    // Add Tailwind plugins here if needed
  ],
};
