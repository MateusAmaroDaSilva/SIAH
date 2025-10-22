import { FileText, Calendar, Building2, ExternalLink } from "lucide-react"
import { formatDate } from "./exams-list.js"
import "./exams-list.css"

export default function ExamsList({ exams }) {
  return (
    <div className="exams-list">
      {exams.map((exam) => (
        <div key={exam.id_exame} className="exam-card">
          <div className="exam-card__header">
            <div className="exam-card__header-content">
              <FileText className="exam-card__icon" />
              <h3 className="exam-card__title">{exam.tipo_exame}</h3>
            </div>
            <a href={exam.resultado_link} target="_blank" rel="noopener noreferrer" className="exam-card__button">
              <ExternalLink className="exam-card__button-icon" />
              Ver Resultado
            </a>
          </div>

          <div className="exam-card__content">
            <div className="exam-card__grid">
              <div className="exam-card__item">
                <Calendar className="exam-card__item-icon" />
                <div className="exam-card__item-content">
                  <p className="exam-card__label">Data de Realização</p>
                  <p className="exam-card__value">{formatDate(exam.data_realizacao)}</p>
                </div>
              </div>

              <div className="exam-card__item">
                <Building2 className="exam-card__item-icon" />
                <div className="exam-card__item-content">
                  <p className="exam-card__label">Laboratório</p>
                  <p className="exam-card__value">{exam.nome_laboratorio}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
