# Configuração do Projeto C++ com Neovim

## Atalhos Rápidos

| Tecla | Comando | Descrição |
|-------|---------|-----------|
| `s<CR>` | `make configure` | Configura o projeto (CMake) |
| `m<CR>` | `make build` | Compila o projeto |
| `<space><CR>` | `./build/app_example` | Executa o aplicativo |
| `<C-l>` | `rm -rf build/` | Limpa os arquivos compilados |

## Configuração

Adicione no seu `after/ftplugin/cpp.lua`:

```lua
vim.g.projectionist_heuristics = {
    ["*.cpp"] = {
        ["*.cpp"] = {
            ["start"] = "make configure",
            ["make"] = "make build",
            ["run"] = "lua require('config.neovim_dev').app('./build/app_example')",
            ["clean"] = "!rm -rf {project}/build",
            ["type"] = "cpp",
        },
    },
}
```

## Como usar

1. Pressione `s<CR>` para configurar o projeto
2. Pressione `m<CR>` para compilar
3. Pressione `<space><CR>` para executar
4. Pressione `<C-l>` para limpar os arquivos build
