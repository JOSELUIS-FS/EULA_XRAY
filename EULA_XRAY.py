import os
import streamlit as st
from llama_cpp import Llama 
import PyPDF2

# 1. CONFIGURATION AND STYLING
st.set_page_config(
    page_title="EULA X-Ray | Legal Document Analyzer", 
    page_icon="⚖️", 
    layout="wide"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Botón primario mejorado y ancho */
        .stButton>button {
            border-radius: 8px;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            border: none;
            width: 100%;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #FF2B2B;
            border: 1px solid white;
        }
    </style>
""", unsafe_allow_html=True)

# 2. NVIDIA PATHS AND HEADERS
cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2\bin"
if os.path.exists(cuda_path):
    os.add_dll_directory(cuda_path)

st.title("⚖️ EULA X-Ray")
st.markdown("### *Your AI powered tool against fine print*")
st.divider()

# 3. CARGA DEL MODELO
@st.cache_resource
def load_model():
    return Llama(
        model_path="./models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
        n_ctx=8192,         
        n_threads=6,        
        n_gpu_layers=25,    
        flash_attn=True,    
        verbose=False
    )

llm = load_model()

# 4. INTERFACE IN COLUMNS (The visual magic)
# col1 (left) will be a bit narrower, col2 (right) will be wider
col1, col2 = st.columns([1, 1.5]) 

with col1:
    st.markdown("#### 1️⃣ Provide the Legal Document")
    tab1, tab2 = st.tabs(["📄 Upload PDF", "✍️ Paste Text"])

    legal_text = ""

    with tab1:
        uploaded_file = st.file_uploader("Upload a Terms of Service or Contract (PDF)", type="pdf")
        if uploaded_file is not None:
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                extracted_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
                
                st.success("✅ PDF loaded successfully!")
                with st.expander("Preview extracted text"):
                    st.text(extracted_text[:500] + "...")
                    
                legal_text = extracted_text
            except Exception as e:
                st.error(f"Error reading PDF: {e}")

    with tab2:
        pasted_text = st.text_area("Or paste the text manually...", height=200)
        if not uploaded_file and pasted_text:
            legal_text = pasted_text

    st.write("") # VISUAL SPACER
    # THE BUTTON TO TRIGGER ANALYSIS
    analyze_button = st.button("🔍 Scan for Red Flags", type="primary")

with col2:
    st.markdown("#### 2️⃣ Real-Time Analysis")
    
    # 5. INFERENCE AND DISPLAY RESULTS
    if analyze_button:
        if not legal_text:
            st.error("⚠️ Please upload a PDF or paste some legal text to scan.")
        else:
            if len(legal_text) > 18000:
                st.warning("⚠️ Document is very long. The AI will analyze the first section to prevent memory overload.")
                legal_text = legal_text[:18000]

            with st.spinner("🧠 Analyzing legal jargon and scanning for predatory clauses..."):
                system_prompt = """You are an elite legal tech analyst and privacy advocate. Your job is to read complex legal text (Terms of Service, EULAs, Privacy Policies) and translate it into brutally honest, simple English for a normal user. 

                Instructions:
                You will receive a chunk of legal text. Analyze it and generate a structured report in exactly these 3 parts:

                PART 1: The "10-Year-Old" Translation (TL;DR)
                In a maximum of two sentences, explain what this text actually means, stripped of all legal jargon.

                PART 2: 🚩 Red Flags (Hidden Traps)
                Identify the most predatory or dangerous clauses (e.g., selling user data to third parties, waiving class-action rights, giving up intellectual property, unexpected fees). Create up to 3 bullet points. If the text is completely safe, state "No major red flags detected." 
                For each point, quote a tiny snippet of the original text, then explain why it's bad.

                PART 3: 🛡️ User Rights (What you keep)
                List 1 or 2 bullet points highlighting what rights the user actually retains or guarantees the company is making.

                Critical Restriction: DO NOT include greetings or conversational filler. Return ONLY the 3 structured sections using Markdown."""
                
                response = llm.create_chat_completion(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": legal_text}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )
                
                st.success("⚡ Analysis Complete. 100% Processed Locally via GPU.")
                
                # Caja decorativa para los resultados
                with st.container():
                    st.markdown(response["choices"][0]["message"]["content"])
    else:
        # Mensaje por defecto cuando aún no se ha pulsado el botón
        st.info("👈 Upload a document and click scan to see the results here.")