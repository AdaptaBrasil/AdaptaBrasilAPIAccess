import urllib.request, json
import argparse
import re

def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Programa para obter metadados da API do AdaptaBrasil.')
    parser.add_argument('--base_url', type=str,
                        default = 'https://sistema.adaptabrasil.mcti.gov.br/',
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
    return parser.parse_args()

def if_none(value):
    return value if value is not None else ''

CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

if __name__ == '__main__':
    args = get_command_line_arguments()
    url_hierarchy = f"{args.base_url}/api/hierarquia/{args.schema}"
    with urllib.request.urlopen(url_hierarchy) as url, open(args.arquivo_saida,mode='w', encoding='utf-8') as csv_file:
        indicators = json.load(url)
        s = '\ufeff' # BOM code to preserve diacritics em Excel
        s += 'id|nome|url_mostra_mapas_na_tela|url_obtem_dados_indicador|url_obtem_totais_evolucao_tendencia|url_faz_download_geometrias_dados|' \
             'descricao_simples|descricao_completa|nivel|proporcao_direta|indicador_pai|' \
             'anos|setor_estrategico|tipo_geometria|unidade_medida|cenarios\n'
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

                s += f"{indicator['id']}|{indicator['name']}|"
                s += f"{url_show_map_on_the_site}|{url_getmapdata}|{url_gettotal_evolucao_tendencia}|{url_download}|" \
                    f"{indicator['simple_description']}|{indicator['complete_description']}|{indicator['level']}|" \
                    f"{if_none(indicator['pessimist'])}|{if_none(indicator['indicator_id_master'])}|{if_none(indicator['years'])}|" \
                    f"{if_none(seps[indicator['sep_id']])}|{if_none(indicator['geometrytype']) if int(indicator['level']) > 1 else ''}|{if_none(indicator['measurement_unit'])}|" \
                    f"{if_none(list_scenario)}".replace('\r', ' ').replace('\n', ' ')
                s += "\n"
        csv_file.write(s)
    print('Feito!')


