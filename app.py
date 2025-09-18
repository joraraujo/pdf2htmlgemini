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

st.markdown("""
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
""",unsafe_allow_html=True
)




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
                    model="gemini-2.5-flash",
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
        # Adiciona o script VLibras ao HTML gerado
        vlibras_code = """
    <script>
window.interdeal = {
    get sitekey (){ return "ca727b42941b46b193becfaab4950955"} ,
    get domains(){
        return {
            "js": "https://cdn.equalweb.com/",
            "acc": "https://access.equalweb.com/"
        }
    },
    "Position": "left",
    "Menulang": "PT",
    "draggable": true,
    "btnStyle": {
        "vPosition": [
            "80%",
            "20"
        ],
        "margin": [
            "0",
            "0"
        ],
        "scale": [
            "0.5",
            "0.5"
        ],
        "color": {
            "main": "#0080b0",
            "second": "#ffffff"
        },
        "icon": {
            "outline": true,
            "outlineColor": "#ffffff",
            "type":  1 ,
            "shape": "circle"
        }
    },
                        "showTooltip": true,
      
};
(function(doc, head, body){
    var coreCall             = doc.createElement('script');
    coreCall.src             = interdeal.domains.js + 'core/5.1.13/accessibility.js';
    coreCall.defer           = true;
    coreCall.integrity       = 'sha512-70/AbMe6C9H3r5hjsQleJEY4y5l9ykt4WYSgyZj/WjpY/ord/26LWfva163b9W+GwWkfwbP0iLT+h6KRl+LoXA==';
    coreCall.crossOrigin     = 'anonymous';
    coreCall.setAttribute('data-cfasync', true );
    body? body.appendChild(coreCall) : head.appendChild(coreCall);
})(document, document.head, document.body);
</script>
<div vw class="enabled" style="display:none;" id="vlibras">
    <div vw-access-button class="active" id="vlibrasclick"></div>
    <div vw-plugin-wrapper>
        <div class="vw-plugin-top-wrapper"></div>
    </div>
</div>
<script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
<script>
    new window.VLibras.Widget('https://vlibras.gov.br/app');
</script>
<script>
    window.addEventListener("load", function () {
        var INDLibrasCount = 0;
        var INDLibrasLoad = setInterval(() => {
            try {
                if (interdeal.menu.querySelector("#btvlibras") == null && INDLibrasCount == 0) {
                    INDLibrasCount = 1; // para o counter
                    var b = document.createElement('button');
                    b.setAttribute("id", "btvlibras");
                    b.setAttribute("data-indopt", "vlibrasreader");
                    b.setAttribute("role", "checkbox");
                    b.setAttribute("aria-labelledby", "vlibrasreader_label_1 vlibrasreader_label_2");
                    b.setAttribute("tabindex", "0");
                    b.setAttribute("aria-checked", "false");
                    b.innerHTML = '<svg version="1.2" baseProfile="tiny" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="126.04px" height="122.666px" viewBox="0 0 126.04 122.666" xml:space="preserve"> <path d="M108.875,61.237c0.002-10.126-4.098-19.334-10.711-25.996c-1.361-1.374-3.58-1.383-4.951-0.021c-1.372,1.361-1.381,3.577-0.02,4.951v-0.002c5.371,5.421,8.681,12.847,8.681,21.068c0.003,0.016,0,0.074,0.003,0.17c-0.032,8.219-3.401,15.663-8.842,21.071c-1.372,1.361-1.379,3.577-0.018,4.949c0.686,0.688,1.585,1.034,2.484,1.034c0.893,0,1.784-0.339,2.467-1.018c6.695-6.646,10.873-15.881,10.906-26.063V61.237z M109.015,19.872c-1.364-1.372-3.579-1.381-4.952-0.019c-1.369,1.363-1.378,3.579-0.016,4.951v-0.002c9.273,9.353,14.992,22.19,14.992,36.389c0,0.049,0,0.134,0.002,0.253c-0.058,14.206-5.878,27.071-15.267,36.398c-1.372,1.362-1.381,3.58-0.017,4.952c0.684,0.689,1.584,1.034,2.484,1.034c0.891,0,1.781-0.338,2.465-1.016c10.648-10.569,17.273-25.227,17.332-41.405v-0.217C126.042,45.092,119.536,30.468,109.015,19.872z M81.307,0.362c-1.189-0.59-2.621-0.451-3.677,0.355L35.889,32.576H3.502c-0.924,0-1.824,0.372-2.476,1.025C0.375,34.253,0,35.153,0,36.075v50.516c0,0.922,0.375,1.822,1.026,2.476c0.651,0.651,1.554,1.024,2.476,1.024H35.89l41.74,31.858c0.622,0.474,1.372,0.717,2.128,0.717c0.527,0,1.059-0.119,1.549-0.361c1.189-0.59,1.947-1.81,1.947-3.136V3.5C83.254,2.17,82.497,0.949,81.307,0.362z M76.255,112.092L39.196,83.809c-0.606-0.464-1.36-0.718-2.122-0.718H7V39.575h30.074c0.762,0,1.516-0.255,2.122-0.717l37.059-28.286V112.092z"></path> </svg> <span id="vlibras_label_1" aria-hidden="true" class="INDmenuBtn-text">V Libras</span> <span id="vlibras_label_2" aria-hidden="true" class="INDmenuBtn-desc">Aciona o V Libras</span>';
                    b.addEventListener("click", function () {
                        document.getElementById("vlibras").style.display = "block";
                        document.getElementById("vlibrasclick").click();
                    });
                    var menu = interdeal.menu.querySelector('#INDmenuBtnzWrap');
                    menu.append(b);
                    clearInterval(INDLibrasLoad);
                }
            } catch (error) {
                INDLibrasCount = 0;
            }
        }, 1000);
    })
</script>
        """
        
        # Insere o código VLibras antes do fechamento do body
        if "</body>" in html_result:
            html_result = html_result.replace("</body>", vlibras_code + "\n</body>")
        else:
            html_result += vlibras_code

        st.download_button(
            label="Baixar arquivo HTML",
            data=html_result,
            file_name=file_name,
            mime="text/html",
        )

else:
    st.info("Faça upload de um arquivo PDF para iniciar.")

