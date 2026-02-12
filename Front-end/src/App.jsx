import { Routes, Route } from "react-router-dom";
import Cadastro from "./pages/Cadastro/cadastro.jsx";
import Informacoes from "./pages/Informacoes/informacoes.jsx";

function App() {
  return (
    <Routes>
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/informacoes/:cpf" element={<Informacoes />} />
    </Routes>
  );
}

export default App;