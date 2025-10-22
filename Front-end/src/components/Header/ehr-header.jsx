"use client"

import { Download } from "lucide-react"
import "./ehr-header.css"

export default function EHRHeader({ patient }) {
  const handleExport = () => {
    alert("Funcionalidade de exportação em desenvolvimento")
  }

  return (
    <header className="ehr-header">
      <div className="ehr-header__content">
        

        <button className="ehr-header__button" onClick={handleExport}>
          <Download className="ehr-header__button-icon" />
          Exportar Prontuário
        </button>
      </div>
    </header>
  )
}
