# Catálogo de Produtos - ListaProdutos

Este é um catálogo de produtos responsivo e interativo, desenvolvido em HTML, CSS e JavaScript puro. Ele exibe produtos organizados por categorias, com navegação suave, funcionalidade de busca e design moderno.

## Funcionalidades

### 1. **Estrutura Geral**
- **Header Principal**: Contém o logo da empresa no canto esquerdo e o título do catálogo. Fundo com gradiente e imagem de fundo para um visual atrativo.
- **Barra de Pesquisa**: Localizada logo abaixo do header. Permite buscar produtos por nome (baseado no título do card).
- **Seções de Categorias**: Cada categoria é uma "página" vertical separada, com header próprio contendo título e subtítulo, fundo com imagem e gradiente.
- **Cards de Produtos**: Exibem imagem, referência, título, preços (débito/crédito e à vista) e informações adicionais (unidade, peso).
- **Footer**: Informações de contato no final da página.

### 2. **Layout Responsivo**
- **Grid de Cards**: 3 colunas em telas grandes (desktop), 2 em médias (tablet), 1 em pequenas (mobile).
- **Navegação Flutuante**: Botões fixos no canto inferior esquerdo para navegar entre seções.
- **Scroll Snap**: As seções se "encaixam" suavemente ao rolar, simulando páginas verticais.

### 3. **Navegação**
- **Botões Flutuantes**:
  - **Anterior**: Volta para a seção anterior.
  - **🔍 (Busca)**: Foca e rola suavemente para a barra de pesquisa.
  - **Próxima**: Avança para a próxima seção.
- **Ocultação Automática**: Os botões desaparecem quando o footer entra na visão (usando IntersectionObserver).
- **Scroll Suave**: Navegação entre seções com animação suave.

### 4. **Funcionalidade de Busca**
- **Filtro em Tempo Real**: Digite na barra de pesquisa para filtrar cards por título (case-insensitive).
- **Exibição de Resultados**: Quando há busca ativa, os headers das categorias são ocultados e os cards filtrados aparecem em um grid abaixo da barra.
- **Sem Resultados**: Se nenhum produto corresponder, exibe "Item não encontrado!" centralizado.
- **Limpeza**: Ao apagar o texto da busca, volta à visualização normal das seções.

### 5. **Interações e UX**
- **Hover Effects**: Botões flutuantes sobem levemente ao passar o mouse.
- **Foco Automático**: O botão de busca rola para a barra e foca nela.
- **Acessibilidade**: Botões com aria-label para leitores de tela.

## Como Utilizar

1. **Abrir o Catálogo**:
   - Abra o arquivo `index.html` em qualquer navegador moderno (Chrome, Firefox, Edge, etc.).

2. **Navegar pelas Categorias**:
   - Use os botões flutuantes no canto inferior esquerdo: "ANTERIOR" para voltar, "🔍" para ir à busca, "PRÓXIMA" para avançar.
   - Ou role a página normalmente – as seções se encaixam suavemente.

3. **Buscar Produtos**:
   - Clique na barra de pesquisa ou use o botão 🔍 para focar nela.
   - Digite o nome do produto (ex.: "amendoa").
   - Os resultados aparecem imediatamente abaixo da barra, com headers ocultos.
   - Se nada for encontrado, verá "Item não encontrado!".

4. **Visualizar Detalhes**:
   - Cada card mostra imagem, preços e infos. Passe o mouse para interações (se aplicável).

5. **Responsividade**:
   - Redimensione a janela do navegador para ver o layout se adaptar (desktop → tablet → mobile).

## Estrutura de Arquivos

- `index.html`: Página principal com HTML, CSS inline e JavaScript.
- `styles.css`: Estilos CSS para layout, responsividade e visual.
- `pagina/` (pasta): Contém imagens usadas nos fundos (ex.: logo, headers).

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica.
- **CSS3**: Flexbox, Grid, Gradientes, Transições, Media Queries.
- **JavaScript (ES6+)**: DOM manipulation, Event listeners, IntersectionObserver para interações dinâmicas.

## Notas Técnicas

- **Sem Frameworks**: Tudo em vanilla (puro) para simplicidade e performance.
- **Performance**: Cards são clonados para busca, evitando recriação desnecessária.
- **Compatibilidade**: Funciona em navegadores modernos; evite IE11.
- **Customização**: Cores e estilos são definidos via variáveis CSS (`--accent`, `--bg1`, etc.).

Se precisar de ajustes ou novas funcionalidades, edite os arquivos diretamente!</content>
<parameter name="filePath">d:\ListProducts\Pagina\README.md