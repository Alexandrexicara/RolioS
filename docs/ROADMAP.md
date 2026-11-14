# Roteiro de desenvolvimento do RollOS

## Marco 0.2 — prévia e serviços iniciais
- [x] Interface web responsiva de demonstração publicada na Netlify.
- [x] Simulação de expansão da tela no navegador.
- [x] Roll Core: configuração local e log de eventos.
- [x] Roll Display: cálculo de dimensões e modo compacto/expandido.
- [x] Roll Storage: consulta informativa, sem apagar dados.
- [x] Cliente opcional NVIDIA NIM no protótipo desktop.
- [x] Catálogo conceitual de aplicativos.

## Marco 0.3 — protótipo desktop
- [x] Integrar os serviços ao shell desktop PySide6.
- [x] Registrar inicialização e mudanças do modo de tela.
- [x] Exibir status da integração NVIDIA sem mostrar a chave.
- [ ] Corrigir qualquer falha apontada pelo GitHub Actions.
- [ ] Aprovar testes automatizados em Linux e Windows.
- [ ] Validar interface em diferentes resoluções, escalas e tamanhos de janela.
- [ ] Tratar corretamente o fechamento da janela durante chamadas de IA.
- [ ] Testar erros de rede, timeout, resposta inválida e chave NVIDIA ausente.
- [ ] Criar backend autenticado e com limites de uso para a IA na prévia web.

## Marco 0.35 — Roll Cloud inicial\n- [x] Cliente Neon Management API para listar organizações e criar projeto PostgreSQL na conta escolhida.\n- [x] Chave pessoal solicitada em tempo de execução, sem persistência no RollOS.\n- [x] URI PostgreSQL guardada no cofre de credenciais do sistema operacional no protótipo desktop.\n- [x] Criação idempotente das tabelas iniciais de metadados e preferências.\n- [x] Criação de bucket privado de Object Storage (API beta; sujeito à disponibilidade).\n- [x] Confirmação explícita antes de criar projeto (ação sujeita aos limites/plano Neon).\n- [ ] Executar testes automatizados do cliente Neon em CI Windows/Linux.\n- [ ] Obter aprovação/credenciais do programa de parceria Neon para OAuth oficial.\n- [ ] Implementar callback OAuth com state/PKCE, refresh seguro e revogação.\n- [ ] Conectar o backend RollOS ao banco usando segredo guardado no servidor, não no cliente móvel.\n- [ ] Criar bucket privado de Object Storage e uploads/downloads com URLs assinadas.\n- [ ] Implementar quotas por usuário, limites de tamanho, verificação de tipo, antivírus e exclusão/exportação de dados.\n\n## Marco 0.4 — base móvel
- [ ] Escolher um dispositivo ARM real de referência.
- [ ] Confirmar SoC, GPU, modem, painel, controlador de toque, sensores e documentação do fabricante.
- [ ] Selecionar base Linux móvel compatível e política de licenças.
- [ ] Definir bootloader, kernel suportado, device tree e estratégia de recuperação.
- [ ] Definir partições, criptografia, atualização segura e rollback.
- [ ] Criar imagem inicializável de desenvolvimento para o aparelho escolhido.

## Marco 0.5 — hardware expansível
- [ ] Obter especificações elétricas e protocolo do painel/mecanismo expansível.
- [ ] Implementar driver somente com documentação e hardware de teste.
- [ ] Integrar sensores de posição e limites de segurança do mecanismo.
- [ ] Ajustar interface automaticamente conforme dimensões reais reportadas pelo sistema.
- [ ] Testar ciclos de expansão, falhas e recuperação sem danificar o painel.

## Marco 0.6 — experiência de uso
- [ ] Implementar inicialização, bloqueio de tela, configurações e gerenciamento de energia.
- [ ] Implementar conectividade móvel, Wi-Fi, Bluetooth, áudio, câmera e localização conforme suporte do aparelho.
- [ ] Criar loja com catálogo assinado, permissões, instalação, atualização e remoção.
- [ ] Implementar armazenamento real com permissões e limpeza segura controlada pelo usuário.
- [ ] Implementar perfis de desempenho e camada de jogos.
- [ ] Preparar instalador, documentação e atualização de sistema.

## Critérios para considerar funcional
- Inicializa no dispositivo físico escolhido e recupera de falhas de boot.
- Reconhece tela, toque, conectividade, áudio e sensores suportados.
- A interface muda com dados reais do painel, não com um controle de demonstração.
- Atualizações são verificadas e podem ser revertidas.
- Aplicativos são instalados por uma fonte confiável, com permissões explícitas.
- IA funciona sem expor chaves no aplicativo cliente.

## Bloqueios externos
O kernel, drivers, imagem instalável e controle do mecanismo não podem ser concluídos corretamente sem um aparelho ARM de referência, documentação do fabricante e acesso ao hardware. Até lá, o desenvolvimento seguro se concentra no protótipo, nos serviços independentes e na automação de testes.

## Segurança e escopo
O protótipo atual roda em espaço de usuário. Não altera partições, não controla motores e não instala kernel. A leitura de armazenamento é somente informativa. O catálogo ainda não instala pacotes. Nenhuma chave ou senha deve ser incluída no repositório.
