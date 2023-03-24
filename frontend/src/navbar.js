import {NavLink,Link} from 'react-router-dom';
import { BsPersonFill } from 'react-icons/bs';
import { FaHome } from 'react-icons/fa';
import { MdWork } from 'react-icons/md';
import { AiFillProject } from 'react-icons/ai';
import { BsMap ,BsTelephone} from 'react-icons/bs';

const Navbar = () => {
    return (
        <nav className='navbar'>
            <h1 className='navbar-logo'>RedPils</h1>
            <ul className='navbar-links'>
                <li className='navbar-item'>
                <a href='/'>Search</a>
                </li>
                <li className='navbar-item'>
                <a href='/workexperience'>Insights</a>
                </li>
            </ul>
        </nav>
      );
}
 
export default Navbar;