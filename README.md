# Chatbot with OpenAI GPT-3.5 Turbo

This is a chatbot powered by OpenAI's GPT-3.5 Turbo model that can answer questions from the documents deposited in the /docs directory, as it will generate a vector file (index.json) and perform specific API calls using function intent using Python. It allows you to interact with the chatbot to ask any question about the documents supplied, obtain account balance (dummy function), and retrieve stock market information from Yahoo finance as an example.

## Installation

To run this chatbot, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/support-function-chatbot.git
```

2. Navigate to the project directory:

```bash
cd support-function-chatbot
```

3. Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Configuration

You will need to set up your OpenAI API key. Replace `'YOUR-KEY-HERE'` in the code with your actual OpenAI API key.

```python
os.environ["OPENAI_API_KEY"] = 'YOUR-KEY-HERE'
openai.api_key = "YOUR-KEY-HERE" 
```

## Usage

Once you've completed the installation and configuration, you can run the chatbot by executing the Python script. Use the following command:

```bash
streamlit chatbot.py
```

This will start the chatbot interface, and you can interact with it using Streamlit.

## Features

1. **FAQ Responses:** The chatbot can answer frequently asked questions using GPT-3.5 Turbo's language generation capabilities.

2. **Function Calls:** The chatbot can call specific Python functions based on user intent. Two example functions are included:

    - `get_saldo(cuenta)`: This function returns a hardcoded account balance.
    - `get_stock(cuenta)`: This function retrieves stock market information using Yahoo Finance.

3. **Dynamic Learning:** The chatbot can learn and improve its responses over time by leveraging a pre-built index of documents.

## How to Use

1. Run the chatbot as instructed above.

2. Enter your questions or commands in the chat input field.

3. The chatbot will respond with answers or perform actions based on your input.

4. You can also use the sidebar to view additional information and instructions.

## Contributing

If you want to contribute to this project or improve the chatbot's functionality, please follow these guidelines:

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine.

3. Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

4. Make your changes and commit them:

```bash
git commit -m "Add your feature or fix"
```

5. Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request (PR) on the original repository, explaining your changes and improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This chatbot is powered by OpenAI's GPT-3.5 Turbo model and was developed by [Marvin Nahmias](https://github.com/your-username).

If you have any questions or encounter any issues, please feel free to [create an issue](https://github.com/your-username/your-chatbot-repo/issues) on this repository.