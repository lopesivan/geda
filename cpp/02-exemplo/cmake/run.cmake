# cmake/run.cmake

# Adia a criação do target para o final da configuração do CMake
cmake_language(DEFER CALL create_run_target)

function(create_run_target)
    if(NOT TARGET run)
        if(TARGET app_example)
            add_custom_target(run
                COMMAND $<TARGET_FILE:app_example>
                DEPENDS app_example
                COMMENT "Executando o aplicativo app_example..."
                USES_TERMINAL
                VERBATIM
            )
        else()
            message(WARNING "Target 'app_example' nao encontrado. O target 'run' nao foi criado.")
        endif()
    endif()
endfunction()

# O erro Sem regra para processar o alvo 'run' acontece por causa da ordem em
# que o CMake avalia as coisas.
#
# Quando o CMAKE_PROJECT_INCLUDE roda, o seu CMakeLists.txt principal ainda
# não executou a linha add_executable(...). Por isso, na verificação if(TARGET
# app_example), o target app_example ainda não existe na memória do CMake!
# Como a condição resulta em falso e o else() estava comentado, o target run
# simplesmente não foi criado.
#
# Solução
# Altere o arquivo cmake/run.cmake para usar cmake_language(DEFER ...). Isso
# diz ao CMake para só registrar o target run no final da leitura de todo o
# CMakeLists.txt, quando o app_example já terá sido declarado:
