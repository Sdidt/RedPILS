import { BrowserRouter , Route,Routes} from 'react-router-dom';

import logo from './logo.svg';
import SearchPage from './search_page';
import Navbar from './navbar';
import Insights from './insights';
import './App.css';

function App() {
  return (
    <div className="mainApp">
      <Navbar/>
      <div className='App'>
        <BrowserRouter basename={process.env.PUBLIC_URL}>
            <Routes>
              <Route path='/' element={<SearchPage/>}/>
              {/* <Route path='/insights' element={<Insights />}/>
              <Route path='/projects' element={<SearchPage />} />x
              <Route path='/about' element={<SearchPage/>} /> */}
            </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
