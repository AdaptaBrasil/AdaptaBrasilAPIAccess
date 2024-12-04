# Como acessar a API da plataforma AdaptaBrasil

Este repositório contem scripts para acessar os dados da plataforma AdaptaBrasil, automatizando a obtenção desses dados e possibilitando o acesso de maneira dinâmica.

O script Python [AdaptaBrasilAPIAccess.py](AdaptaBrasilAPIAccess.py) gera um CSV com todos os indicadores da plataforma. Alternativamente pode ser usado o CSV [adaptaBrasilAPIEstrutura.csv](adaptaBrasilAPIEstrutura.csv), que contém as URLs já geradas para cada indicador. Como a plataforma é constantemente atualizada, este CSV pode estar desatualizado, sendo preferível executar o script toda vez que for baixar novos dados. As instruções e parâmetros para se executar o script encontram-se abaixo.

As colunas do CSV gerado são separadas pelo caractere "|", em vez de vírgula ou ponto-e-vírgula. Quando abrir esse arquivo no Excel, indique o "|" como separador.

## Iniciando

Para acessar os dados do AdaptaBrasil são usadas URLs que especificam qual o dado a ser obtido, bem como alguma opção de filtro.

Uma das maneiras de se obter essas URLs é navegar pela plataforma com o browser em modo depuração, buscar a aba Rede (Network) do navegador e observar as URLs acessadas:

![img.png](chrome_debug.png)

Estão indicadas em vermelho as referências à URL chamada para obter dados para o preenchimento dos valores dessa tela. Se for clicado em na referência à URL (null na tela), será aberta uma outra aba do browser com os dados exibidos na tela. Os dados são retornados por default em formato JSON. Quando é especificado um formato, como no caso das URLs de download de dados, será feito um arquivo .zip contendo os dados no formato solicitado.

Se a ideia for obter dados de muitos indicadores e/ou em diferentes formatos, a melhor opção é executar o script [AdaptaBrasilAPIAccess.py](AdaptaBrasilAPIAccess.py). Ele pode receber os seguintes parâmetros:

Parâmetros:
```commandline
python AdaptaBrasilAPIAccess.py --help

Parâmetros:
  --help                         Mostra essa mensagem e sai.
  --base_url BASE_URL            URL base de uma versão do AdaptaBrasil.
  --schema SCHEMA                Esquema a ser usado. Atualmente só esta disponível o esquema adaptabrasil.
  --recorte RECORTE              Recorte a ser usado nas URLs.
  --resolucao RESOLUCAO          Resolução a ser usada nas URLs.
  --arquivo_saida ARQUIVO_SAIDA  Nome do arquivo destino (CSV).
```

Ele gerará um arquivo atualizado com as seguintes colunas:

**id**: id do ìndicador.
		  
**nome**: nome do indicador.

**url_mostra_mapas_na_tela**: Exibe o portal no navegador de acordo com os parâmetros indicados.

Exemplo: https://sistema.adaptabrasil.mcti.gov.br/5000/1/2015/null/BR/municipio/adaptabrasil

Parâmetros (separados por / após gov.br na URL):

_Indicador_: id do indicador, conforme pode ser obtido na hierarquia (5000, no exemplo).

Dado a ser exibido: formato na tela em que os dados serão exibidos (1, no exemplo). 

    1: Mapa
    2: Totais
    3: Evolução
    4: Tendência

_Ano_: Ano dos dados exibidos (2015).

_Cenário_: id do cenário a ser exibido. Os ids dos cenários possíveis estão indicados na hierarquia. 

_Recorte_: recorte a que corresponderão os dados exibidos (BR significa todo o Brasil). Os recortes possíveis estão indicados na hierarquia.

_Resolução_: resolução a que corresponderão os dados exibidos (municipio). As resoluções possíveis estão indicadas na hierarquia.

_Esquema_: O conjunto de setores estratégicos a ser acessado (atualmente o único disponível é o adaptabrasil)

**url_obtem_dados_indicador**: Obtem os dados de um indicador associados a um recorte e uma resolução.

Exemplo: https://sistema.adaptabrasil.mcti.gov.br/api/mapa-dados/BR/municipio/1000/2015/null/adaptabrasil

_Nome da API_: (fixo, mapa-dados).

_Recorte_: recorte a que corresponderão os dados exibidos (BR). Os recortes possíveis estão indicados na hierarquia.

_Resolução_: resolução a que corresponderão os dados exibidos (municipio). As resoluções possíveis estão indicadas na hierarquia.

_Indicador_: id do indicador, conforme pode ser obtido na hierarquia (1000, no exemplo).

_Ano_: Ano a que deverão corresponder os dados exibidos (2015).

_Cenário_: id do cenário a ser exibido (null, no exemplo). Os ids dos cenários possíveis estão indicados na hierarquia. 

_Esquema_: (adaptabrasil)

**url_obtem_totais_evolucao_tendencia**: Obtém dados por faixa de valores de um determinado indicador monstrados nas telas de Totais, Evolução e Tendência do Adapta Brasil:

Exemplo: https://sistema.adaptabrasil.mcti.gov.br/api/total/BR/municipio/1000/null/2015/adaptabrasil: 

_Nome da API_: (fixo, _total_).

_Recorte_: recorte a que corresponderão os dados exibidos (BR - Brasil). Os recortes possíveis estão indicados na hierarquia.

_Resolução_: resolução a que corresponderão os dados exibidos (municipio). As resoluções possíveis estão indicadas na hierarquia.

_Indicador_: id do indicador, conforme pode ser obtido na hierarquia (1000, no exemplo).

_Cenário_: id do cenário a ser exibido (null, no exemplo). Os ids dos cenários possíveis estão indicados na hierarquia. 

_Ano_: Ano a que deverão corresponder os dados exibidos (2015).

_Esquema_: (adaptabrasil)

**url_faz_download_geometrias_dados**: faz o download de geometrias com seus dados associados, em diversos formatos.

Exemplo: https://sistema.adaptabrasil.dev.apps.rnp.br/api/geometria/data/1000/BR/null/2015/municipio/SHPz/adaptabrasil

_Nome da API_: (fixo, _geometria/data_).

_Indicador_: id do indicador, conforme pode ser obtido na hierarquia (1000, no exemplo).

_Recorte_: recorte a que corresponderão os dados exibidos (BR - Brasil). Os recortes possíveis estão indicados na hierarquia.

_Cenário_: id do cenário a ser exibido (null, no exemplo). Os ids dos cenários possíveis estão indicados na hierarquia. 

_Ano_: Ano a que deverão corresponder os dados exibidos (2015).

_Resolução_: resolução a que corresponderão os dados exibidos (municipio). As resoluções possíveis estão indicadas na hierarquia.

Formatos geoespaciais disponíveis:

    SHPz    : shapefile (arquivo zip contendo os vários arquivos que compõe o formato).
    GEOJSONz: geoJSON
    KMZz    : formato compatível com o Google Maps

Formatos tabulares disponíveis:

    JSONz: JSON
    XLSXz: planilha Excel
    CSV  :   CSV (texto com colunas separadas por ';')

Formato de imagem disponível:

    PNG: png

_Esquema_: (adaptabrasil)

**descricao_simples**: descrição simplificada do que os dados desse indicador representam.

**descricao_completa**: descrição detalhada do indicador.

**nivel**: nível do indicador na hierarquia que os agrupa. Só os indicadores de nívem maior que 1 possuem dados associados a eles.

**proporcao_direta**: indica se quanto maior o valor pior ou melhor o significado dele.

Valores:

    0: indica que valores maiores significam uma situação pior.
    1: indica que valores maiores significam uma situação melhor.

**indicador_pai**: os indicadores formam uma hierarquia. Os indicadores de nivel "1", que correspondem aos Setores Estratégicos, agrupam alguns dos de nível "2" e assim por diante, e essa coluna expressa essa relação.

**anos**: anos para os quais há valores desse indicador.

**setor_estrategico**: setor estratégico ao qual pertence o indicador.

**tipo_geometria**: tipo das geometrias usadas nesse indicador: Multipolygon, MultilineString, MultiPoint.

**unidade_medida**: unidade de medida dos valores do indicador.

**cenários**: cenários possíveis para esse indicador.

### API de hierarquia

A API de hierarquia acessa todos os indicadores que compõe o site (sem os dados). Um exemplo do retornado por essa API pode ser visto [aqui](https://sistema.adaptabrasil.mcti.gov.br/api/hierarquia/adaptabrasil).

O parâmetro **adaptabrasil** especifica o esquema de dados a ser acessado. Atualmente há apenas um esquema disponível, chamado **adaptabrasil**.
