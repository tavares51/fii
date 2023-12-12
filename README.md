## Escopo
Criar um robô que colete no link => https://www.fundsexplorer.com.br/ranking <br>
Os dados dos Fundos Imobiliários para análise <br>

### Colunas
Fundo; Setor; Preço Atual; Liquidez Diária; P/VP; Último dividendo; DY; DY12(Média); Variação

### Processo
Salvar Arquivo com nome 'report_fii_{data_hora_execução}.csv' <br>
Criar Log de Erros 'log_{data_hora_execução}.csv'
<br>
csv: Pandas <br>
automação: Selenium, BeautifulSoup
