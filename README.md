AI-powered interpreter for Infocom Interactive Fiction games

To setup:
1. clone repository
2. paste your openai api key into openai_creds.json
3. run ```pip install -r requirements.txt```

To use:
```python ai_player.py [FILENAME]```

|Flag|Function|Default|
|-|-|-|
|-d|toggles debug|False|
|-m|sets open model type, either gpt-4 or gpt-3.5-turbo|gpt-4|
|-l|sets the gameplay language for automatic translations (experimental)|English|

Tested with GPT-4. May still function with GPT-3.5-turbo but your mileage may vary.