require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Configuration, OpenAIApi } = require('openai');

const app = express();
const port = 3000;

app.use(cors()); // Use cors middleware to allow cross-origin requests
app.use(bodyParser.json());

// Assuming Configuration and OpenAIApi are correctly imported based on the version of your package
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

app.post('/send-to-gpt', async (req, res) => {
  try {
    const { prompt } = req.body;
    const completion = await openai.createCompletion({
      model: "text-davinci-003", // Adjust this to the model you intend to use
      prompt: prompt,
      max_tokens: 150,
      temperature: 0.7,
    });
    res.json({ text: completion.data.choices[0].text });
  } catch (error) {
    console.error("Failed to fetch from OpenAI:", error);
    res.status(500).json({ error: "Failed to generate response from OpenAI" });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
