const express = require('express');
const path = require('path');
const cors = require('cors');
const dotenv = require('dotenv');
const fs = require('fs');

// Load environment variables from .env.local if it exists, otherwise from env.environment
const envPath = fs.existsSync(path.join(__dirname, '../.env.local')) 
  ? path.join(__dirname, '../.env.local') 
  : path.join(__dirname, '../env.environment');

dotenv.config({ path: envPath });

// Import routes
const banksRoutes = require('./routes/banks');
const llmRoutes = require('./routes/llm');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Routes
app.use('/api/banks', banksRoutes);
app.use('/api', llmRoutes);

// Serve the main HTML file for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'An error occurred',
    error: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Using LLM provider: ${process.env.LLM_PROVIDER || 'claude'}`);
});
