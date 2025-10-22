import { Activity, Thermometer, Heart, Weight, Ruler, FileText, Clock } from "lucide-react"
import { calculateBMI, getBMICategory, formatDateTime } from "./triage-card.js"
import "./triage-card.css"

export default function TriageCard({ triages }) {
  return (
    <div className="triage-list">
      {triages.map((triage) => {
        const bmi = calculateBMI(triage.peso, triage.altura)
        const bmiCategory = getBMICategory(bmi)

        return (
          <div key={triage.id_triagem} className="triage-card">
            <div className="triage-card__header">
              <h3 className="triage-card__title">Triagem #{triage.id_triagem}</h3>
              <div className="triage-card__date">
                <Clock className="triage-card__date-icon" />
                <span>{formatDateTime(triage.data_hora_triagem)}</span>
              </div>
            </div>

            <div className="triage-card__content">
              <div className="triage-card__grid">
                <div className="triage-card__item">
                  <Activity className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Pressão Arterial</p>
                    <p className="triage-card__value">{triage.pressao_arterial}</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <Thermometer className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Temperatura</p>
                    <p className="triage-card__value">{triage.temperatura}</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <Heart className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Frequência Cardíaca</p>
                    <p className="triage-card__value">{triage.frequencia_cardiaca} bpm</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <Weight className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Peso</p>
                    <p className="triage-card__value">{triage.peso} kg</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <Ruler className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Altura</p>
                    <p className="triage-card__value">{triage.altura} m</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <Activity className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">IMC</p>
                    <div className="triage-card__bmi">
                      <p className="triage-card__value">{bmi}</p>
                      <span className="triage-card__badge">{bmiCategory}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="triage-card__section">
                <div className="triage-card__item">
                  <FileText className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Sintomas Principais</p>
                    <p className="triage-card__section-text">{triage.sintomas_principais}</p>
                  </div>
                </div>

                <div className="triage-card__item">
                  <FileText className="triage-card__icon" />
                  <div className="triage-card__item-content">
                    <p className="triage-card__label">Observações de Enfermagem</p>
                    <p className="triage-card__section-text">{triage.observacoes_enfermagem}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
