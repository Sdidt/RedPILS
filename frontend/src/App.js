import { BrowserRouter , Route,Routes} from 'react-router-dom';

import logo from './logo.svg';
import SearchPage from './search_page';
import Navbar from './navbar';
import './App.css';

function App() {
  return (
    <div className="mainApp">
      <Navbar/>
      <div className='App'>
        <BrowserRouter basename={process.env.PUBLIC_URL}>
            <Routes>
              <Route path='/' element={<SearchPage/>}/>
              <Route path='/workexperience' element={<SearchPage />}/>
              <Route path='/projects' element={<SearchPage />} />
              <Route path='/about' element={<SearchPage/>} />
            </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
