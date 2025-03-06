const express = require('express');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const { OpenAI } = require('openai');
const Anthropic = require('@anthropic-ai/sdk');

const router = express.Router();

// Load agents configuration
const loadAgent = (agentName) => {
  const agentPath = path.join(__dirname, `../../agents/${agentName}.json`);
  return JSON.parse(fs.readFileSync(agentPath, 'utf8'));
};

// LLM Client configurations
const getLLMClient = () => {
  const provider = process.env.LLM_PROVIDER || 'claude';
  
  switch(provider) {
    case 'openai':
      return new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    case 'claude':
      return new Anthropic({ apiKey: process.env.CLAUDE_API_KEY });
    case 'deepseek':
      return { 
        chat: async (params) => {
          const response = await axios.post('https://api.deepseek.com/v1/chat/completions', {
            model: "deepseek-r1",
            messages: params.messages
          }, {
            headers: { Authorization: `Bearer ${process.env.DEEPSEEK_API_KEY}` }
          });
          return { choices: response.data.choices };
        }
      };
    default:
      throw new Error('Unsupported LLM provider');
  }
};

// POST /api/generate - Generate content using Copywriter agent
router.post('/generate', async (req, res) => {
  try {
    const { bankId, contentDescription, wordCount } = req.body;
    const llm = getLLMClient();
    const copywriter = loadAgent('copywriter');
    
    // Load bank details
    const banksPath = path.join(__dirname, '../../config/banks.json');
    const banks = JSON.parse(fs.readFileSync(banksPath, 'utf8'));
    const bank = banks.find(b => b.id === bankId);

    // Construct prompt
    const prompt = copywriter.prompt_template
      .replace('{{content_description}}', contentDescription)
      .replace('{{word_count}}', wordCount)
      .replace('{{brand_guidelines}}', JSON.stringify(bank.brand_guidelines));

    // LLM-specific formatting
    let response;
    switch(process.env.LLM_PROVIDER) {
      case 'claude':
        response = await llm.messages.create({
          model: "claude-3-haiku-20240307",
          max_tokens: 1024,
          messages: [{ role: "user", content: prompt }]
        });
        break;
      case 'openai':
        response = await llm.chat.completions.create({
          model: "gpt-4o",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 1024
        });
        break;
      case 'deepseek':
        response = await llm.chat({
          messages: [{ role: "user", content: prompt }]
        });
        break;
    }

    res.json({
      success: true,
      content: process.env.LLM_PROVIDER === 'claude' ? 
        response.content[0].text : 
        response.choices[0].message.content
    });
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({
      success: false,
      message: 'Content generation failed',
      error: error.message
    });
  }
});

// POST /api/review - Submit content for review
router.post('/review', async (req, res) => {
  try {
    const { content, bankId, agentNames } = req.body;
    const llm = getLLMClient();
    const reviews = [];

    for (const agentName of agentNames) {
      const agent = loadAgent(agentName);
      const banksPath = path.join(__dirname, '../../config/banks.json');
      const banks = JSON.parse(fs.readFileSync(banksPath, 'utf8'));
      const bank = banks.find(b => b.id === bankId);

      const prompt = agent.prompt_template
        .replace('{{content}}', content)
        .replace('{{regulatory_info}}', JSON.stringify(bank.regulatory_info))
        .replace('{{brand_guidelines}}', JSON.stringify(bank.brand_guidelines));

      let response;
      switch(process.env.LLM_PROVIDER) {
        case 'claude':
          response = await llm.messages.create({
            model: "claude-3-haiku-20240307",
            max_tokens: 1024,
            messages: [{ role: "user", content: prompt }]
          });
          break;
        case 'openai':
          response = await llm.chat.completions.create({
            model: "gpt-4o",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 1024
          });
          break;
        case 'deepseek':
          response = await llm.chat({
            messages: [{ role: "user", content: prompt }]
          });
          break;
      }

      reviews.push({
        agent: agentName,
        feedback: process.env.LLM_PROVIDER === 'claude' ? 
          response.content[0].text : 
          response.choices[0].message.content
      });
    }

    res.json({ success: true, reviews });
  } catch (error) {
    console.error('Review error:', error);
    res.status(500).json({
      success: false,
      message: 'Content review failed',
      error: error.message
    });
  }
});

// POST /api/regenerate - Regenerate content with selected feedback
router.post('/regenerate', async (req, res) => {
  try {
    const { originalContent, feedback, bankId } = req.body;
    const llm = getLLMClient();
    const copywriter = loadAgent('copywriter');
    
    const banksPath = path.join(__dirname, '../../config/banks.json');
    const banks = JSON.parse(fs.readFileSync(banksPath, 'utf8'));
    const bank = banks.find(b => b.id === bankId);

    const prompt = `Original content:\n${originalContent}\n\nFeedback to incorporate:\n${
      feedback.join('\n')
    }\n\nPlease rewrite the content incorporating this feedback. ${
      copywriter.prompt_template.split('Please review')[0]
    } ${JSON.stringify(bank.brand_guidelines)}`;

    let response;
    switch(process.env.LLM_PROVIDER) {
      case 'claude':
        response = await llm.messages.create({
          model: "claude-3-haiku-20240307",
          max_tokens: 1024,
          messages: [{ role: "user", content: prompt }]
        });
        break;
      case 'openai':
        response = await llm.chat.completions.create({
          model: "gpt-4o",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 1024
        });
        break;
      case 'deepseek':
        response = await llm.chat({
          messages: [{ role: "user", content: prompt }]
        });
        break;
    }

    res.json({
      success: true,
      content: process.env.LLM_PROVIDER === 'claude' ? 
        response.content[0].text : 
        response.choices[0].message.content
    });
  } catch (error) {
    console.error('Regeneration error:', error);
    res.status(500).json({
      success: false,
      message: 'Content regeneration failed',
      error: error.message
    });
  }
});

module.exports = router;
