import { User, FileText, Activity, FlaskConical, Syringe, Heart } from "lucide-react"
import "./ehr-sidebar.css"

export default function EHRSidebar({ activeSection, onSectionChange }) {
  const menuItems = [
    { id: "paciente", label: "Dados do Paciente", icon: User },
    { id: "/consulta", label: "Consultas", icon: FileText },
    { id: "triagem", label: "Triagem", icon: Activity },
    { id: "exame", label: "Exames", icon: FlaskConical },
    { id: "vacina", label: "Vacinas", icon: Syringe },
  ]

  return (
    <aside className="ehr-sidebar">
      <div className="ehr-sidebar__header">
        <div className="ehr-sidebar__logo">
          <Heart className="ehr-sidebar__logo-icon" />
          <h1 className="ehr-sidebar__logo-text">Sistema EHR</h1>
        </div>
      </div>

      <nav className="ehr-sidebar__nav">
        <div className="ehr-sidebar__menu">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = activeSection === item.id

            return (
              <button
                key={item.id}
                className={`ehr-sidebar__menu-item ${isActive ? "ehr-sidebar__menu-item--active" : ""}`}
                onClick={() => onSectionChange(item.id)}
              >
                <Icon className="ehr-sidebar__menu-icon" />
                <span>{item.label}</span>
              </button>
            )
          })}
        </div>
      </nav>

      <div className="ehr-sidebar__footer">
        <p className="ehr-sidebar__footer-text">Sistema de Prontuário Eletrônico</p>
      </div>
    </aside>
  )
}
