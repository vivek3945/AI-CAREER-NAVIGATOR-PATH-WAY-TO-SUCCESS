
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Advisor from './pages/Advisor';
import SkillGapAnalysis from './pages/skill-gap';


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/advisor" element={<Advisor />} />
        <Route path="/skill-gap" element={<SkillGapAnalysis />} />
      </Routes>
    </Router>
  );
}

export default App;