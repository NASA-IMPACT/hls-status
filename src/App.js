import logo from './logo.svg';
import './App.css';
import StatusPage from './components/StatusPage';
import NavBar from './components/NavBar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import RssFeedPage from './components/RSSFeed';
import Metric from './components/Metric';


function App() {
  return (
    <div>
      <NavBar />
      <BrowserRouter>
        <main>
          <Routes>
            <Route path="/all-feeds" element={<RssFeedPage/>} />
            <Route path="/metrics" element={<Metric/>} />
            <Route path="/" element = {<StatusPage/>} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
