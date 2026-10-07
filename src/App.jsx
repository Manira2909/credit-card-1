import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard.jsx';
import AddCard from './pages/AddCard.jsx';
import Payment from './pages/Payment.jsx';
import Login from './pages/Login.jsx';


function PrivateRoute({ children}) {
  const token = localStorage.getItem('access'); // <-- 'jwt' illama 'access'
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/add-card" element={<PrivateRoute><AddCard /></PrivateRoute>} />
        <Route path="/payment" element={<PrivateRoute><Payment /></PrivateRoute>} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;