# cmake/run.cmake

cmake_language(DEFER CALL create_run_target)

function(create_run_target)
    if(NOT TARGET run)
        if(TARGET ${PROGRAM})
            # ARGS é lido em tempo de execução (variável de ambiente).
            # Sem ARGS, usa exemplo.sch.
            add_custom_target(run
                COMMAND sh -c "\"$0\" \${ARGS:-exemplo.sch}" $<TARGET_FILE:${PROGRAM}>
                DEPENDS ${PROGRAM}
                WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                COMMENT "Executando o aplicativo ${PROGRAM}..."
                USES_TERMINAL
                VERBATIM
            )
        else()
            message(WARNING "Target '${PROGRAM}' nao encontrado. O target 'run' nao foi criado.")
        endif()
    endif()
endfunction()

