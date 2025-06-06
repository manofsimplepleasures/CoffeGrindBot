import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

// Регистрация компонентов Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    newUsersToday: 0,
    popularSettings: [],
  });
  const [trends, setTrends] = useState({
    labels: [],
    data: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Получение статистики пользователей
        const userStats = await axios.get('http://localhost:5000/api/stats/users');
        setStats(prev => ({ ...prev, ...userStats.data }));

        // Получение трендов
        const trendsData = await axios.get('http://localhost:5000/api/analytics/trends');
        const { daily_usage } = trendsData.data;
        
        setTrends({
          labels: daily_usage.map(item => item.date),
          data: daily_usage.map(item => item.count),
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    fetchData();
  }, []);

  const chartData = {
    labels: trends.labels,
    datasets: [
      {
        label: 'Использование бота',
        data: trends.data,
        borderColor: '#795548',
        backgroundColor: 'rgba(121, 85, 72, 0.5)',
        tension: 0.4,
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
        text: 'Тренд использования бота',
      },
    },
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Дашборд
      </Typography>

      <Grid container spacing={3}>
        {/* Статистика пользователей */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Пользователи
              </Typography>
              <Typography variant="h3">{stats.totalUsers}</Typography>
              <Typography color="textSecondary">
                Новых сегодня: {stats.newUsersToday}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* График трендов */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Line data={chartData} options={chartOptions} />
          </Paper>
        </Grid>

        {/* Популярные настройки */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Популярные настройки
            </Typography>
            <Grid container spacing={2}>
              {stats.popularSettings.map((setting, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1">
                        {setting.coffee_type} - {setting.brew_method}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Крупность: {setting.grind_size}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Использований: {setting.count}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 