import React from "react";

const Impressum = () => {
  return (
    <div className="mainContainer flex flex-col  items-center mt-5 min-h-screen">
      <div className="impContents  max-w-[1000px]  px-5">
        <h1 className="text-[#6b21e5] text-center text-[24px] font-bold">
          Impressum & Haftungsauschluss
        </h1>
        <p className="text-center mt-2 font-semibold">
        Haftungsausschluss: Dieses Werkzeug dient ausschließlich zu Informationszwecken. Es bietet eine Analyse von GmbH-Verträgen auf mögliche fehlende Klauseln. Es stellt keine Rechtsberatung dar. Wir übernehmen keine Garantie für die Genauigkeit oder Vollständigkeit. Benutzer sollten sich für Beratung an Rechtsprofis wenden. Die Nutzung dieses Werkzeugs erfolgt auf eigenes Risiko, und wir haften nicht für etwaige Folgen. Mit der Nutzung dieses Werkzeugs stimmen Sie diesen Bedingungen zu.
        </p>
      </div>
    </div>
  );
};

export default Impressum;
