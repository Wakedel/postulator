# Postulator: Your AI-Powered Application Letter & Interview Prep Assistant

Postulator is a powerful tool designed to help individuals, especially those from economically disadvantaged backgrounds, create compelling application letters and prepare for job interviews. Inspired by the deeplearning.ai CrewAI mini-lecture, Postulator goes beyond the basics by focusing on crafting effective, culturally sensitive application materials.

## Features

-   **AI-Powered Application Letter Generation:**
    -   Creates professional, tailored application letters using your CV and provided examples.
    -   Leverages AI to match your skills and experiences with job requirements.
    -   Generates LaTeX output for high-quality, printable letters.
-   **Customizable Letter Templates:**
    -   Easily modify the LaTeX template to suit your specific needs.
-   **Tailored Resume Creation:**
    -   Adapts your CV to align with specific job postings, highlighting relevant skills and experiences.
-   **Interview Preparation Materials:**
    -   Generates potential interview questions and answers based on the job posting and your background.
-   **Culturally Sensitive Design:**
    -   Aims to bridge the cultural capital gap, enabling individuals from diverse backgrounds to compete effectively in the job market.
-   **Easy to Use:**
    -   Simple configuration and execution, making it accessible to users with varying technical skills.

## Getting Started

### Prerequisites

-   Python 3.10 to 3.12
-   Google Gemini API Key
-   Google Serper API Key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd postulator
    ```

2.  **Install:**

    -   **Install crewai using pip:**

        ```bash
        pip install crewai
        ```

    -   **Build the environment the code will be run in:**
        Go to the root directory of the project and run the following command.
        ```bash
        crewai install
        ```

3.  **Configure API keys:**

    Amend the `.env` file in the root directory to add your Google Gemini and Google Serper API keys:
        ```
        GOOGLE_API_KEY=your_gemini_api_key
        SERPER_API_KEY=your_serper_api_key
        ```

### Usage

1.  **Prepare your CV:**
    -   Write your CV in `input/resume_long.md`.

2.  **Provide an example application letter:**
    -   Amend `input/example_motivation_letter.txt` with an example letter you want the system to mimic.

3.  **Configure `config.json`:**
    -   Set the `job_posting` URLs, `language`, and `personal_writeup` in `config.json`.
    -   Example `config.json`:

        ```json
        {
          "job_posting": "urls: https://www.example-job-board.com/job/software-engineer ; https://www.example-company.com/about-us",
          "language": "English",
          "personal_writeup": "I am a highly motivated software engineer with a passion for building scalable and efficient systems. I have experience in Python, Java, and cloud technologies. I am particularly interested in this role because it aligns with my career goals and allows me to contribute to innovative projects. I have overcome a difficult economic background through hard work, and I am highly motivated to succeed. I'm also very interested in the company's commitment to social responsibility."
        }
        ```

    -   **Explanation of the `config.json` fields:**

        * **`job_posting`:**
            * This is an array of URLs that provide information about the job you are applying for.
            * Include the job posting URL itself, as well as any relevant company information or other resources.
            * The AI will use these URLs to understand the job requirements and company culture.
        * **`language`:**
            * Specifies the language in which the application letter and other outputs should be generated.
            * Examples: "English", "French", "Spanish", etc.
        * **`personal_writeup`:**
            * This is a free-form text field where you can provide additional information about yourself.
            * Include details about your motivation, relevant experiences, or anything else that you want the AI to consider when generating the application letter.
            * This is a perfect place to add information about any hardships you have overcome, and how that has shaped you.
            * It is also a perfect place to add information about why you want to work for the company, and why this specific role is appealing.
            * Providing a well written personal_writeup will drastically improve the quality of the application letter.

4.  **Run Postulator:**

    ```bash
    crewai run
    ```

5.  **View the outputs:**
    -   Find the generated application letter (`motivation_letter.tex`) ---be aware that it may not fit on a single page---, tailored resume (`tailored_resume.md`), and interview materials (`interview_materials.md`) in the `output` directory.
    -   Compile the motivation_letter.tex file with a Latex compiler.

## Customization

-   **Modify the LaTeX template:**
    -   Edit `src/postulator/tools/custom_tools.py` to customize the application letter template.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## Future Improvement: More Comprehensive Job Information with PDF Support

To provide even more accurate and detailed application letters, we're adding the capability to process PDF documents as job posting sources. Simply place your PDF job descriptions in the `input` directory, and Postulator will incorporate them into its analysis.

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for details.
