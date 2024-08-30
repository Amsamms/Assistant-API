
# Assistant API Streamlit App

This is a Streamlit-based web application that allows users to interact with various OpenAI assistants through a chat interface. The app provides the flexibility to use either a default set of assistants or user-provided assistants based on an OpenAI API key.

## Features

- **API Key Input**: Securely enter your OpenAI API key through a password-protected input field.
- **Assistant Selection**: Choose from a list of available assistants fetched using the provided API key.
- **Custom Instructions**: Automatically fetch and use the built-in instructions of the selected assistant during the chat.
- **Chat Interface**: Engage in a chat with the selected assistant, with chat history displayed in the app.
- **Session Management**: Start and exit chat sessions, with the option to reset and clear chat history.

## Requirements

- Python 3.7+
- Streamlit
- OpenAI Python client library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/assistant-api-streamlit.git
   ```
2. Navigate to the project directory:
   ```bash
   cd assistant-api-streamlit
   ```
3. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to `http://localhost:8501`.

3. Enter your OpenAI API key in the sidebar. Choose whether to use the default assistants or your own.

4. Select an assistant from the dropdown menu.

5. Click "Start Chat" to begin the conversation with the assistant. You can type your messages in the chat input field.

6. To end the chat session, click "Exit Chat". This will reset the chat history.

## File Structure

- `app.py`: The main application code.
- `README.md`: This file, which provides an overview and instructions for the app.
- `requirements.txt`: Lists the Python packages required to run the app.

## Configuration

- **OpenAI API Key**: The application requires a valid OpenAI API key to fetch available assistants and engage in conversations.

## Notes

- Ensure your API key has the necessary permissions to access the OpenAI services.
- The application uses the `gpt-4-o` model by default but can be configured to use other available models.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for providing the API services.
- [Streamlit](https://www.streamlit.io/) for the amazing framework that made this app possible.
