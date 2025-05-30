# Persian Voice Command System

## Description

Welcome to the **Persian Voice Command System**, an innovative Python project that empowers Persian speakers to control their Windows computers using voice commands. This application allows users to record voice commands in Persian, transcribe them into text using a fine-tuned AI model, and execute corresponding Windows commands securely. Built with a user-friendly [Streamlit](https://streamlit.io/) interface, it combines advanced AI technologies with a simple design, making it accessible for both everyday users and developers interested in AI-driven applications.

The system is optimized for Persian language processing, ensuring accurate transcription and command execution. By using local AI models, it prioritizes user privacy and supports offline functionality after initial setup, making it a robust solution for voice-based computer control.

## Features

- **Voice Recording**: Capture 5-second voice commands in Persian via a simple web interface.
- **Speech-to-Text Conversion**: Transcribe audio into Persian text using the Persian-optimized [Wav2Vec2 model](https://huggingface.co/m3hrdadfi/wav2vec2-large-xlsr-persian).
- **Command Execution**: Process transcribed text into secure Windows commands using [Ollama](https://ollama.com/) with the `qwen2.5` model.
- **Secure Execution**: Restrict commands to a predefined set, including:
  - Starting applications: Chrome, Firefox, Visual Studio Code, File Explorer
  - Opening directories: Downloads, Documents
  - Terminating processes: Chrome, Visual Studio Code
- **User-Friendly Interface**: Streamlit provides an intuitive web-based interface for seamless interaction.
- **Offline Capability**: Runs locally with downloaded models, ensuring privacy and functionality without internet dependency after setup.

## How It Works

The system integrates three core components:

1. **Voice Recording**: Uses [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) to record 5 seconds of audio from the user's microphone, saving it as a WAV file.
2. **Speech-to-Text Conversion**: Employs the `m3hrdadfi/wav2vec2-large-xlsr-persian` model from Hugging Face to transcribe audio into Persian text, with audio preprocessing handled by [Torchaudio](https://pytorch.org/audio/stable/index.html).
3. **Command Execution**: Processes transcribed text using Ollama's `qwen2.5` model to generate Windows commands, executed securely via Python's `subprocess` module.

The workflow is managed by [LangGraph](https://langchain-ai.github.io/langgraph/), ensuring a structured process from input to output, all accessible through a Streamlit interface.

## System Requirements

- **Operating System**: Windows (required for command execution).
- **Python**: Version 3.8 or higher.
- **Microphone**: A working microphone for voice input.
- **Internet**: Required for initial setup to download models.
- **Hardware**: GPU recommended for better performance, but CPU is sufficient.

## Installation

Follow these steps to set up the Persian Voice Command System:

1. **Install Python 3.8 or Higher**
   - Download and install from [Python.org](https://www.python.org/downloads/).

2. **Install Required Libraries**
   - Run the following command to install dependencies:
     ```bash
     pip install streamlit pyaudio transformers torchaudio torch langchain-core langchain-ollama langgraph
     ```
   - **Note for Windows Users**: PyAudio requires [PortAudio](http://www.portaudio.com/download.html). Install it and ensure it's in your system PATH.

3. **Install Ollama**
   - Follow instructions on [Ollama's website](https://ollama.com/).
   - Pull the required model:
     ```bash
     ollama pull qwen2.5
     ```
   - Start Ollama:
     ```bash
     ollama serve
     ```

4. **Clone the Repository**
     ```bash
     git clone https://github.com/armanjscript/Persian-Voice-Command-System.git
     ```

5. **Navigate to the Project Directory**
   - ```bash
     cd Persian-Voice-Command-System
     ```

6. **Run the Application**
   - ```bash
     streamlit run app.py
     ```

**Note**: A GPU enhances performance for speech-to-text and command generation, but the system runs on CPU as well. Ensure a stable internet connection for initial model downloads.

## Usage

1. **Launch the Application**
   - Run `streamlit run app.py` to open the app in your default web browser.

2. **Interact with the Interface**
   - Click **"Record Command (5 seconds)"** to record a voice command in Persian.
   - The recorded audio will play back for verification.
   - Click **"Process Command"** to transcribe the audio and execute the command.
   - View the transcribed text and command execution result in the interface.

3. **Supported Commands**
   - Examples of supported Persian commands:
     - "مرورگر را باز کن" (Open Chrome browser)
     - "دانلودها" (Open Downloads folder)
     - "کد را ببند" (Close Visual Studio Code)

**Important Notes**:
- Ensure a working microphone is connected.
- Use Persian commands for optimal transcription accuracy.
- The system restricts commands to a safe set to prevent unauthorized actions.

## Technologies Used

| Technology       | Role                                                                 |
|------------------|----------------------------------------------------------------------|
| **Python**       | Primary programming language.                                        |
| **Streamlit**    | Creates the interactive web interface.                               |
| **PyAudio**      | Records audio from the microphone.                                   |
| **Transformers** | Handles speech-to-text conversion with Wav2Vec2 model.               |
| **Torchaudio**   | Processes audio files for transcription.                             |
| **Torch**        | Runs the speech-to-text model on CPU or GPU.                         |
| **Langchain**    | Manages prompts and output parsing for command generation.           |
| **LangGraph**    | Structures the workflow for efficient task management.               |
| **Ollama**       | Runs the local language model for command processing.                |
| **Subprocess**   | Executes Windows commands securely.                                  |

## Security

The system prioritizes security by restricting command execution to a predefined set of safe commands. This prevents malicious or unauthorized actions, limiting operations to starting specific applications (Chrome, Firefox, VS Code, Explorer), opening designated directories (Downloads, Documents), and terminating specific processes (Chrome, VS Code).

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository on [GitHub](https://github.com/armanjscript).
2. Create a new branch for your changes.
3. Submit a pull request with a clear description.
4. For bug reports or feature requests, open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, open an issue on [GitHub](https://github.com/armanjscript) or email [armannew73@gmail.com].