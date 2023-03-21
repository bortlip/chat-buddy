import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar({ onResetSession }) {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Chat</Link>
        </li>
        <li>
          <Link to="/settings">Settings</Link>
        </li>
        <li className="dropdown">
          <a href="" className="dropdown-toggle">
            Actions
          </a>
          <ul className="dropdown-menu">
            <li>
              <a onClick={() => onResetSession()()}>Reset Session</a>
            </li>
            <li>
              <a href="">Action 2</a>
            </li>
            <li>
              <a href="">Action 3</a>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
