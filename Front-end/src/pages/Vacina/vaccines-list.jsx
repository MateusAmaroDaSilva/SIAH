import { Syringe, Calendar, Package, MapPin, User } from "lucide-react"
import { formatDate } from "./vaccines-list.js"
import "./vaccines-list.css"

export default function VaccinesList({ vaccines }) {
  return (
    <div className="vaccines-list">
      {vaccines.map((vaccine) => (
        <div key={vaccine.id_vacina_aplicada} className="vaccine-card">
          <div className="vaccine-card__header">
            <div className="vaccine-card__header-content">
              <Syringe className="vaccine-card__icon" />
              <h3 className="vaccine-card__title">{vaccine.nome_vacina}</h3>
            </div>
            <span className="vaccine-card__badge">{vaccine.dose}</span>
          </div>

          <div className="vaccine-card__content">
            <div className="vaccine-card__grid">
              <div className="vaccine-card__item">
                <Calendar className="vaccine-card__item-icon" />
                <div className="vaccine-card__item-content">
                  <p className="vaccine-card__label">Data de Aplicação</p>
                  <p className="vaccine-card__value">{formatDate(vaccine.data_aplicacao)}</p>
                </div>
              </div>

              <div className="vaccine-card__item">
                <Package className="vaccine-card__item-icon" />
                <div className="vaccine-card__item-content">
                  <p className="vaccine-card__label">Lote</p>
                  <p className="vaccine-card__value">{vaccine.lote}</p>
                </div>
              </div>

              <div className="vaccine-card__item">
                <MapPin className="vaccine-card__item-icon" />
                <div className="vaccine-card__item-content">
                  <p className="vaccine-card__label">Local</p>
                  <p className="vaccine-card__value">{vaccine.hospital?.nome_hospital}</p>
                  <p className="vaccine-card__value vaccine-card__value--small">
                    {vaccine.hospital?.cidade} - {vaccine.hospital?.estado}
                  </p>
                </div>
              </div>

              <div className="vaccine-card__item">
                <User className="vaccine-card__item-icon" />
                <div className="vaccine-card__item-content">
                  <p className="vaccine-card__label">Aplicado por</p>
                  <p className="vaccine-card__value">{vaccine.profissional?.nome}</p>
                  <p className="vaccine-card__value vaccine-card__value--small">{vaccine.profissional?.crm_coren}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
