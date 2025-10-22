import { User, Phone, Mail, MapPin, Calendar, AlertCircle, Activity } from "lucide-react"
import { calculateAge } from "./patient-card.js"
import "./patient-card.css"

export default function PatientCard({ patient }) {
  const age = calculateAge(patient.data_nascimento)

  return (
    <div className="patient-card">
      <div className="patient-card__header">
        {patient.foto_rosto_link ? (
          <img
            src={patient.foto_rosto_link || "/placeholder.svg"}
            alt={patient.nome}
            className="patient-card__avatar"
          />
        ) : (
          <div className="patient-card__avatar-fallback">
            {patient.nome
              .split(" ")
              .map((n) => n[0])
              .join("")
              .slice(0, 2)}
          </div>
        )}
        <h2 className="patient-card__name">{patient.nome}</h2>
        <p className="patient-card__age">{age} anos</p>
      </div>

      <div className="patient-card__info">
        <div className="patient-card__info-item">
          <User className="patient-card__icon" />
          <div className="patient-card__info-content">
            <p className="patient-card__label">CPF</p>
            <p className="patient-card__value">{patient.cpf}</p>
          </div>
        </div>

        <div className="patient-card__info-item">
          <Calendar className="patient-card__icon" />
          <div className="patient-card__info-content">
            <p className="patient-card__label">Data de Nascimento</p>
            <p className="patient-card__value">{new Date(patient.data_nascimento).toLocaleDateString("pt-BR")}</p>
          </div>
        </div>

        <div className="patient-card__info-item">
          <Phone className="patient-card__icon" />
          <div className="patient-card__info-content">
            <p className="patient-card__label">Telefone</p>
            <p className="patient-card__value">{patient.telefone}</p>
          </div>
        </div>

        <div className="patient-card__info-item">
          <Mail className="patient-card__icon" />
          <div className="patient-card__info-content">
            <p className="patient-card__label">Email</p>
            <p className="patient-card__value">{patient.email}</p>
          </div>
        </div>

        <div className="patient-card__info-item">
          <MapPin className="patient-card__icon" />
          <div className="patient-card__info-content">
            <p className="patient-card__label">Endereço</p>
            <p className="patient-card__value">{patient.endereco}</p>
          </div>
        </div>

        <div className="patient-card__divider">
          <div className="patient-card__section">
            <div className="patient-card__info-item">
              <AlertCircle className="patient-card__icon" style={{ color: "var(--color-destructive)" }} />
              <div className="patient-card__info-content">
                <p className="patient-card__label">Alergias</p>
                <div className="patient-card__badges">
                  {patient.alergias.split(",").map((alergia, index) => (
                    <span key={index} className="patient-card__badge patient-card__badge--destructive">
                      {alergia.trim()}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="patient-card__section">
            <div className="patient-card__info-item">
              <Activity className="patient-card__icon" />
              <div className="patient-card__info-content">
                <p className="patient-card__label">Condições Crônicas</p>
                <div className="patient-card__badges">
                  {patient.condicoes_cronicas.split(",").map((condicao, index) => (
                    <span key={index} className="patient-card__badge patient-card__badge--secondary">
                      {condicao.trim()}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
