import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

// Loading Skeleton Component
const SkeletonCard = () => <div className="h-32 bg-gray-200 rounded-2xl animate-pulse"></div>
const SkeletonRow = () => <div className="h-12 bg-gray-100 rounded-lg animate-pulse mb-2"></div>

const StatCard = ({ title, value, color = "text-gray-900", icon }) => (
  <div className="bg-white p-6 rounded-2xl shadow-md border-gray-100 hover:shadow-lg transition">
    <p className="text-gray-500 text-sm font-medium">{title}</p>
    <p className={`text-3xl font-bold mt-2 ${color}`}>{value}</p>
  </div>
);

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get('/dashboard/summary'); // NEW API
        setSummary(response.data);
      } catch (error) {
        if (error.response?.status === 401) {
          setError('Session expired. Please login again.');
          localStorage.removeItem('jwt');
          setTimeout(() => navigate('/login'), 2000);
        } else {
          setError('Failed to fetch dashboard data. Check if backend is running.');
        }
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [navigate]);

  // JWT Error Screen
  if (error) {
    return (
      <div className="p-6 min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-100 text-red-700 p-6 rounded-xl text-center border-red-300 max-w-md">
          <h2 className="font-bold text-lg mb-2">Authentication Error</h2>
          <p>{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-500 mb-6">Overview of your spending and transactions</p>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {loading ? (
            <>
              <SkeletonCard /><SkeletonCard /><SkeletonCard /><SkeletonCard />
            </>
          ) : (
            <>
              <StatCard title="Total Spent" value={`₹${summary.total_amount_spent.toLocaleString('en-IN')}`} />
              <StatCard title="Available Credit" value={`₹${summary.available_credit_limit.toLocaleString('en-IN')}`} color="text-green-600" />
              <StatCard title="Total Transactions" value={summary.total_transactions} />
              <StatCard title="This Month" value={`₹${summary.current_month_spending.toLocaleString('en-IN')}`} color="text-blue-600" />
            </>
          )}
        </div>

        {/* Last 5 Transactions Table */}
        <div className="bg-white rounded-2xl shadow-md p-6 border-gray-100">
          <h2 className="font-semibold text-xl mb-4">Last 5 Transactions</h2>
          
          {loading ? (
            <div><SkeletonRow /><SkeletonRow /><SkeletonRow /><SkeletonRow /><SkeletonRow /></div>
          ) : summary.last_5_transactions.length === 0 ? (
            <div className="text-center py-10 text-gray-500">
              <p>No transactions yet.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="text-gray-500 text-sm border-b">
                  <tr>
                    <th className="py-3 font-semibold">Date</th>
                    <th className="font-semibold">Card</th>
                    <th className="font-semibold">Amount</th>
                    <th className="font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.last_5_transactions.map((txn, i) => (
                    <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
                      <td className="py-4">{new Date(txn.date).toLocaleDateString('en-IN')}</td>
                      <td className="font-mono text-sm">{txn.masked_card_number}</td>
                      <td className="font-bold">₹{txn.amount.toLocaleString('en-IN')}</td>
                      <td>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          txn.status === 'success' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {txn.status.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex gap-3">
          <button 
            onClick={() => navigate('/add-card')} 
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-bold hover:bg-indigo-700 transition"
          >
            + Add New Card
          </button>
          <button 
            onClick={() => navigate('/payment')} 
            className="px-6 py-3 bg-green-600 text-white rounded-lg font-bold hover:bg-green-700 transition"
          >
            Make Payment
          </button>
        </div>

      </div>
    </div>
  );
}