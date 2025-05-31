import base64
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import os

# Carrega variáveis do .env
load_dotenv()

st.title("Conversor de PDF para HTML")

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
                                        1. **Semantic structure**: Use <header>, <main>, <nav>, <section>, <footer>. Add a “Skip to main content” link. Use headings (<h1>–<h3>) in logical order.
                                        2. **Contrast**: Ensure text contrast is ≥ 4.5:1 (or 3:1 for large/bold text). Do not use color alone to convey meaning.
                                        3. **Responsive design**: Use viewport meta tag. Tables must scroll on small screens (overflow-x: auto). Use relative units (%, em, rem).
                                        4. **Tables**: Use <caption>, <th scope=\"col/row\">, and headers/id if needed.
                                        5. **Images**: Include all images from the PDF with <img> tags. All must have alt text. Use alt=\"\" if decorative.
                                        6. **Keyboard access**: All interactive elements must be usable by keyboard. Include visible focus styles.
                                        7. **Screen readers**: Use ARIA where appropriate (aria-label, aria-describedby, aria-live). All icons must have labels.
                                        8. **Forms**: Associate <label> with inputs. Use aria-invalid and show visible error messages. Provide clear feedback.
                                        9. **Validation**: HTML must be valid (W3C). Must pass tools like WAVE, axe, Lighthouse. Target: WCAG 2.1 AA.
                                        **Output**: Return only the final HTML.""" )
            ]
        )

        output_html = ""
        my_bar = st.progress(0, text="Gerando HTML...")

        for i in range(10):
            time.sleep(0.05)
            my_bar.progress(i + 1, text="Preparando geração do HTML...")
        
        try:
            chunk_count = 0
            max_chunks_estimate = 40  # número estimado de chunks (ajustável)
            
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash-preview-04-17",
                contents=contents,
                config=config,
            ):
                output_html += chunk.text
                chunk_count += 1
                # Atualiza progresso com limite de 100%
                progress = min(int((chunk_count / max_chunks_estimate) * 100), 100)
                my_bar.progress(progress, text="Gerando HTML...")

            # Limpa código extra
            output_html = output_html.replace("```html", "").replace("```", "")

            return output_html.strip()

        except Exception as e:
            st.error(f"Erro: {e}")
            return None

        finally:
            my_bar.empty()

            
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
