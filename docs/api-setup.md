# Setting Up the Gemini API

## Getting Your API Key

1. **Visit Google AI Studio:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key:**
   - Click on "Get API key" button
   - If you don't have an API key, click "Create API key"
   - Copy your API key immediately (you won't be able to see it again)

3. **Set Up API Key:**
   ```bash
   # On Unix/macOS
   export GEMINI_API_KEY='your-api-key-here'

   # On Windows (PowerShell)
   $env:GEMINI_API_KEY='your-api-key-here'
   ```

## Subscription Plans

1. **Free Trial:**
   - 100 free generations per month
   - No credit card required
   - 30-day trial period

2. **Paid Plans:**
   - Pay-as-you-go
   - Enterprise (custom pricing)
   - Student (special pricing)

3. **Usage Limits:**
   - Free tier: 100 generations/month
   - Standard tier: Up to 1000 generations/month
   - Enterprise: Custom limits

## Best Practices

- Never commit your API key to version control
- Use environment variables for API key storage
- Monitor your usage in Google AI Studio dashboard
- Consider rate limiting in your application 