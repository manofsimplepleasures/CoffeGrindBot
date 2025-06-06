import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';

const Settings = () => {
  const [settings, setSettings] = useState({
    grindSize: '',
    grindTime: '',
    coffeeType: '',
    brewMethod: '',
  });

  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setSettings(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // TODO: Реализовать отправку настроек на сервер
      setMessage({
        type: 'success',
        text: 'Настройки успешно сохранены',
      });
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Ошибка при сохранении настроек',
      });
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Настройки
      </Typography>

      {message.text && (
        <Alert severity={message.type} sx={{ mb: 2 }}>
          {message.text}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Крупность помола</InputLabel>
                <Select
                  name="grindSize"
                  value={settings.grindSize}
                  onChange={handleChange}
                  label="Крупность помола"
                >
                  <MenuItem value="very_fine">Очень мелкий</MenuItem>
                  <MenuItem value="fine">Мелкий</MenuItem>
                  <MenuItem value="medium">Средний</MenuItem>
                  <MenuItem value="coarse">Крупный</MenuItem>
                  <MenuItem value="very_coarse">Очень крупный</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                name="grindTime"
                label="Время помола (секунды)"
                type="number"
                value={settings.grindTime}
                onChange={handleChange}
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Тип кофе</InputLabel>
                <Select
                  name="coffeeType"
                  value={settings.coffeeType}
                  onChange={handleChange}
                  label="Тип кофе"
                >
                  <MenuItem value="arabica">Арабика</MenuItem>
                  <MenuItem value="robusta">Робуста</MenuItem>
                  <MenuItem value="blend">Смесь</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Метод заваривания</InputLabel>
                <Select
                  name="brewMethod"
                  value={settings.brewMethod}
                  onChange={handleChange}
                  label="Метод заваривания"
                >
                  <MenuItem value="espresso">Эспрессо</MenuItem>
                  <MenuItem value="pour_over">Pour Over</MenuItem>
                  <MenuItem value="french_press">Френч-пресс</MenuItem>
                  <MenuItem value="aero_press">Аэропресс</MenuItem>
                  <MenuItem value="cold_brew">Колд-брю</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                fullWidth
              >
                Сохранить настройки
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};

export default Settings; 