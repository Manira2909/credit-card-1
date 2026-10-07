import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        alert("Login Success!");
        // window.location.href = "/payment"; // payment page ku poganum na
      } else {
        alert("Login Failed: " + (data.detail || "Invalid credentials"));
      }
    } catch (err) {
      alert("Login Failed: " + err.message);
    }
  };

  return (
    <div>
      <h1>Login !</h1>
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Username"
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}