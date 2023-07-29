# Send trading notifications to your Telegram Bot

The objective of Zetralerts is to receive timely notifications whenever high probability setups materialize in the trading landscape. Once these scenarios are identified, one can conduct further in-depth analysis before executing any trades. The underlying concept revolves around the seamless fusion of automation and human discretion in the realm of trading, optimizing decision-making processes for enhanced results.

*Zetralerts is under heavy development*. See the disclaimer below. 

## Getting started

Lets help you get started working locally with Zetralerts. 

### Installation

Clone the Zetralerts folder from Github:

     git clone https://github.com/zeta-zetra/zetralerts.git

### Create the .env file

You need to create the `.env` file which will contain all of the necessary environment variables. Take a look at the .env.sample 
file of the environment variables.

### Setting up Telegram Bot

Follow these steps to setup your Telegram bot:

 1. Search for @botfather in Telegram.

 2. Type in /newbot 

 3. Set a name for your bot

 4. Copy your Token API 
 
You can follow the steps in the [article](https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/) to get started as well.

### Run Test

Once you have your Telegram API token, in the .env file place it the TELEGRAM_TOKEN environment variable. 

In your bot, write anything. e.g: `Hello`, `Test`. This will be needed when Zetralerts attempts to get the Chat ID. 

You can then run the following command:

    python run_test.py

If successful, then you should get the close price of the EURUSD at the 15-minute timeframe. 

## Available Alerts 

Currently these are the available alerts:

- [x] Fibonacci line breakout

- [x] Triangle patterns

- [x] Rounding bottom patterns

More details about the alerts can be found on the [online book](https://zeta-zetra.github.io/docs-forex-strategies-python/)

## Custom Alerts

*Coming soon*

## Frontend

A streamlit application is under development which will make it easier to view all available alerts, create custom alerts. You can also
activate and deactivate the alerts from the app.

You can start the app by running:

    streamlit run app.py


## Deployment

You want to receive notifications even when your workstation is off. The best option would be to deploy Zetralerts on a remote server.

We want to make it seamlessly to deploy onto a server, in fact it needs to be one line:

    fab deploy-zetralerts

To use the above command, make sure information about your server is placed in the `.env` file. The server should be Linux ubuntu based. 

*Video coming soon*

## Disclaimer

We want to emphasize that this is purely for educational purposes only. We do not offer any financial advice, recommendations, or make any guarantees of profit or success. Trading carries a risk of loss, and it is important to always consult with a qualified professional before making any trading decisions.

## License 

MIT License

## Contact

You can reach me at: info@zetra.io

