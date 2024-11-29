const dotenv = require('dotenv');
dotenv.config();

module.exports.getEnvVars = () => ({
  openaiApiKey: process.env.OPENAI_API_KEY,
  instagramAccessToken: process.env.INSTAGRAM_ACCESS_TOKEN,
}); 