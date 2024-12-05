import urllib.request, json
import argparse
import re

def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Programa para obter metadados da API do AdaptaBrasil.')
    parser.add_argument('--base_url', type=str,
                        default = 'https://sistema.adaptabrasil.mcti.gov.br',
                        help='URL base de uma versão do AdaptaBrasil.')
    parser.add_argument('--schema', type=str,
                        default='adaptabrasil',
                        help='schema a ser usado (adaptabrasil, impactos_economicos).')
    parser.add_argument('--recorte', type=str,
                        default='BR',
                        help='Recorte a ser usado nas URLs.')
    parser.add_argument('--resolucao', type=str,
                        default='municipio',
                        help='Resolução a ser usada nas URLs.')
    parser.add_argument('--arquivo_saida', type=str,
                        default = 'adaptaBrasilAPIEstrutura.csv',
                        help='Nome do arquivo destino (csv).')
    parser.add_argument('--separador_csv', type=str,
                        default = '|',
                        help='Separador de colunas a ser usado no csv gerado.')
    return parser.parse_args()

def if_none(value):
    return value if value is not None else ''

CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

if __name__ == '__main__':
    args = get_command_line_arguments()
    url_hierarchy = f"{args.base_url}{'' if args.base_url[-1] == '/' else '/'}api/hierarquia/{args.schema}"
    with urllib.request.urlopen(url_hierarchy) as url, open(args.arquivo_saida,mode='w', encoding='utf-8') as csv_file:
        indicators = json.load(url)
        s = '\ufeff' # BOM code to preserve diacritics em Excel
        s += f'id{args.separador_csv}nome{args.separador_csv}url_mostra_mapas_na_tela{args.separador_csv}url_obtem_dados_indicador{args.separador_csv}url_obtem_totais_evolucao_tendencia{args.separador_csv}url_faz_download_geometrias_dados{args.separador_csv}' \
             f'descricao_simples{args.separador_csv}descricao_completa{args.separador_csv}nivel{args.separador_csv}proporcao_direta{args.separador_csv}indicador_pai{args.separador_csv}' \
             f'anos{args.separador_csv}setor_estrategico{args.separador_csv}tipo_geometria{args.separador_csv}unidade_medida{args.separador_csv}cenarios\n'
        list_scenario = []
        seps = {}
        for indicator in indicators:
            years = None
            if indicator['years'] is None:
                pass
            elif type(indicator['years']) is list:
                years = indicator['years']
            else:
                years = indicator['years'].split(',')
            if indicator['sep_description'] is not None:
                seps[indicator['sep_id']] = cleanhtml(indicator['sep_description'])
            url_getmapdata = ''
            url_gettotal_evolucao_tendencia = ''
            url_download = ''
            url_show_map_on_the_site = ''
            list_scenario = []
            if indicator['scenarios'] is None:
                pass
            else:
                for scenario in indicator['scenarios']:
                    list_scenario.append(scenario['label'])
            if years is not None and years != []:
                # https://sistema.adaptabrasil.mcti.gov.br/5000/1/2015/null/BR/municipio/
                url_show_map_on_the_site = f"{args.base_url}/{indicator['id']}/1/{years[0]}/null/{args.recorte}/{args.resolucao}/{args.schema}"
                # https://sistema.adaptabrasil.dev.apps.rnp.br/api/mapa-dados/BR/municipio/1000/2015/null
                url_getmapdata = f"https://sistema.adaptabrasil.mcti.gov.br/api/mapa-dados/{args.recorte}/{args.resolucao}/" \
                                 f"{indicator['id']}/{years[0]}/null/{args.schema}"
                # https://sistema.adaptabrasil.mcti.gov.br/api/total/BR/municipio/5000/2/null
                url_gettotal_evolucao_tendencia = f"https://sistema.adaptabrasil.mcti.gov.br/api/total/{args.recorte}/{args.resolucao}/" \
                                                  f"{indicator['id']}/null/{years[0]}/{args.schema}"
                # https://sistema.adaptabrasil.dev.apps.rnp.br/api/geometria/data/1000/BR/null/2015/municipio/SHPz
                url_download = f"https://sistema.adaptabrasil.dev.apps.rnp.br/api/geometria/data/{indicator['id']}/" \
                               f"{args.recorte}/null/{years[0]}/{args.resolucao}/SHPz/{args.schema}"

                s += f"{indicator['id']}{args.separador_csv}{indicator['name']}{args.separador_csv}"
                s += f"{url_show_map_on_the_site}{args.separador_csv}{url_getmapdata}{args.separador_csv}{url_gettotal_evolucao_tendencia}{args.separador_csv}{url_download}{args.separador_csv}" \
                    f"{indicator['simple_description']}{args.separador_csv}{indicator['complete_description']}{args.separador_csv}{indicator['level']}{args.separador_csv}" \
                    f"{if_none(indicator['pessimist'])}{args.separador_csv}{if_none(indicator['indicator_id_master'])}{args.separador_csv}{if_none(indicator['years'])}{args.separador_csv}" \
                    f"{if_none(seps[indicator['sep_id']])}{args.separador_csv}{if_none(indicator['geometrytype']) if int(indicator['level']) > 1 else ''}{args.separador_csv}{if_none(indicator['measurement_unit'])}{args.separador_csv}" \
                    f"{if_none(list_scenario)}".replace('\r', ' ').replace('\n', ' ')
                s += "\n"
        csv_file.write(s)
    print('Feito!')


