import base64
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Definindo o layout em WideScreen
st.set_page_config(layout="wide")

# Definindo o layout com duas colunas
col1, col2 = st.columns([1, 1])  # Duas colunas de tamanho igual

# Logotipo na primeira coluna (alinhada à esquerda)
with col1:
    st.image("https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png", width=150)

# TAG 'Viva a Evolução' na segunda coluna (alinhada à direita)
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <img src="https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/tagline-viva-evolucao.png" style="max-width: 70%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Código HTML e CSS para a faixa no cabeçalho
html_code = """
<div style='
    background: #bfd730;
    background: linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -webkit-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -moz-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    margin: 0px 0px 0px 0px;
    width: 100%;
    position: fixed;
    padding: 10px;
    bottom: 0;
    left: 0;
    text-align: center;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 24px; 
    font-weight: bold; 
'>
   Conversor de PDF para HTML
</div>
"""

# Renderiza o HTML na aplicação Streamlit
components.html(html_code, height=50)


# Obtém a chave API da variável de ambiente
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Chave da API não encontrada. Defina GOOGLE_API_KEY no arquivo .env")
    st.stop()

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Faça upload do arquivo PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    def generate_html():
        client = genai.Client(api_key=api_key)

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(mime_type="application/pdf", data=base64.b64decode(encoded_pdf))
                ]
            )
        ]

        config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""You are an expert assistant in web accessibility and semantic HTML (WCAG 2.1 AA).
                                        **Task**: Convert a PDF into a complete, accessible HTML page. Preserve the original structure, layout, and images.
                                        Apply the following rules:
                                        1. **Semantic structure**: Use <header>, <main>, <nav>, <section>, <footer>.Use headings (<h1>–<h3>) in logical order.
                                        2. **Menu**: Create a navigation menu after the first main heading with links to each section, the link should have the title section name. Use <nav> and <ul> for the menu.
                                        3. **Responsive design**: Use viewport meta tag. Tables must scroll on small screens (overflow-x: auto). Use relative units (%, em, rem).
                                        4. **Tables**: Use <caption>, <th scope=\"col/row\">, and headers/id if needed.
                                        5. **Images**: Include all images from the PDF with <img> tags. All must have alt text.
                                        6. **Keyboard access**: All interactive elements must be usable by keyboard. Include visible focus styles.
                                        7. **Screen readers**: Use ARIA where appropriate (aria-label, aria-describedby, aria-live). All icons must have labels.
                                        8. **Links**: All links must have descriptive text. No “click here” or “read more”. Use <a> tags with href attributes.
                                        9. **Validation**: HTML must be valid (W3C). Must pass tools like WAVE, axe, Lighthouse. Target: WCAG 2.1 AA.
                                        **Output**: Return only the final HTML.""" )
            ]
        )

        output_html = ""

        with st.spinner("Gerando HTML..."):
            try:
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash-preview-04-17",
                    contents=contents,
                    config=config,
                ):
                    output_html += chunk.text
                
                # Remove o indicador de bloco HTML se presente
                if "```html" in output_html:
                    output_html = output_html.replace("```html", "")
                if "```" in output_html:
                    output_html = output_html.replace("```", "")
                
                return output_html.strip()

            except Exception as e:
                st.error(f"Erro: {e}")
                return None
            
    if uploaded_file:
        if "last_filename" not in st.session_state or st.session_state["last_filename"] != uploaded_file.name:
            st.session_state["html_result"] = None
            st.session_state["last_filename"] = uploaded_file.name

        if st.session_state.get("html_result") is None:
            html_result = generate_html()
            st.session_state["html_result"] = html_result
        else:
            html_result = st.session_state["html_result"]


    if html_result:
        file_name = os.path.splitext(uploaded_file.name)[0] + ".html"
        st.success("Conversão concluída!")
        st.download_button(
            label="Baixar arquivo HTML",
            data=html_result,
            file_name=file_name,
            mime="text/html",
        )

else:
    st.info("Faça upload de um arquivo PDF para iniciar.")
