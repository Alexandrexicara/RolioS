# RollOS Native Launcher (Android)

Este módulo é a base nativa para que o RollOS funcione como tela inicial real do Android.

## Comportamento
- Declara a atividade como launcher HOME do Android.
- Consulta os aplicativos instalados que oferecem uma atividade de inicialização.
- Mostra automaticamente nome e ícone de cada aplicativo em uma grade.
- Abre o aplicativo ao tocar no ícone.
- Atualiza a grade quando aplicativos são instalados, removidos ou alterados e também ao voltar para a tela inicial.
- Não mantém uma lista manual: consulta o Package Manager do Android.

## Instalação e teste
Abra a pasta android-launcher no Android Studio, sincronize o Gradle, gere o APK de debug, instale em um aparelho Android e selecione RollOS como aplicativo de tela inicial padrão.

## Limitações
- O código-fonte Android ainda precisa ser compilado, instalado e testado em aparelho físico.
- Só aparecem aplicativos que oferecem uma atividade de inicialização. Componentes sem ícone de launcher não aparecem como aplicativos.
- QUERY_ALL_PACKAGES é uma permissão sensível; publicação na Google Play depende das políticas e aprovação aplicáveis.
- Isso não transforma o site Netlify em sistema operacional nem instala APKs. O launcher nativo exibe os aplicativos já instalados no Android.
