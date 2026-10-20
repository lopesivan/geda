
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

    # Inclui PNGs e PDFs da mesma pasta do Makefile.
    for arquivo in sorted(makefile.parent.iterdir()):
        if not arquivo.is_file():
            continue

        extensao = arquivo.suffix.lower()
        if extensao not in {".png", ".pdf"}:
            continue

        nome = arquivo.relative_to(raiz).as_posix()
        caminho = quote(nome, safe="/")
        tipo = extensao[1:]
        itens.append((nome, caminho, tipo))

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
    padding: 0;
    text-align: left;
    font: inherit;
    color: inherit;
    background: #222;
    border: 1px solid #333;
    border-radius: 10px;
    overflow: hidden;
    transition: transform .15s, border-color .15s;
    cursor: pointer;
  }

  .card:hover {
    transform: translateY(-3px);
    border-color: #777;
  }

  .card[hidden] { display: none; }

  .card:focus-visible, .fechar:focus-visible {
    outline: 3px solid #75baff;
    outline-offset: 3px;
  }

  .preview {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: #fff;
  }

  .preview img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .preview iframe {
    display: block;
    width: 100%;
    height: 100%;
    border: 0;
    pointer-events: none;
  }

  .tipo {
    position: absolute;
    top: 8px;
    right: 8px;
    padding: 4px 8px;
    border-radius: 5px;
    background: #333;
    color: white;
    font-size: 11px;
    font-weight: bold;
  }

  .tipo.pdf { background: #b71c1c; }
  .tipo.png { background: #1565c0; }

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

  .vazio {
    text-align: center;
    color: #aaa;
    padding: 30px;
  }

  .vazio[hidden] { display: none; }

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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }

  .modal::backdrop {
    background: rgba(0, 0, 0, .8);
  }

  .modal img {
    max-width: 100%;
    max-height: calc(100dvh - 160px);
    object-fit: contain;
    border-radius: 8px;
  }

  .modal iframe {
    width: min(100%, 1100px);
    height: calc(100dvh - 170px);
    border: 0;
    border-radius: 8px;
    background: #fff;
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

  .abrir {
    color: #75baff;
    text-decoration: none;
    font-size: 14px;
  }

  .abrir:hover { text-decoration: underline; }

  .legenda {
    max-width: 100%;
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
  aria-label="Filtrar arquivos pelo nome, pasta ou extensão"
  placeholder="Filtrar por nome, pasta, PNG ou PDF…"
>

<div class="grid" id="grid">
"""

for nome, caminho, tipo in itens:
    nome_html = escape(nome, quote=True)
    caminho_html = escape(caminho, quote=True)
    filtro_html = escape(nome.lower(), quote=True)

    if tipo == "png":
        preview = f'<img src="{caminho_html}" alt="{nome_html}" loading="lazy">'
    else:
        preview = f'<iframe src="{caminho_html}#page=1&toolbar=0&navpanes=0" title="{nome_html}" loading="lazy" tabindex="-1"></iframe>'

    html += f"""  <button class="card" type="button"
    data-nome="{filtro_html}"
    data-src="{caminho_html}"
    data-tipo="{tipo}"
    title="{nome_html}">
    <div class="preview">
      {preview}
      <span class="tipo {tipo}">{tipo.upper()}</span>
    </div>
    <span class="nome">{nome_html}</span>
  </button>
"""

html += """</div>

<p class="vazio" id="vazio" hidden>Nenhum arquivo encontrado.</p>

<dialog class="modal" id="modal" aria-label="Visualização ampliada">
  <button class="fechar" id="fechar" type="button" aria-label="Fechar">&times;</button>
  <div id="modalConteudo"></div>
  <div class="legenda" id="modalLegenda"></div>
  <a class="abrir" id="abrirArquivo" href="#" target="_blank" rel="noopener">
    Abrir arquivo em nova aba ↗
  </a>
</dialog>

<script>
const filtro = document.getElementById('filtro');
const cards = [...document.querySelectorAll('.card')];
const contador = document.getElementById('contador');
const vazio = document.getElementById('vazio');
const modal = document.getElementById('modal');
const modalConteudo = document.getElementById('modalConteudo');
const modalLegenda = document.getElementById('modalLegenda');
const abrirArquivo = document.getElementById('abrirArquivo');

function atualizarFiltro() {
  const busca = filtro.value.toLowerCase().trim();
  let visiveis = 0;
  let pngs = 0;
  let pdfs = 0;

  cards.forEach(card => {
    const mostrar = card.dataset.nome.includes(busca);
    card.hidden = !mostrar;

    if (mostrar) {
      visiveis++;
      if (card.dataset.tipo === 'png') pngs++;
      if (card.dataset.tipo === 'pdf') pdfs++;
    }
  });

  contador.textContent = `${visiveis} de ${cards.length} arquivos | ${pngs} PNG | ${pdfs} PDF`;
  vazio.hidden = visiveis > 0;
}

function abrirModal(src, nome, tipo) {
  modalConteudo.replaceChildren();

  if (tipo === 'pdf') {
    const iframe = document.createElement('iframe');
    iframe.src = src;
    iframe.title = nome;
    iframe.style.width = 'min(90vw, 1100px)';
    iframe.style.height = 'calc(100dvh - 170px)';
    modalConteudo.appendChild(iframe);
  } else {
    const img = document.createElement('img');
    img.src = src;
    img.alt = nome;
    modalConteudo.appendChild(img);
  }

  modalLegenda.textContent = nome;
  abrirArquivo.href = src;
  modal.showModal();
}

function fecharModal() {
  modal.close();
}

cards.forEach(card => {
  card.addEventListener('click', () => {
    abrirModal(
      card.dataset.src,
      card.title,
      card.dataset.tipo
    );
  });
});

filtro.addEventListener('input', atualizarFiltro);
document.getElementById('fechar').addEventListener('click', fecharModal);

modal.addEventListener('click', event => {
  if (event.target === modal) fecharModal();
});

modal.addEventListener('close', () => {
  modalConteudo.replaceChildren();
});

atualizarFiltro();
</script>
</body>
</html>
"""

destino = raiz / "galeria.html"
destino.write_text(html, encoding="utf-8")

pngs = sum(tipo == "png" for _, _, tipo in itens)
pdfs = sum(tipo == "pdf" for _, _, tipo in itens)

print(f"✅ {destino} gerado com {len(itens)} arquivos")
print(f"   PNG: {pngs}")
print(f"   PDF: {pdfs}")
