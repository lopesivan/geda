Vou manter **a mesma estrutura do seu código**, mas agora explicitar **seno e cosseno** sendo plotados corretamente, e depois explico **quais funções matemáticas aparecem no gráfico**.

---

## Código C++ (seno e cosseno)

```cpp
#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

int main()
{
    int n = 1000;

    std::vector<double> x, y_sin, y_cos;

    for(int i = 0; i < n; i++)
    {
        // variável independente
        double xi = i * i;   // x = i²

        x.push_back(xi);

        // seno e cosseno
        y_sin.push_back(std::sin(2 * M_PI * i / 360.0));
        y_cos.push_back(std::cos(2 * M_PI * i / 360.0));

        if(i % 10 == 0)
        {
            plt::clf();

            // seno
            plt::named_plot("sin(2πi/360)", x, y_sin);

            // cosseno
            plt::named_plot("cos(2πi/360)", x, y_cos);

            plt::xlim(0, n * n);
            plt::title("Seno e Cosseno");
            plt::legend();
            plt::pause(0.01);
        }
    }
}
```

---

## Quais funções estão sendo impressas?

Assim como antes, o `plot(x, y)` **não plota em função de `i`**, mas **em função de `x = i²`**.

### 1️⃣ Função seno

No código:

```cpp
y_sin = sin(2π i / 360)
x     = i²
```

Logo, no gráfico:

[
\boxed{
y(x) = \sin!\left(\frac{2\pi}{360}\sqrt{x}\right)
}
]

---

### 2️⃣ Função cosseno

No código:

```cpp
y_cos = cos(2π i / 360)
x     = i²
```

Logo, no gráfico:

[
\boxed{
y(x) = \cos!\left(\frac{2\pi}{360}\sqrt{x}\right)
}
]

---

## Interpretação matemática do gráfico

* **Ambas são funções trigonométricas**
* O argumento depende de (\sqrt{x}), não de (x)
* Isso causa um efeito visual importante:

📌 **As oscilações ficam mais espaçadas conforme x cresce**, porque:
[
\theta = \frac{2\pi}{360}\sqrt{x}
]

ou seja, a “frequência aparente” diminui ao longo do eixo x.

---

## Observação didática importante

Se o seu objetivo fosse plotar **sin(x)** e **cos(x)** no sentido usual (argumento linear), o correto seria:

```cpp
double xi = i * 2 * M_PI / n;
x.push_back(xi);
y_sin.push_back(std::sin(xi));
y_cos.push_back(std::cos(xi));
```

Mas **no seu código atual**, você está conscientemente explorando a relação:

[
x = i^2
]

o que é matematicamente válido e interessante.

---

Se quiser, no próximo passo posso:

* Reescrever para **argumento angular contínuo**
* Fazer **animação didática mostrando fase**
* Comparar **sin(i)** × **sin(√x)** no mesmo gráfico
* Relacionar isso com **frequência instantânea**

É só dizer como quer aprofundar.

