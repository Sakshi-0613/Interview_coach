# 🤖 AI Interview Coach

This is a mock interview coaching tool built using **Streamlit** and **Gemini 1.5 Pro** from Google's Generative AI API. It asks you domain-specific interview questions, analyzes your answers, and provides detailed feedback.

## 🧠 Features

- Domain selection: Data Science, Web Dev, HR, Marketing, and Software Engineering
- Answer feedback with score, strengths, improvement suggestions, and revised version
- Final PDF report download with all answers and AI feedback

## 📸 Screenshots

### 1. Home Page  
<img src="assets/S_1.png" width="600"/>

### 2. Domain Selection  
<img src="assets/S_2.png" width="600"/>

### 3. Answer Submission  
<img src="assets/S_3.png" width="600"/>

### 4. Feedback Received  
<img src="assets/S_4.png" width="600"/>
<img src="assets/S_5.png" width="600"/>


## 🛠 Setup Instructions

1. Clone the repo and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Get your API key from [Google AI Studio](https://g.co/kgs/n9XSs2x) by deploying **Gemini 1.5 Pro**.

3. Create a `.env` file:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

4. Run the app:
    ```bash
    streamlit run task1.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.