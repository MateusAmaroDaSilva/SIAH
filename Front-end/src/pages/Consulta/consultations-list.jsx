import { useState } from "react"
import { Calendar, MapPin, User, ChevronDown, ChevronUp, FileText, Pill } from "lucide-react"
import { formatDateTime } from "./consultations-list.js"
import "./consultations-list.css"

export default function ConsultationsList({ consultations = [] }) {
  const [expandedId, setExpandedId] = useState(null)

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id)
  }

  if (!Array.isArray(consultations) || consultations.length === 0) {
    return <p className="no-consultations">Nenhuma consulta encontrada.</p>
  }

  return (
    <div className="consultations-list">
      {consultations.map((consultation) => (
        <div key={consultation.id_consulta} className="consultation-card">
          <div className="consultation-card__header">
            <div className="consultation-card__header-content">
              <h3 className="consultation-card__title">{consultation.motivo_consulta}</h3>
              <div className="consultation-card__meta">
                <div className="consultation-card__meta-item">
                  <Calendar className="consultation-card__meta-icon" />
                  <span>{formatDateTime(consultation.data_consulta)}</span>
                </div>
                <div className="consultation-card__meta-item">
                  <User className="consultation-card__meta-icon" />
                  <span>{consultation.profissional?.nome}</span>
                </div>
              </div>
            </div>
            <button
              className="consultation-card__toggle"
              onClick={() => toggleExpand(consultation.id_consulta)}
            >
              {expandedId === consultation.id_consulta ? (
                <ChevronUp className="consultation-card__toggle-icon" />
              ) : (
                <ChevronDown className="consultation-card__toggle-icon" />
              )}
            </button>
          </div>

          {expandedId === consultation.id_consulta && (
            <div className="consultation-card__content">
              <div className="consultation-card__grid">
                <div>
                  <div className="consultation-card__section-header">
                    <MapPin className="consultation-card__section-icon" />
                    <h4 className="consultation-card__section-title">Hospital</h4>
                  </div>
                  <p className="consultation-card__section-text">
                    {consultation.hospital?.nome_hospital}
                  </p>
                  <p className="consultation-card__section-text consultation-card__section-text--small">
                    {consultation.hospital?.endereco}, {consultation.hospital?.cidade} -{" "}
                    {consultation.hospital?.estado}
                  </p>
                </div>

                <div>
                  <div className="consultation-card__section-header">
                    <User className="consultation-card__section-icon" />
                    <h4 className="consultation-card__section-title">Profissional</h4>
                  </div>
                  <p className="consultation-card__section-text">
                    {consultation.profissional?.nome}
                  </p>
                  <p className="consultation-card__section-text consultation-card__section-text--small">
                    {consultation.profissional?.especialidade} -{" "}
                    {consultation.profissional?.crm_coren}
                  </p>
                </div>
              </div>

              <div className="consultation-card__section">
                <div className="consultation-card__section-header">
                  <FileText className="consultation-card__section-icon" />
                  <h4 className="consultation-card__section-title">Diagnóstico</h4>
                </div>
                <p className="consultation-card__section-text">{consultation.diagnostico}</p>
              </div>

              <div className="consultation-card__section">
                <div className="consultation-card__section-header">
                  <Pill className="consultation-card__section-icon" />
                  <h4 className="consultation-card__section-title">Prescrição</h4>
                </div>
                <div className="consultation-card__prescription">
                  <p className="consultation-card__prescription-text">{consultation.prescricao}</p>
                </div>
              </div>

              {consultation.anotacoes_medicas && (
                <div className="consultation-card__section">
                  <h4 className="consultation-card__section-title">Anotações Médicas</h4>
                  <p className="consultation-card__section-text">
                    {consultation.anotacoes_medicas}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
