Vou explicar **exatamente quais funções estão sendo plotadas** e como elas aparecem no gráfico, relacionando isso diretamente ao código.

---

## 1. Vetores criados no código

Dentro do `for`, a cada iteração `i`, você constrói três vetores:

```cpp
x.push_back(i * i);
y.push_back(sin(2 * M_PI * i / 360.0));
z.push_back(log(i));
```

Ou seja:

* **x** recebe valores do tipo
  [
  x_i = i^2
  ]

* **y** recebe valores do tipo
  [
  y_i = \sin!\left(\frac{2\pi}{360}, i\right)
  ]

* **z** recebe valores do tipo
  [
  z_i = \log(i)
  ]

---

## 2. Funções efetivamente impressas

### 📈 Primeira função plotada

```cpp
plt::plot(x, y);
```

Isso plota **y em função de x**, isto é:

[
\boxed{
y(x) = \sin!\left(\frac{2\pi}{360},\sqrt{x}\right)
}
]

Justificativa:

* Como `x = i^2`, então `i = \sqrt{x}`
* O `plot(x, y)` associa cada `y_i` ao respectivo `x_i`

📌 **Interpretação física/matemática**
É uma **função seno**, mas com o argumento crescendo como a **raiz quadrada de x**, o que faz com que as oscilações fiquem **cada vez mais espaçadas** à medida que `x` cresce.

---

### 📉 Segunda função plotada (com legenda)

```cpp
plt::named_plot("log(x)", x, z);
```

Isso plota **z em função de x**, isto é:

[
\boxed{
z(x) = \log!\left(\sqrt{x}\right)
}
]

ou, de forma equivalente:

[
\boxed{
z(x) = \tfrac{1}{2},\log(x)
}
]

Justificativa:

* `z = log(i)`
* `i = \sqrt{x}`
* Logo:
  [
  z = \log(\sqrt{x}) = \frac{1}{2}\log(x)
  ]

📌 **Observação importante**
No código, quando `i = 0`:

```cpp
log(0)
```

isso resulta em **−∞** (valor indefinido matematicamente).
Dependendo do backend do matplotlib, isso pode:

* Ser ignorado
* Gerar warnings
* Produzir um ponto inválido

---

## 3. Resumo das funções desenhadas

| Curva | Função matemática                                     |
| ----- | ----------------------------------------------------- |
| 1ª    | ( y(x) = \sin!\left(\frac{2\pi}{360}\sqrt{x}\right) ) |
| 2ª    | ( z(x) = \frac{1}{2}\log(x) )                         |

Ambas são desenhadas **no mesmo sistema de eixos**, com:

```cpp
plt::xlim(0, n * n);
```

ou seja:

[
x \in [0, n^2]
]

---

## 4. Comportamento visual esperado

* A curva seno:

  * Oscilatória
  * Frequência aparente diminui conforme `x` cresce
* A curva logarítmica:

  * Crescimento lento
  * Sempre crescente para `x > 0`

---

Se quiser, posso:

* Reescrever isso como **funções contínuas** puras (sem discretização)
* Ajustar o código para evitar `log(0)`
* Separar os gráficos em subplots
* Analisar o efeito da escolha `x = i²` do ponto de vista matemático

Basta dizer.

