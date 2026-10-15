# Ferramentas gEDA, gEDA/gaf e Lepton EDA

Guia de referência para captura de esquemáticos, bibliotecas
de símbolos, geração de netlists, documentação e
integração com projetos de placas de circuito impresso (PCB).

> **Compatibilidade:** gEDA/gaf, gEDA PCB e Lepton EDA são
projetos relacionados, mas não são um único programa. Os
executáveis e as opções dependem da distribuição e da
versão. Consulte sempre `command -v NOME` e `NOME --help`
antes de automatizar comandos.

## 1. Visão geral do fluxo

```text
Bibliotecas de símbolos (.sym)
            │
            ▼
Editor de esquemáticos ───► Verificação de símbolos
     (.sch)                         │
       │                            │
       ├──► Atributos (refdes, value, footprint)
       │
       ├──► Exportação (PS, PDF, SVG, imagens)
       │
       └──► Netlist ──┬──► SPICE (simulação)
                      ├──► BOM (lista de materiais)
                      └──► PCB (layout, fabricação)
```

Uma **netlist** representa conexões elétricas entre
terminais. Um **footprint** descreve a geometria física do
componente na placa. Um símbolo esquemático não substitui
o footprint: ambos precisam de mapeamento correto de pinos.

## 2. Captura de esquemáticos e ferramentas gerais

### `gschem`

Editor gráfico tradicional do gEDA/gaf para arquivos
`.sch`. Permite inserir símbolos, desenhar nets e barramentos,
editar atributos e organizar projetos em múltiplas folhas.

```bash
gschem circuito.sch
```

**Verificações recomendadas:** conferir junções elétricas,
nomes de nets, alimentação, `refdes`, `value`, `device`,
`footprint` e a correspondência entre números de pinos
do símbolo e pads do footprint. A aparência de dois fios
cruzados não garante, por si só, conexão elétrica.

**No Lepton EDA:** o editor equivalente é geralmente `lepton-schematic`.

### `gaf`

Interface de linha de comando do **gEDA/gaf** para tarefas
disponibilizadas pela versão instalada, como exportação
e operações relacionadas ao projeto.

```bash
gaf --help
gaf export --help
```

Exemplo de exportação (confirme as opções na versão local):

```bash
gaf export -o circuito.pdf circuito.sch
```

**Atenção:** não confundir `gaf` com o comando do Lepton
EDA, `lepton-cli`, cuja sintaxe é própria.

### `gschlas` — identificação pendente

O nome **não corresponde a um utilitário padrão amplamente
documentado do gEDA/gaf**. Pode ser um script local, um pacote
de terceiros ou um nome incorreto. Não se deve atribuir a
ele uma sintaxe de exportação sem identificar sua origem.

Para exportação em lote, investigue `gaf export`, `gsch2ps`
(legado) ou `lepton-cli export`, conforme o ambiente.

```bash
command -v gschlas || echo 'gschlas não instalado'
command -v gsch2ps
```

### `garchive`

Ferramenta histórica de arquivamento de projetos gEDA. Seu
propósito é reunir esquemáticos e dependências relevantes,
incluindo símbolos personalizados, para facilitar
transferência e preservação.

```bash
garchive --help
```

**Boa prática:** inspecionar o arquivo produzido e testar
a abertura em outra máquina. Arquivamento não garante
automaticamente que bibliotecas externas, footprints, modelos
SPICE e configurações particulares estejam incluídos.

## 3. Netlists e integração com PCB

### `gnetlist`

Converte esquemáticos em representações de conectividade
para ferramentas posteriores. Os *backends* disponíveis
dependem da instalação; historicamente incluem saídas para
SPICE, BOM e fluxos PCB.

```bash
gnetlist --help
gnetlist -g spice-sdb -o circuito.cir circuito.sch
```

O backend `spice-sdb` é histórico: confirme sua presença
antes de utilizá-lo. O arquivo `.cir` deve ser revisado,
especialmente quanto a modelos, fontes, subcircuitos e ordem
dos pinos.

**No Lepton EDA:** procure `lepton-netlist` e confira `lepton-netlist --help`.

### `gnetlist-legacy`

Nome encontrado em alguns ambientes de compatibilidade,
mas **não é um executável universal** das distribuições
gEDA/Lepton. Quando disponível, pode preservar comportamentos
antigos; confirme o pacote de origem e os backends efetivamente
suportados.

```bash
command -v gnetlist-legacy
```

### `gsch2pcb`

Ferramenta histórica de transição entre esquemáticos gEDA
e o programa **PCB** clássico. Ajuda a produzir arquivos de
conectividade e alterações de componentes para sincronizar
o layout.

```bash
gsch2pcb --help
```

Não confunda o programa **PCB** clássico com **pcb-rnd** ou
**KiCad PCB Editor**: os formatos e as rotinas de importação
não são automaticamente intercambiáveis. Revise footprints
e pinagens antes de aplicar mudanças ao layout.

### `pcb_backannotate`

Utilitário associado a fluxos históricos de
*back-annotation*: propagar informações do layout para o
esquemático, como alterações de numeração ou trocas de
portas, quando suportadas.

```bash
pcb_backannotate --help
```

**Cuidado:** o nome, a disponibilidade e o formato de entrada
variam. Faça backup ou commit antes de executar; revise
o resultado com `git diff` e gere novamente a netlist para
conferir consistência.

## 4. Atributos e numeração

### `gattrib`

Editor gráfico em formato de tabela para atributos dos
componentes do esquemático. Útil para revisar vários
`refdes`, valores e footprints sem abrir cada símbolo
individualmente.

```bash
gattrib circuito.sch
```

Atributos comuns:

| Atributo | Função | Exemplo |
|---|---|---|
| `refdes` | Identificador único no projeto | `R12`, `U3`, `J1` |
| `value` | Valor ou designação | `10k`, `100nF` |
| `device` | Tipo lógico do componente | `RESISTOR` |
| `footprint` | Associação com encapsulamento físico | depende da biblioteca PCB |
| `net` | Associação explícita de rede em contextos específicos | depende do símbolo |
| `slot` | Unidade selecionada de componente multipartes | `1`, `2` |

**Atenção:** editar atributos não valida automaticamente
pinagem, existência do footprint ou disponibilidade comercial
do componente.

### `refdes_renum`

Script histórico para renumerar designadores de referência,
com regras que podem considerar a posição dos símbolos
nas folhas.

```bash
refdes_renum --help
```

Execute antes de consolidar BOM e layout, pois
renumerações tardias podem dificultar a comparação entre
revisões. Confira componentes multipartes e referências
previamente reservadas.

### `grenum`

Nome associado a utilitários de renumeração em determinados
pacotes ou scripts. **Não presuma que seja sinônimo direto de
`refdes_renum`**: identifique sua origem e confira a sintaxe
e os critérios de ordenação.

```bash
command -v grenum
grenum --help
```

## 5. Símbolos e bibliotecas

### `tragesym`

Gerador de símbolos a partir de descrições textuais
estruturadas. É útil para componentes com muitos pinos,
pois reduz trabalho manual e ajuda a padronizar atributos.

```bash
tragesym --help
```

Fluxo recomendado: obter pinagem no datasheet → preparar a
descrição no formato aceito pela versão → gerar `.sym`
→ abrir no editor → executar `gsymcheck` → conferir
manualmente pinos e tipos elétricos.

### `gsymcheck`

Verificador de símbolos `.sym`. Ajuda a detectar atributos
ausentes ou inconsistentes e problemas estruturais dos
símbolos.

```bash
gsymcheck componente.sym
```

A aprovação do verificador **não comprova** que a pinagem
está correta em relação ao datasheet. Confira números de
pinos, nomes, slots, atributos e o mapeamento para o footprint.

### `gsymfix`

Nome associado a scripts de manutenção/conversão de
símbolos, mas **não deve ser tratado como ferramenta
padrão garantida**. Determine a versão e a origem antes de
utilizá-lo para reescrever bibliotecas.

```bash
command -v gsymfix
gsymfix --help
```

Para bibliotecas sob controle de versão, faça a conversão
em um branch separado e inspecione as alterações antes
de incorporar.

## 6. Comparação, montagem e APIs

### `schdiff`

Ferramenta para comparação de esquemáticos entre
versões. Dependendo da implementação, pode gerar ou
apresentar diferenças visuais, úteis em revisões de
engenharia.

```bash
schdiff --help
```

Para revisões confiáveis, combine comparação visual
com `git diff` dos arquivos `.sch` e, quando possível,
comparação de netlists. Mudanças de posição gráfica
nem sempre representam mudanças elétricas.

### `gxyrs`

Utilitário relacionado ao tratamento de coordenadas **XYRS**
(posição X/Y, rotação e lado ou informação de montagem,
conforme o formato). Pode apoiar a preparação de dados para
montagem SMT.

```bash
gxyrs --help
```

Confirme as unidades (mm/mil), origem da placa, eixo Y, sentido
positivo de rotação, lado superior/inferior e convenção
do fabricante. Arquivos *pick-and-place* incorretos podem
causar montagem invertida.

### `xorn`

Conjunto de bibliotecas e APIs para manipulação programática
de objetos esquemáticos no ecossistema gEDA, com componentes
em C e interfaces Python em determinadas versões. **Não é
necessariamente um comando de terminal chamado `xorn`**.

Aplicações possíveis: ler estruturas, transformar objetos,
automatizar verificações e construir ferramentas de
análise. Verifique os módulos efetivamente instalados e
suas APIs, que variam entre releases.

## 7. Lepton EDA: equivalências importantes

O Lepton EDA deriva historicamente do gEDA/gaf e mantém
conceitos e formatos relacionados, mas não é seguro trocar
executáveis sem consultar a documentação da versão.

| Tarefa | gEDA/gaf tradicional | Lepton EDA |
|---|---|---|
| Editar esquemáticos | `gschem` | `lepton-schematic` |
| Gerar netlists | `gnetlist` | `lepton-netlist` |
| Verificar símbolos | `gsymcheck` | `lepton-symcheck` |
| Editar atributos | `gattrib` | `lepton-attrib` (quando disponível) |
| Exportar | `gaf export` | `lepton-cli export` |

Consulte a ajuda de cada ferramenta para conferir opções, subcomandos e backends.

## 8. Exemplo de organização de projeto

```text
amplificador/
├── README.md
├── schematics/
│   └── amplificador.sch
├── symbols/
│   └── componente-customizado.sym
├── footprints/
├── simulation/
├── manufacturing/
│   ├── gerber/
│   └── assembly/
├── bom/
└── docs/
```

Sugestão de sequência de trabalho:

1. Criar ou validar símbolos e conferir o datasheet.
2. Capturar o esquemático e revisar conexões e atributos.
3. Renumerar `refdes` antes de estabelecer referências externas.
4. Gerar a netlist apropriada ao simulador ou editor de PCB.
5. Conferir o mapeamento entre pinos, pads e footprints.
6. Criar o layout, verificar regras elétricas e geométricas
com as ferramentas apropriadas.
7. Gerar Gerbers, arquivos de furação, BOM e coordenadas de montagem.
8. Arquivar esquemáticos, bibliotecas, configurações,
resultados e versões de ferramentas.

## 9. Diagnóstico de instalação no Linux

```bash
for cmd in gschem gaf gschlas garchive gnetlist gnetlist-legacy \
           gsch2pcb pcb_backannotate gattrib refdes_renum grenum \
           tragesym gsymcheck gsymfix schdiff gxyrs xorn \
           lepton-schematic lepton-netlist lepton-symcheck \
           lepton-attrib lepton-cli; do
    if path=$(command -v "$cmd" 2>/dev/null); then
        printf '[OK]      %-20s %s\n' "$cmd" "$path"
    else
        printf '[AUSENTE] %s\n' "$cmd"
    fi
done
```

Para descobrir o pacote proprietário de um executável
instalado no Ubuntu/Debian:

```bash
dpkg -S "$(command -v gschem)"
```

Se um comando não estiver instalado, não conclua
automaticamente que ele foi removido do projeto: pode pertencer
a um pacote opcional, ter sido renomeado ou não existir na
distribuição utilizada.

## 10. Glossário

- **ERC (*Electrical Rules Check*):** análise de consistência
elétrica; não substitui simulação nem revisão humana.
- **DRC (*Design Rules Check*):** verificação de regras
geométricas e de fabricação do PCB.
- **BOM (*Bill of Materials*):** lista de componentes,
quantidades e informações de compra.
- **Netlist:** descrição da conectividade entre terminais.
- **Refdes:** identificador de referência, como `R1` e `U2`.
- **Footprint:** representação física de pads, furos e geometria de montagem.
- **Back-annotation:** propagação de alterações do layout
para o esquemático.
- **Pick-and-place:** dados de posicionamento de componentes
para montagem automatizada.

## 11. Referências

- [gEDA Project](http://www.geda-project.org/)
- [Lepton EDA](https://github.com/lepton-eda/lepton-eda)
- [gEDA/gaf](https://github.com/geda-project/geda-gaf)
- [pcb-rnd](https://www.repo.hu/projects/pcb-rnd/)

> **Nota de precisão:** os nomes e usos históricos
foram separados de funcionalidades cuja presença depende
do pacote. Em particular, `gschlas`, `gnetlist-legacy`,
`grenum`, `gsymfix`, `gxyrs` e `xorn` devem ser identificados
na instalação concreta antes de serem incorporados a scripts
de produção.
