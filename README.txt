# ⚖️ EULA X-Ray

> Your local AI-powered tool against fine print.

##  About the Project
EULA X-Ray is an application designed to analyze Terms of Service (ToS), End User License Agreements (EULAs), and Privacy Policies. It automatically extracts text from PDF documents and utilizes a local language model to break down legal jargon, identify predatory clauses (Red Flags), and summarize actual user rights in seconds.

##  Tech Stack
* **Frontend:** Streamlit (with optimized two-column layout).
* **AI Engine:** `llama-cpp-python` with native **CUDA 12** (`cu122`) support.
* **Model:** Meta-Llama-3-8B-Instruct (Optimized in GGUF format with *Flash Attention*).
* **PDF Processing:** PyPDF2.

##  Requirements & Local Installation
To replicate the environment with GPU hardware acceleration (NVIDIA):

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/eula-xray.git](https://github.com/your-username/eula-xray.git)
   cd eula-xray