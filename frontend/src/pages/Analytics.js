import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import axios from 'axios';

// Регистрация компонентов Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Analytics() {
  const [analytics, setAnalytics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/analytics');
        setAnalytics(response.data);
        setLoading(false);
      } catch (err) {
        setError('Ошибка при загрузке данных аналитики');
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const chartData = {
    labels: analytics.map(item => item.method),
    datasets: [
      {
        label: 'Количество запросов',
        data: analytics.map(item => item.count),
        backgroundColor: 'rgba(52, 152, 219, 0.5)',
        borderColor: 'rgba(52, 152, 219, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Популярность методов заваривания',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  if (loading) {
    return (
      <div className="card">
        <p>Загрузка данных...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <p className="error">{error}</p>
      </div>
    );
  }

  return (
    <div className="analytics">
      <div className="card">
        <h1 className="card-title">Аналитика использования</h1>
        <p>
          На этой странице вы можете увидеть статистику использования различных методов заваривания.
          Данные обновляются в реальном времени.
        </p>
      </div>

      <div className="chart-container">
        <Bar data={chartData} options={chartOptions} />
      </div>

      <div className="card">
        <h2 className="card-title">Статистика по методам</h2>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Метод заваривания</th>
              <th>Количество запросов</th>
            </tr>
          </thead>
          <tbody>
            {analytics.map((item, index) => (
              <tr key={index}>
                <td>{item.method}</td>
                <td>{item.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Analytics; 