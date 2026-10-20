# Explicação Matemática: Método das Cascas Cilíndricas (Cálculo de Volume)

Vou explicar com cuidado conceitual e matemático, passo a passo, justificando a fórmula do $dV$ usada no método das cascas no seu código.

### Observação importante (conceitual):
No seu exemplo do cone, o método correto é o método das **cascas cilíndricas**, não esféricas.
* “Cascas esféricas” são usadas quando o sólido é naturalmente descrito por esferas (ex.: uma esfera carregada).
* Aqui, como a variável é $\rho$ (raio no plano), estamos lidando com cascas cilíndricas.

---

### 1. Ideia geométrica do método das cascas cilíndricas
Em vez de decompor o cone em discos horizontais, nós o decompomos em cascas verticais:
* Cada casca é um cilindro fino e oco;
* **Raio:** $\rho$
* **Espessura:** $d\rho$
* **Altura:** depende de $\rho$

**Visualmente:** É como “descascar” o cone em tubos concêntricos, do eixo até a borda.

### 2. Volume elementar de uma casca cilíndrica
O volume de uma casca cilíndrica fina é:

$$\boxed{dV = (\text{área lateral}) \times (\text{espessura})}$$

A área lateral de um cilindro de raio $\rho$ e altura $h(\rho)$ é:

$$A_{\text{lateral}} = 2\pi\rho \cdot h(\rho)$$

Logo:

$$\boxed{dV = 2\pi\rho \cdot h(\rho) \, d\rho}$$

### 3. Determinação da altura da casca $h(\rho)$
O cone tem:
* **Raio da base:** $r$
* **Altura total:** $h$

A altura do cone decresce linearmente com o raio $\rho$. Isso vem de semelhança de triângulos:
* Quando $\rho = 0$, a altura é $h$.
* Quando $\rho = r$, a altura é $0$.

Relação geométrica:
$$\frac{h(\rho)}{h} = 1 - \frac{\rho}{r}$$

Portanto:
$$\boxed{h(\rho) = h\left(1 - \frac{\rho}{r}\right)}$$
ou, expandindo:
$$\boxed{h(\rho) = h - \frac{h}{r}\rho}$$

### 4. Substituindo na expressão de $dV$
Voltamos à fórmula geral da casca:
$$dV = 2\pi\rho \cdot h(\rho) \, d\rho$$

Substituindo $h(\rho)$:
$$dV = 2\pi\rho \left(h - \frac{h}{r}\rho\right) d\rho$$

E chegamos exatamente à fórmula que você usou:
$$\boxed{dV = 2\pi\rho \left(h - \frac{h}{r}\rho\right) d\rho}$$

### 5. Por que os limites são $0 \le \rho \le r$
Como estamos varrendo as cascas:
* Começamos no eixo do cone: $\rho = 0$
* Terminamos na borda da base: $\rho = r$

Logo, o volume total é:
$$V = \int_0^r 2\pi\rho\left(h-\frac{h}{r}\rho\right)d\rho$$

### 6. Resultado final (consistência física)
Ao resolver a integral, obtemos:
$$V = \frac{1}{3}\pi r^2 h$$

Isso confirma a coerência geométrica e a consistência com o volume conhecido do cone.

### 7. Resumo conceitual
1.  O método das cascas cilíndricas decompõe o sólido em tubos finos.
2.  Cada tubo contribui com $dV = (\text{perímetro}) \times (\text{altura}) \times (\text{espessura})$.
3.  No cone, a altura varia linearmente com o raio.


## Dedução Vetorial: Cascas Cilíndricas no Cone via Jacobiano

A seguir, apresentamos uma dedução puramente vetorial para o método das cascas cilíndricas no cone, justificando o elemento de volume $dV$ através de parametrização e do produto vetorial (determinante Jacobiano).

### 1. Parametrização Vetorial do Cone
Considere o cone com vértice no eixo $z$, altura $h$, base no plano $z=0$ com raio $r$, e vértice em $z=h$.

No método das cascas, fixamos o raio cilíndrico $\rho \in [0,r]$ e varremos o ângulo $\varphi \in [0,2\pi)$ e a coordenada vertical $z$ ao longo da geratriz. Pela geometria do cone, a relação entre o raio e a altura é:

$$\rho(z) = r\Bigl(1 - \frac{z}{h}\Bigr) \iff z = h\Bigl(1 - \frac{\rho}{r}\Bigr)$$

Logo, para uma casca de raio $\rho$, a altura máxima $z_{\max}$ atingida é:
$$z_{\max}(\rho) = h\Bigl(1 - \frac{\rho}{r}\Bigr)$$

Parametrizamos o volume do sólido $\mathbf{X}(\rho, \varphi, z)$ como:
$$\mathbf{X}(\rho,\varphi,z) = \begin{pmatrix} \rho \cos \varphi \\ \rho \sin \varphi \\ z \end{pmatrix}$$

Onde os domínios são: $0 \le \rho \le r$, $0 \le \varphi < 2\pi$, $0 \le z \le z_{\max}(\rho)$.

### 2. Elemento de Volume via Jacobiano Vetorial
O elemento de volume em uma parametrização $\mathbf{X}(u,v,w)$ é dado pelo módulo do determinante da matriz Jacobiana:

$$dV = \left| \det \left[ \frac{\partial\mathbf{X}}{\partial \rho}, \frac{\partial\mathbf{X}}{\partial \varphi}, \frac{\partial\mathbf{X}}{\partial z} \right] \right| \, d\rho \, d\varphi \, dz$$

Calculamos os vetores tangentes:
$$\mathbf{X}_\rho = \begin{pmatrix} \cos\varphi \\ \sin\varphi \\ 0 \end{pmatrix}, \quad \mathbf{X}_\varphi = \begin{pmatrix} -\rho\sin\varphi \\ \rho\cos\varphi \\ 0 \end{pmatrix}, \quad \mathbf{X}_z = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$

O Jacobiano pode ser obtido pelo produto misto:
$$| \det[\mathbf{X}_\rho, \mathbf{X}_\varphi, \mathbf{X}_z] | = |(\mathbf{X}_\rho \times \mathbf{X}_\varphi) \cdot \mathbf{X}_z|$$

Primeiro, o produto vetorial:
$$\mathbf{X}_\rho \times \mathbf{X}_\varphi = \begin{pmatrix} 0 \\ 0 \\ \rho(\cos^2\varphi + \sin^2\varphi) \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ \rho \end{pmatrix}$$

Então o produto escalar com $\mathbf{X}_z$:
$$\begin{pmatrix} 0 \\ 0 \\ \rho \end{pmatrix} \cdot \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix} = \rho$$

Portanto, o elemento de volume diferencial é:
$$\boxed{dV = \rho \, d\rho \, d\varphi \, dz}$$

### 3. "Casca Cilíndrica" como Integração Parcial
Para um $\rho$ fixo, a casca corresponde a integrar o elemento $dV$ nas variáveis $\varphi$ e $z$:

$$dV_{\text{casca}}(\rho) = \left( \int_{0}^{2\pi} \int_{0}^{z_{\max}(\rho)} \rho \, dz \, d\varphi \right) d\rho$$

1. **Integrando em $z$:** $\int_{0}^{z_{\max}(\rho)} \rho \, dz = \rho \cdot z_{\max}(\rho)$
2. **Integrando em $\varphi$:** $\int_{0}^{2\pi} \rho \cdot z_{\max}(\rho) \, d\varphi = 2\pi\rho \cdot z_{\max}(\rho)$

Substituindo $z_{\max}(\rho) = h - \frac{h}{r}\rho$, obtemos a fórmula final do código:
$$\boxed{dV_{\text{casca}}(\rho) = 2\pi\rho \left( h - \frac{h}{r}\rho \right) d\rho}$$

### 4. Volume Total
$$V = \int_{0}^{r} 2\pi\rho \left( h - \frac{h}{r}\rho \right) d\rho = 2\pi \left[ \frac{h\rho^2}{2} - \frac{h\rho^3}{3r} \right]_{0}^{r} = \frac{1}{3}\pi r^2 h$$

---
**O que foi "puramente vetorial" aqui:**
* A **parametrização** $\mathbf{X}(\rho, \varphi, z)$ do sólido.
* O **Jacobiano** via produto misto de vetores tangentes.
* A **fórmula da casca** como consequência natural da integração parcial do volume diferencial.
