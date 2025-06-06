import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <img
            src="/logo.png"
            alt="Coffee Grinder Bot"
            style={{ height: '40px', marginRight: '10px' }}
          />
          Coffee Grinder Bot
        </Typography>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            component={RouterLink}
            to="/"
            color="inherit"
            startIcon={<DashboardIcon />}
          >
            Дашборд
          </Button>
          <Button
            component={RouterLink}
            to="/analytics"
            color="inherit"
            startIcon={<AnalyticsIcon />}
          >
            Аналитика
          </Button>
          <Button
            component={RouterLink}
            to="/settings"
            color="inherit"
            startIcon={<SettingsIcon />}
          >
            Настройки
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 