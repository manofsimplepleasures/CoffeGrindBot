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
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
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

const Analytics = () => {
  const [ratings, setRatings] = useState({
    labels: [],
    data: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/analytics/ratings');
        const { ratings_by_coffee } = response.data;
        
        setRatings({
          labels: ratings_by_coffee.map(item => item.coffee_type),
          data: ratings_by_coffee.map(item => item.average_rating),
        });
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      }
    };

    fetchData();
  }, []);

  const chartData = {
    labels: ratings.labels,
    datasets: [
      {
        label: 'Средняя оценка',
        data: ratings.data,
        backgroundColor: [
          'rgba(121, 85, 72, 0.6)',
          'rgba(141, 110, 99, 0.6)',
          'rgba(165, 138, 127, 0.6)',
        ],
        borderColor: [
          'rgb(121, 85, 72)',
          'rgb(141, 110, 99)',
          'rgb(165, 138, 127)',
        ],
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
        text: 'Средние оценки по типам кофе',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 5,
      },
    },
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Аналитика
      </Typography>

      <Grid container spacing={3}>
        {/* График оценок */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Bar data={chartData} options={chartOptions} />
          </Paper>
        </Grid>

        {/* Статистика по типам кофе */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Статистика по типам кофе
            </Typography>
            <Grid container spacing={2}>
              {ratings.labels.map((label, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1">
                        {label}
                      </Typography>
                      <Typography variant="h4">
                        {ratings.data[index].toFixed(1)}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Средняя оценка
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

export default Analytics; 