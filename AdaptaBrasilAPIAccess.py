import urllib.request, json
import argparse

def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Programa para obter metadados da API do AdaptaBrasil.')
    parser.add_argument('--url', type=str,
                        default = 'https://sistema.adaptabrasil.mcti.gov.br/api/hierarquia',
                        help='URL para obtenção das URLs para acesso aos dados do AdaptaBrasil via API.')
    parser.add_argument('--arquivo_saida', type=str,
                        default = 'adaptaBrasilAPIEstrutura.csv',
                        help='Nome do arquivo destino (csv).')
    return parser.parse_args()

def if_none(value):
    return value if value is not None else ''

if __name__ == '__main__':
    args = get_command_line_arguments()

    with urllib.request.urlopen(args.url) as url, open(args.arquivo_saida,mode='w', encoding='utf-8') as csv_file:
        indicators = json.load(url)
        s = '\ufeff' # BOM code to preserve diacritics em Excel
        s += 'id|nome|url_mostra_mapas_na_tela|url_obtem_dados_indicador|url_obtem_totais_evolucao_tendencia|url_faz_download_geometrias_dados|' \
             'descricao_simples|descricao_completa|nivel|proporcao_direta|indicador_pai|' \
             'anos|setor_estrategico|tipo_geometria|unidade_medida|cenarios\n'
        list_scenario = []
        for indicator in indicators:
            years = indicator['years'].split(',') if indicator['years'] is not None else None
            if indicator['scenarios'][0] is not None:
                url_getmapdata = ''
                url_gettotal_evolucao_tendencia = ''
                url_download = ''
                url_show_map_on_the_site = ''
                list_scenario = []
                for scenario in indicator['scenarios']:
                    list_scenario.append(scenario)
                if indicator['years'] is not None:
                    # https://sistema.adaptabrasil.mcti.gov.br/5000/1/2015/null/BR/municipio/
                    url_show_map_on_the_site = f"https://sistema.adaptabrasil.mcti.gov.br/{indicator['id']}/1/{years[0]}/null/BR/municipio/"
                    # https://sistema.adaptabrasil.dev.apps.rnp.br/api/mapa-dados/BR/municipio/1000/2015/null
                    url_getmapdata = f"https://sistema.adaptabrasil.mcti.gov.br/api/mapa-dados/BR/municipio/" \
                                     f"{indicator['id']}/{years[0]}/null"
                    # https://sistema.adaptabrasil.mcti.gov.br/api/total/BR/municipio/5000/2/null
                    url_gettotal_evolucao_tendencia = f"https://sistema.adaptabrasil.mcti.gov.br/api/total/BR/municipio/" \
                                                      f"{indicator['id']}/null/{years[0]}"
                    # https://sistema.adaptabrasil.dev.apps.rnp.br/api/geometria/data/1000/BR/null/2015/municipio/SHPz
                    url_download = f"https://sistema.adaptabrasil.dev.apps.rnp.br/api/geometria/data/{indicator['id']}/" \
                                   f"BR/null/{years[0]}/municipio/SHPz"

                s += f"{indicator['id']}|{indicator['name']}|"
                s += f"{url_show_map_on_the_site}|{url_getmapdata}|{url_gettotal_evolucao_tendencia}|{url_download}|" \
                    f"{indicator['simple_description']}|{indicator['complete_description']}|{indicator['level']}|" \
                    f"{if_none(indicator['pessimist'])}|{if_none(indicator['indicator_id_master'])}|{if_none(indicator['years'])}|" \
                    f"{if_none(indicator['sep_description'])}|{if_none(indicator['geometrytype']) if int(indicator['level']) > 1 else ''}|{if_none(indicator['measurement_unit'])}|" \
                    f"{if_none(indicator['scenarios'])}".replace('\r', ' ').replace('\n', ' ')
                s += "\n"
        csv_file.write(s)
    print('Feito!')


