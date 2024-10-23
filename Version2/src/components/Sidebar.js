import React, { useState } from 'react';
import { NavLink, Link, useLocation } from 'react-router-dom';

const SidebarItem = ({ icon, text, to, subItems }) => {
  const [isHovered, setIsHovered] = useState(false);
  const location = useLocation();
  const isActive = location.pathname.startsWith(to);

  return (
    <div
      className="relative w-full group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <NavLink
        to={to}
        className={({ isActive }) =>
          `flex flex-col items-center justify-center p-2 w-full h-20 ${
            isActive ? 'bg-premium-gold' : 'hover:bg-premium-gold-dark'
          }`
        }
      >
        {({ isActive }) => (
          <>
            <span className={`material-icons text-2xl mb-0 ${isActive ? 'text-premium-black' : 'text-premium-gold-light'}`}>
              {icon}
            </span>
            <span className={`text-[10px] text-center ${isActive ? 'text-premium-black' : 'text-premium-gold-light'}`}>
              {text}
            </span>
          </>
        )}
      </NavLink>
      {subItems && isHovered && (
        <div className="absolute left-full top-0 ml-2 bg-premium-black border border-premium-gold rounded-lg p-2 z-10 w-48">
          <div className="absolute right-full top-0 w-3 h-full" />
          {subItems.map((item, index) => (
            <Link
              key={index}
              to={item.to}
              className="block py-1 px-2 text-premium-gold-light hover:bg-premium-gold-dark rounded"
            >
              {item.text}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

function Sidebar() {
  return (
    <div className="bg-premium-black text-premium-gold-light h-full w-20 flex flex-col items-center py-4">
      <div className="w-12 h-12 bg-premium-gold rounded-full mb-8"></div>
      <nav className="flex flex-col items-center w-full">
        <SidebarItem icon="dashboard" text="Dashboard" to="/" />
        <SidebarItem 
          icon="people" 
          text="Clients" 
          to="/clients"
          subItems={[
            { text: "All Clients", to: "/clients" },
            { text: "Add Client", to: "/clients/add" }
          ]}
        />
        <SidebarItem icon="event" text="Appointments" to="/appointments" />
        <SidebarItem 
          icon="folder" 
          text="Documents" 
          to="/documents"
          subItems={[
            { text: "All Documents", to: "/documents" },
            { text: "Upload", to: "/documents/upload" }
          ]}
        />
        <SidebarItem icon="analytics" text="Analyzer" to="/analyzer" />
        <SidebarItem icon="bar_chart" text="Reports" to="/reports" />
        <SidebarItem icon="settings" text="Settings" to="/settings" />
      </nav>
    </div>
  );
}

export default Sidebar;