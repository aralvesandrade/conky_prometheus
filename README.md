Executar para testar

```
python3 mysql_status.py
```

Instalar `conky`

```
sudo apt install conky-all
cp /etc/conky/conky.conf ~/.conkyrc
gedit ~/.conkyrc
```

Copiar conteúdo do arquivo `.conkyrc` e colar no arquivo editado acima `~/.conkyrc`:

Exemplo de como inserir uma linha no `conky`

```
${font sans-serif:bold:size=10}SERVICE STATUS (UPTIME-KUMA) ${hr 2}
${font sans-serif:normal:size=8}${execi 60 python3 ~/conky_prometheus/services_status.py}
```

Testar

```
killall conky && conky
```