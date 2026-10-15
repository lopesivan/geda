def texto(x, y, conteudo, tamanho=10, cor=9, alinhamento=0):
    return (
        f"T {x} {y} {cor} {tamanho} 1 0 0 {alinhamento} 1\n"
        f"{conteudo}\n"
    )


footer = [
    texto(50000, 40900, "Circuito RC - Filtro Passa-Baixas", 20),
    texto(50000, 40350, "exemplo.sch"),
    texto(53900, 40350, "1.0"),
    texto(50000, 40100, "1"),
    texto(51500, 40100, "1"),
    texto(53900, 40100, "Ivan Carlos da Silva Lopes"),
]

print("".join(footer))

