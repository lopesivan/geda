# 🎯 Resumo do que o código faz:

## **Matemática dos Números Complexos**
O código usa uma técnica elegante: representa pontos 2D
como **números complexos** (x + iy), onde:
- `e^(iθ) = cos(θ) + i·sin(θ)` (Fórmula de Euler)
- Multiplicar por `a` escala o raio
- Somar `xy[0] + i·xy[1]` translada para a posição desejada

### **Estrutura da Animação (3 fases):**

1. **Fase 0** → Desenha hexágonos vazios coloridos em padrão de colmeia
2. **Fase 1** → Adiciona estrelas Y (divide cada hexágono em 3 setores)
3. **Fase 2** → Adiciona grades paralelas dentro de cada setor

### **Padrão de Colmeia:**


- Linhas pares e ímpares deslocadas (`.5*(k % 2)`)
- Espaçamento vertical compactado (`1.5*r` ao invés de `2*r`)

### **Por que usar números complexos?**
✅ Código mais compacto e elegante
✅ Rotações são apenas multiplicações por `e^(iθ)`
✅ Evita trigonometria manual com sin/cos separados

