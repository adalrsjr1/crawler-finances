## Rendimentos Mensais

Assimg como nos modelos de valuation para ações, definir o fluxo de caixa
futuro é uma das tarefas mais importantes e, muitas vezes complicada, para um
bom cálculo do preço justo.

No caso dos fundos imobiliários temos, basicamente, 3 categorias de fluxo de
caixa, através dos rendimentos mensais:

#### I. Constantes

Caso do fundo Europar (EURO11), que desde agosto/2008 distribui o rendimento de
R$ 1,36 por cota.

É importante citar também os fundos que garantem um rendimento mensal mínimo
através de seu regulamento, como o Fundo Floripa Shopping (FLRP11B), que
distribui mensalmente R$ 8,80 por cota.

#### II. Praticamente Constantes

São fundos que distribuem um rendimento muito próximo de uma média.

Um exemplo é o Fundo Hospital Nossa Senhora de Lourdes (NSLU11B), cujo
rendimento se dá em torno dos R$ 1,56 por cota, embora este valor não seja
preciso todo mês, variando entre R$ 1,53 e R$ 1,60.

#### III. Inconstantes

Fundos cujo rendimento tem grandes variações de mês em mês. Um exemplo é o
Fundo Panamby (PABY11), que às vezes distribui R$ 0,1302 por cota e em outro
mês R$ 1,7547.

#### Método Utilizado

Portanto, uma solução para amenizar o problema de existirem diversas categorias
de distribuição de rendimentos, optei por utilizar um método simples e eficaz:
média do rendimento distribuído nos últimos 12 meses.

Caso o fundo tenha menos de 12 meses de negociação considero a média de todo o
período.

## Preço Atual do Fundo

Nesta parte não tem mistério…basta utilizarmos o preço atual do fundo
imobiliário, que pode ser visto através [do clube do
FII!](https://www.clubefii.com.br/)

## Taxa de Desconto

Este é outro dado de entrada extremamente importante e presente em todo modelo
de precificação.

Seu significado é simples. A taxa de desconto, dada por um investimento livre
de risco (risk-free), mostra a rentabilidade mínima que um investimento deve
gerar para viabilizar o investimento nele.

Observação: Na prática, nenhum investimento é livre de risco. Mas utilizaremos
esta denominação para facilitar a compreensão do que é um investimento com
risco muito baixo.

Em palavras mais claras, se um título público, considerado como livre de risco,
paga 10% ao ano, um ativo mais arriscado deve, no mínimo ter uma rentabilidade
esperada superior a 10% para compensar este risco adicional.

Se o ativo tiver uma rentabilidade de 8%, por exemplo, não valerá a pena
investir nele, já que você pode conseguir os 10% com risco bem inferior a este
ativo.

O nome “taxa de desconto” é utilizado por indicar que o preço justo do ativo em
análise já desconta a taxa de um investimento livre de risco.  Qual é o melhor
ativo para representar a taxa de desconto?

Como utilizamos a média nos últimos 12 meses dos rendimentos como um dos dados
de entrada do modelo, seria mais do que justo considerar um investimento cuja
taxa reflita a mesma periodicidade, não é mesmo?

Portanto, precisamos de um ativo livre de risco que apresente uma taxa para os
próximos 12 meses.

Considerar uma LTN ou qualquer outro título público, embora seja uma boa opção,
não reflete totalmente o período que desejamos.

Por exemplo, uma LTN com vencimento em 01/01/2012 apresenta menos do que 1 ano
de duração. E, conforme o tempo passa, cada vez menos dias até seu vencimento.

Logo, o ativo mais adequado na minha opinião para utilizarmos como taxa de
desconto deve ter uma duração constante de 12 meses (1 ano).

Felizmente, a Anbima possui um índice chamado de “Índice de Duração Constante
Anbima” cuja sigla é IDkA e que reflete a taxa para diversas durações,
abrangendo os títulos pré-fixados e indexados ao IPCA.

No caso, utilizaremos a taxa do IDkA Pré de 1 ano (IDkA Pré 1A) para nosso
modelo de precificação.

A consulta da taxa, assim como outros parâmetros do índice, pode ser feita
através [deste link!](http://www.anbima.com.br/idka/IDkA.asp), no próprio site
da Anbima. Considere a taxa de compra (D-1).

## Imposto de Renda

Um dos maiores benefícios dos fundos imobiliários está no fato da distribuição
mensal deles serem isentas de impostos.

Na teoria, os fundos devem se enquadrar em algumas condições, mas, na prática,
todos os fundos que acompanhamos no site Fundo Imobiliário estão dentro destas
condições.

Seria injusto não considerar o imposto de renda em aplicações de renda-fixa,
como os títulos públicos, em nosso modelo de precificação dos fundos
imobiliários.  Qual imposto de renda devo considerar?

O imposto de renda em aplicações de renda-fixa se dá através do modelo
regressivo, conforme imagem abaixo:

Taxa | Período
-----|---------
22.5% | Antes de 6 meses
20.0% | Entre 6 meses e 1 ano
17.5% | Entre 1 ano e 2 anos
15.0% | Após 2 anos

Portanto, como nosso modelo de precificação está alinhado para o período de 1
ano, podemos considerar a alíquota de 17,50% do imposto de renda, associada ao
período de venda do título em renda-fixa entre 1 ano e 2 anos.

Poderíamos optar pela alíquota de 20% também, mas prefiro ser sempre
conservador nestes modelos de precificação para garantir uma segurança
adicional.

Esta alíquota do imposto de renda incidirá sobre a taxa de desconto de 1 ano
que havíamos definido no item anterior.

## Prêmio de Risco

O Prêmio de Risco poderia estar já estar embutido na própria taxa de desconto
mas preferi definí-lo como um dado de entrada único para facilitar sua
explicação.

Conforme comentamos, os fundos imobiliários apresentam maiores riscos do que o
investimento em um título público.

Dentre todos, acho importante citar quatro:

I. Risco de Crédito – Inadimplência ou o vulgo “calote”;

II. Risco Vacância – Desocupação do imóvel;

III. Risco de Liquidez – Possibilidade de não executar um negócio;

IV. Risco de Mercado – Flutuação no preço do fundo, podendo ocorrer perdas no
valor da cota.

Portanto, para o investimento em fundos imobiliários ser viável, é importante
que ele ofereça um retorno adicional em relação a um investimento livre de
risco, como os títulos públicos.

Para esta rentabilidade adicional damos o nome de “Prêmio de Risco”. O ativo
deve oferecer um prêmio (retorno adicional) devido ao seu maior risco.

Em nosso modelo utilizaremos um prêmio de risco de 10% sobre a taxa de
desconto.

Logo, se ela for de 10%, ao adicionarmos o prêmio de risco, temos uma nova taxa
de desconto de 11% [ 10% * ( 1 + 10% ) ].

Repare que os 10% não são simplesmente somados a taxa anterior. Este valor é
totalmente arbitrário, dependendo do gosto do freguês.

Eu prefiro usar 10%, mas você pode ser ainda mais conservador usando, por
exemplo 20% ou até mesmo retirar este valor.

# Resultados do modelo

Após analisarmos os dados de entrada, resta-nos entender os resultados
intermediários do cálculo do preço justo e, posteriormente, o cálculo final do
valor intrínseco destes fundos.

## Yield Mensal

Caso você já acompanhe os fundos imobiliários conhece bem este termo. Se é um
novo investidor saiba que não há mistério nenhum em relação a este termo. Ele
simplesmente representa a relação entre o rendimento mensal do fundo e seu
preço.

Por exemplo, se um fundo imobiliário distribui R$ 1,00 por cota mensalmente e
seu preço atual é de R$ 100,00, seu yield mensal será de 1,00% ( 1 / 100 ).

Nosso modelo, como considera a média dos rendimentos 12 últimos meses, terá o
cálculo do yield mensal da seguinte forma:média dos rendimentos nos últimos 12
meses / preço atual.

## Taxa de Desconto Mensal – Modificada

Após definirmos a taxa de desconto nos dados de entrada podemos calcular qual
será esta taxa mensal após incluirmos o imposto de renda e o prêmio de risco.

Esta taxa é uma referência para comparação com o yield mensal.

Um exemplo: Se o yield mensal do fundo for de 0,83% e a taxa de desconto mensal
– modificada de 0,89% sabemos que o fundo apresenta um downside.

Ou seja, é preferível investir em títulos públicos do que neste fundo
imobiliário, já que 0,89% > 0,83%.  8. Yield Anual

Nada mais é do que o yield mensal anualizado. A fórmula é a seguinte:

( 1 + yield mensal ) ^ ( 12 ) -1

Por exemplo, se o yield mensal for de 1% temos: ( 1 + 0,01 ) ^ (12 ) -1 =
12,68%.

## Taxa de Desconto Final

Considera o imposto de renda e o prêmio de risco para gerar uma taxa de
desconto final. Exemplo:

I. Taxa de desconto = 12,48%;

II. Imposto de renda = 17,50%;

III. Prêmio de risco = 10,00%

Taxa de Desconto Final = 12,48% * ( 1 – 17,50% ) * ( 1 + 10,00% ) = 11,33%

É apenas um taxa de referência para o modelo, sem interferência nos cálculos
para o preço justo do fundo.  Cálculo Preço Justo

Com todas as informações acima já podemos gerar o preço justo de um fundo
imobiliário desejado.

## Preço Justo

O preço justo, ou valor intrínseco, é uma simples divisão entre a média do
rendimento dos últimos 12 meses e a Taxa de desconto mensal – modificada.

Exemplo:

I. média do rendimento dos últimos 12 meses = R$ 0,8333

II. Taxa de desconto mensal – modificada = 0,89%

Preço Justo = 0,8333 / 0,89 = R$ 93,23.

Logo, se o preço atual do fundo é de R$ 100,00 ele apresenta um downside. Seu
preço justo está abaixo do preço atual. Neste caso, o downside seria de -6,77%
[ ( 93,23 / 100,00 ) – 1 ].

## [Referência](https://hcinvestimentos.com/2011/05/18/como-calcular-o-preco-justo-dos-fundos-imobiliarios/)
