# Simple Stock Flow · Herramientas de demostración

Dos herramientas para dejar **Simple Stock Flow** presentable cuando alguien lo abre a mirar: una
dibuja las imágenes del catálogo y la otra siembra el sistema con ese catálogo.

| Guion | Qué hace |
|---|---|
| `make_pictures.py` | Dibuja las 22 láminas de `img/`, una por producto |
| `seed.py` | Siembra el sistema por la API: 22 productos con su imagen, un vendedor y 18 ventas |

**No forman parte del producto.** El sistema arranca y funciona sin ellas: las cinco categorías y
el usuario administrador existen desde el primer arranque. Esto solo sirve para que el catálogo no
se vea vacío —ni lleno de basura de pruebas— cuando se enseña.

## Para levantar el sistema no necesitas nada de esto

Conviene decirlo pronto, porque es la razón de que este repositorio exista por separado.

Levantar Simple Stock Flow es cosa de **`simple-stock-flow-infra`**, y allí basta con Docker: su README
lo dice tal cual — «ni .NET, ni Node, ni un cliente de base de datos». Estas herramientas, en cambio, piden Python, un par
de paquetes y Chrome, y son del todo opcionales. Vivían dentro de la infraestructura y le
contradecían esa promesa, así que se mudaron aquí.

## Cómo se clona

```bash
git clone https://github.com/code-dev-projects/simple-stock-flow-tools.git
cd simple-stock-flow-tools
```

## Qué necesitas instalado

| Requisito | Para qué | Lo pide |
|---|---|---|
| **Python 3** (probado con 3.11) | ejecutar los guiones | los dos |
| **requests** | hablar con la API por HTTP | `seed.py` |
| **Pillow** | recortar la rejilla en 22 láminas | `make_pictures.py` |
| **Docker** | repartir las ventas en el tiempo, vía `docker compose` | `seed.py` |
| **Google Chrome** | dibujar la rejilla en modo headless | `make_pictures.py` |

Lo demás que importan los guiones —`argparse`, `datetime`, `pathlib`, `subprocess`, `sys`,
`unicodedata`— viene con Python y no se instala.

```bash
pip install requests Pillow
```

## Sembrar el catálogo

Necesita la pila **levantada con la superposición de desarrollo**, porque habla con la API en
`http://localhost:5000`:

```bash
cd ../simple-stock-flow-infra
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --wait
```

Los ficheros de composición viven en ese repositorio, no en este: desde aquí el comando no
encuentra nada que levantar.

Después, desde este repositorio:

```bash
python seed.py
```

Lee las credenciales del administrador del `.env` de la infraestructura, y nunca las imprime. Busca
`simple-stock-flow-infra` **al lado de este repositorio**, que es lo habitual si has clonado los dos
en la misma carpeta. Si lo tienes en otro sitio, dilo:

```bash
python seed.py --infra /ruta/a/simple-stock-flow-infra
```

La ruta por omisión se calcula a partir de la ubicación del propio guion, no del directorio desde el
que lo llamas, así que funciona igual lo llames desde donde lo llames.

**Solo llena un catálogo vacío.** Si ya hay productos se detiene sin tocar nada y te imprime el
comando exacto para vaciarlo: correrlo dos veces duplicaría cada producto y el reporte contaría
doble sin que nada se quejara.

### Qué siembra

| | |
|---|---|
| Productos | **22**, repartidos en las cinco categorías, todos con imagen |
| Stock | de 4 a 300, elegido para que se vean los tres avisos de existencias |
| Ventas | **18**, de 1 a 3 líneas, repartidas en los últimos 24 días |
| Usuario | **`vendedor.demo`**, rol `seller`, con la clave de `DEMO_SELLER_PASSWORD` del `.env` |

El vendedor está para poder **ver en pantalla lo que un vendedor no puede hacer**: entra, vende y
consulta, pero no le aparece «Nuevo producto» y la API le responde 403 si lo intenta por su cuenta.

### Por qué siembra por la API y no por SQL

Todo entra por HTTP, igual que si alguien lo tecleara: un precio que rompa una invariante falla aquí
exactamente como fallaría en pantalla. Sembrar por SQL se saltaría las reglas que solo viven en el
código y dejaría datos que el propio sistema nunca habría aceptado.

**La única excepción es el instante de cada venta**, y está aislada en `spread_sales_over_time`. El
sistema sella la venta con la hora en que se registra —que es lo correcto—, así que un sistema
recién sembrado tendría las 18 ventas dentro del mismo minuto y el reporte por rango de fechas no
tendría nada que enseñar. Un `update` las reparte, cada una en su día y a una hora laboral
verosímil. Es lo único que toca la base directamente, y se hace después de que la venta ya pasó por
todas las reglas. Para eso necesita Docker: alcanza la base por `docker compose exec`.

## Dibujar las imágenes

Las 22 láminas **ya están en `img/`** y van versionadas, así que para sembrar no hace falta ejecutar
esto. Solo se vuelve a correr si cambia el catálogo.

```bash
python make_pictures.py
```

Cada producto tiene su lámina: fondo con el tinte de su categoría y un icono de línea. Chrome dibuja
las 22 en una sola rejilla y Pillow la recorta, para que haya **un** arranque de navegador en vez de
veintidós. Las láminas no llevan margen y miden lo mismo, que es lo que hace que el recorte sea
exacto y no aproximado.

Son marcadores honestos, no fotos: un catálogo real traería fotografías del proveedor.

> Busca Chrome en `C:\Program Files\Google\Chrome\Application\chrome.exe`. Fuera de Windows, o con
> Chrome instalado en otro sitio, hay que cambiar esa ruta en la constante `CHROME` del guion.

## El catálogo

Vive en `catalogue.py`, en una sola lista. El sembrador y el dibujante leen la misma, así que un
producto no puede acabar con la imagen de otro.

## Licencia

MIT. Copyright (c) 2026 Jesus Ariel Gonzalez Bonilla. El texto completo está en
[LICENSE](LICENSE).
