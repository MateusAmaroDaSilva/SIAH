import { Routes, Route } from "react-router-dom";
import Cadastro from "./pages/Cadastro/cadastro.jsx";
import Informacoes from "./pages/Informacoes/informacoes.jsx";
import ConsultationsList from "./pages/Consulta/consultations-list.jsx";
import ExamsList from "./pages/Exame/exams-list.jsx";
import PatientCard from "./pages/Paciente/patient-card.jsx";
import TriageCard from "./pages/Triagem/triage-card.jsx";
import VaccinesList from "./pages/Vacina/vaccines-list.jsx";
import MainLayout from "./components/Layout/MainLayout.jsx";


function App() {
  return (
    <Routes>
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/informacoes/:cpf" element={<Informacoes />} />
      <Route
        path="/consulta"
        element={
          <MainLayout>
            <ConsultationsList />
          </MainLayout>
        }
      />
      <Route
        path="/exame"
        element={
          <MainLayout>
            <ExamsList />
          </MainLayout>
        }
      />
      <Route
        path="/paciente"
        element={
          <MainLayout>
            <PatientCard />
          </MainLayout>
        }
      />
      <Route
        path="/triagem"
        element={
          <MainLayout>
            <TriageCard />
          </MainLayout>
        }
      />
      <Route
        path="/vacina"
        element={
          <MainLayout>
            <VaccinesList />
          </MainLayout>
        }
      />
    </Routes>
  );
}

export default App;