
from pathlib import Path
from html import escape
from urllib.parse import quote

# Execute este script na pasta principal dos exemplos.
raiz = Path(".")
itens = []

# Procura Makefiles em todas as subpastas.
for makefile in sorted(raiz.rglob("Makefile")):
    if not makefile.is_file():
        continue

    # Inclui somente PNGs que estão na mesma pasta do Makefile.
    for imagem in sorted(makefile.parent.iterdir()):
        if not imagem.is_file() or imagem.suffix.lower() != ".png":
            continue

        nome = imagem.relative_to(raiz).as_posix()
        caminho = quote(nome, safe="/")

        # Procura o PDF correspondente ao PNG.
        pdf = imagem.with_suffix(".pdf")
        caminho_pdf = (
            quote(pdf.relative_to(raiz).as_posix(), safe="/")
            if pdf.is_file()
            else None
        )

        itens.append((nome, caminho, caminho_pdf))

html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Galeria de exemplos TikZ</title>
<style>
  * { box-sizing: border-box; }

  body {
    margin: 0;
    padding: 20px;
    font-family: system-ui, -apple-system, sans-serif;
    background: #1a1a1a;
    color: #e0e0e0;
  }

  h1 {
    text-align: center;
    font-weight: 400;
    margin-bottom: 12px;
  }

  .contador {
    text-align: center;
    color: #aaa;
    margin-bottom: 24px;
  }

  .filtro {
    display: block;
    width: 100%;
    max-width: 600px;
    margin: 0 auto 24px;
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid #444;
    background: #222;
    color: #e0e0e0;
    font-size: 16px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(260px, 100%), 1fr));
    gap: 16px;
  }

  .card {
    display: flex;
    flex-direction: column;
    text-align: left;
    background: #222;
    border: 1px solid #333;
    border-radius: 10px;
    overflow: hidden;
    transition: transform .15s, border-color .15s;
  }

  .card[hidden] {
    display: none;
  }

  .card:hover {
    transform: translateY(-3px);
    border-color: #777;
  }

  .imagem-btn {
    display: block;
    width: 100%;
    padding: 0;
    border: 0;
    background: #fff;
    cursor: pointer;
  }

  .imagem-btn img {
    display: block;
    width: 100%;
    height: 200px;
    object-fit: contain;
  }

  .imagem-btn:focus-visible,
  .link-pdf:focus-visible,
  .fechar:focus-visible {
    outline: 3px solid #75baff;
    outline-offset: -3px;
  }

  .nome {
    display: block;
    padding: 10px 12px;
    font-family: ui-monospace, monospace;
    font-size: 14px;
    color: #bbb;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  .link-pdf {
    display: block;
    margin-top: auto;
    padding: 10px 12px;
    border-top: 1px solid #383838;
    color: #75baff;
    text-decoration: none;
    font-size: 13px;
  }

  .link-pdf:hover {
    background: #303030;
    text-decoration: underline;
  }

  .sem-pdf {
    display: block;
    margin-top: auto;
    padding: 10px 12px;
    border-top: 1px solid #383838;
    color: #777;
    font-size: 13px;
  }

  .vazio {
    text-align: center;
    color: #aaa;
    padding: 30px;
  }

  .vazio[hidden] {
    display: none;
  }

  .modal {
    width: 100vw;
    max-width: 100vw;
    height: 100vh;
    max-height: 100vh;
    margin: 0;
    padding: 60px 20px;
    border: 0;
    background: rgba(0, 0, 0, .94);
    color: #fff;
  }

  .modal[open] {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal::backdrop {
    background: rgba(0, 0, 0, .8);
  }

  .modal img {
    max-width: 100%;
    max-height: calc(100dvh - 140px);
    object-fit: contain;
    border-radius: 8px;
  }

  .fechar {
    position: absolute;
    top: 12px;
    right: 20px;
    padding: 4px 12px;
    border: 0;
    background: transparent;
    color: #fff;
    font-size: 36px;
    cursor: pointer;
  }

  .legenda {
    position: absolute;
    bottom: 16px;
    left: 20px;
    right: 20px;
    max-height: 50px;
    overflow: auto;
    text-align: center;
    overflow-wrap: anywhere;
    font-family: ui-monospace, monospace;
    color: #ccc;
  }
</style>
</head>
<body>
<h1>Galeria de exemplos TikZ</h1>
<p class="contador" id="contador" aria-live="polite"></p>

<input
  class="filtro"
  id="filtro"
  type="search"
  aria-label="Filtrar imagens pelo nome ou pasta"
  placeholder="Filtrar por nome ou pasta…"
>

<div class="grid" id="grid">
"""

for nome, caminho, caminho_pdf in itens:
    nome_html = escape(nome, quote=True)
    caminho_html = escape(caminho, quote=True)
    filtro_html = escape(nome.lower(), quote=True)

    if caminho_pdf:
        pdf_html = escape(caminho_pdf, quote=True)
        link_pdf = (
            f'<a class="link-pdf" href="{pdf_html}" '
            f'target="_blank" rel="noopener">📄 Abrir PDF ↗</a>'
        )
    else:
        link_pdf = '<span class="sem-pdf">PDF não disponível</span>'

    html += f"""  <div class="card" data-nome="{filtro_html}" title="{nome_html}">
    <button class="imagem-btn" type="button" aria-label="Ampliar {nome_html}">
      <img src="{caminho_html}" alt="{nome_html}" loading="lazy">
    </button>
    <span class="nome">{nome_html}</span>
    {link_pdf}
  </div>
"""

html += """</div>

<p class="vazio" id="vazio" hidden>Nenhuma imagem encontrada.</p>

<dialog class="modal" id="modal" aria-label="Imagem ampliada">
  <button class="fechar" id="fechar" type="button" aria-label="Fechar">&times;</button>
  <img id="modalImg" alt="">
  <div class="legenda" id="modalLegenda"></div>
</dialog>

<script>
const filtro = document.getElementById('filtro');
const cards = [...document.querySelectorAll('.card')];
const contador = document.getElementById('contador');
const vazio = document.getElementById('vazio');
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modalImg');
const modalLegenda = document.getElementById('modalLegenda');

function atualizarFiltro() {
  const busca = filtro.value.toLowerCase().trim();
  let visiveis = 0;

  cards.forEach(card => {
    const mostrar = card.dataset.nome.includes(busca);
    card.hidden = !mostrar;
    if (mostrar) visiveis++;
  });

  contador.textContent = `${visiveis} de ${cards.length} imagens`;
  vazio.hidden = visiveis > 0;
}

function abrirModal(src, nome) {
  modalImg.src = src;
  modalImg.alt = nome;
  modalLegenda.textContent = nome;
  modal.showModal();
}

function fecharModal() {
  modal.close();
}

cards.forEach(card => {
  const botao = card.querySelector('.imagem-btn');

  botao.addEventListener('click', () => {
    const img = botao.querySelector('img');
    abrirModal(img.src, img.alt);
  });
});

filtro.addEventListener('input', atualizarFiltro);
document.getElementById('fechar').addEventListener('click', fecharModal);

// Fecha ao clicar no espaço ao redor da imagem.
// A tecla Escape é tratada automaticamente pelo dialog.
modal.addEventListener('click', event => {
  if (event.target === modal) fecharModal();
});

modal.addEventListener('close', () => {
  modalImg.removeAttribute('src');
});

atualizarFiltro();
</script>
</body>
</html>
"""

destino = raiz / "galeria.html"
destino.write_text(html, encoding="utf-8")

total_pdf = sum(pdf is not None for _, _, pdf in itens)

print(f"✅ {destino} gerado com {len(itens)} imagens")
print(f"📄 {total_pdf} PDFs associados")

