const express = require('express');
const path = require('path');
const fs = require('fs');

const router = express.Router();

// GET /api/banks - Fetch list of available banks
router.get('/', (req, res) => {
  try {
    const banksPath = path.join(__dirname, '../../config/banks.json');
    const banksData = JSON.parse(fs.readFileSync(banksPath, 'utf8'));
    
    // Return a simplified version for the frontend
    const simplifiedBanks = banksData.map(bank => ({
      id: bank.id,
      name: bank.name,
      description: bank.description
    }));
    
    res.json({
      success: true,
      data: simplifiedBanks
    });
  } catch (error) {
    console.error('Error fetching banks:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch banks',
      error: error.message
    });
  }
});

// GET /api/banks/:id - Fetch a specific bank's details
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const banksPath = path.join(__dirname, '../../config/banks.json');
    const banksData = JSON.parse(fs.readFileSync(banksPath, 'utf8'));
    
    const bank = banksData.find(b => b.id === id);
    
    if (!bank) {
      return res.status(404).json({
        success: false,
        message: `Bank with ID ${id} not found`
      });
    }
    
    res.json({
      success: true,
      data: bank
    });
  } catch (error) {
    console.error(`Error fetching bank ${req.params.id}:`, error);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch bank details',
      error: error.message
    });
  }
});

module.exports = router;
