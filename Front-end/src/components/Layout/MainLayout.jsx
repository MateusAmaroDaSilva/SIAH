import EHRSidebar from "../Side-bar/ehr-sidebar";
import EHRHeader from "..//Header/ehr-header";
import "./MainLayout.css"; 

export default function MainLayout({ children }) {
  return (
    <div className="ehr-app">
      <EHRSidebar />
      <div className="ehr-app__main">
        <EHRHeader />
        <main className="ehr-app__content">{children}</main>
      </div>
    </div>
  );
}
