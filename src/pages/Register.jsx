import React, { useState } from 'react'
import api from '../api/axios'
import { useNavigate, Link } from 'react-router-dom'


export default function Register(){
  const [email,setEmail]=useState(''), [pwd,setPwd]=useState('')
  const nav=useNavigate()
  const submit=async(e)=>{
    e.preventDefault()
    await api.post('/api/auth/register', {email, password: pwd})
    alert('Registered ma! Login pannu')
    nav('/')
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-500 to-blue-600">
      <form onSubmit={submit} className="bg-white p-8 rounded-2xl shadow-xl w-96">
        <h1 className="text-2xl font-bold mb-6">Register ma!</h1>
        <input className="w-full p-3 border rounded mb-3" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/>
        <input className="w-full p-3 border rounded mb-4" type="password" placeholder="Password (min 6)" value={pwd} onChange={e=>setPwd(e.target.value)} required/>
        <button className="w-full bg-green-600 text-white p-3 rounded font-bold">Register</button>
        <Link to="/" className="text-sm text-blue-600 mt-3 block text-center">Already have account? Login</Link>
      </form>
    </div>
  )
}