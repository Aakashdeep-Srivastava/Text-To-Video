# PowerPoint Presentation Generator with Gemini Pro

This project is a Streamlit-based web application that generates PowerPoint presentations using Google's Gemini Pro AI model. Users can input a topic, and the application will automatically create a presentation with relevant slide titles and content.

## Features

- Generate slide titles and content using Gemini Pro AI
- Create PowerPoint presentations automatically
- Easy-to-use web interface built with Streamlit
- Customizable font sizes for slide titles and content

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- A Google Cloud account with access to the Gemini Pro API
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository (or download the source code):
   ```
   git clone https://github.com/yourusername/ppt-generator-gemini-pro.git
   cd ppt-generator-gemini-pro
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud project and obtain an API key for Gemini Pro.

5. Create a `.env` file in the project root directory and add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501` (or the URL provided in the terminal).

3. Enter a topic for your presentation in the text input field.

4. Click the "Generate Presentation" button.

5. Wait for the presentation to be generated. This may take a few moments depending on the complexity of the topic.

6. Once the presentation is ready, click the download link to get your PowerPoint file.

## Customization

You can customize the appearance of the generated presentations by modifying the following constants in the `app.py` file:

- `TITLE_FONT_SIZE`: Font size for slide titles
- `SLIDE_FONT_SIZE`: Font size for slide content

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google for providing the Gemini Pro API
- Streamlit for the excellent web app framework
- python-pptx for PowerPoint file generation capabilities

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.
