# Roteiro de desenvolvimento

## Marco 0.2 — protótipo e serviços iniciais
- [x] Interface web responsiva para demonstração no Netlify.
- [x] Simulação de expansão da tela no navegador.
- [x] Cliente opcional NVIDIA NIM no protótipo desktop.
- [x] Roll Core: configuração local e eventos.
- [x] Roll Display: cálculo de dimensões e modo compacto/expandido.
- [x] Roll Storage: consulta informativa de espaço em disco, sem apagar dados.
- [x] Testes unitários iniciais dos serviços.

## Marco 0.3 — integração
- [ ] Integrar os serviços ao shell desktop.
- [ ] Testes em Windows e Linux.
- [ ] Backend seguro para IA; chave NVIDIA nunca deve ir para JavaScript do navegador.
- [ ] CI para executar os testes em cada push.

## Marco 0.4 — plataforma móvel
- [ ] Definir SoC e dispositivo ARM de referência.
- [ ] Validar suporte upstream de kernel, GPU, modem e painel.
- [ ] Escolher base Linux móvel e plano de boot/atualização.
- [ ] Só então iniciar drivers e integração de sensores/motores.

## Segurança e escopo
O protótipo atual roda em espaço de usuário. Não altera partições, não controla motores e não instala kernel. A leitura de armazenamento é somente informativa. A conexão de IA em nuvem deve ocorrer no backend, protegendo credenciais.
