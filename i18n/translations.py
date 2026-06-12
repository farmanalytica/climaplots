# -*- coding: utf-8 -*-
"""Source strings + translations for the ClimaPlots UI.

Edit translations here, then run ``make_ts.py`` to (re)generate the
``ClimaPlots_<lang>.ts`` files and ``compile_translations.py`` to build the
``.qm`` binaries. English is the source language (no .qm needed). Climate
variable/index names and their descriptions are intentionally kept in English.
"""

# Every user-facing UI string wrapped with _tr("ClimaPlots", ...) in the code.
SOURCES = [
    # sidebar
    "Intro", "Coordinates", "Trends", "Thermo-pluviometric", "Indices",
    # header / page titles
    "Welcome", "Select coordinates", "Annual trends",
    "Thermo-pluviometric diagram", "Climate indices",
    "Proxy settings", "Proxy setting (only if required by your network provider)",
    "Learn more about this plugin",
    # intro
    "Get Started",
    "This is a free and open project, supported by ",
    "Get in touch for exclusive and personalized commercial solutions.",
    # coordinates page
    "Location", "Longitude", "Latitude", "Years", "to",
    "Longitude in decimal degrees (WGS84)", "Latitude in decimal degrees (WGS84)",
    "Capture a coordinate by clicking on the map canvas",
    "First year to download", "Last year to download",
    "📍  Pick a point on the map", "📍  Click the map…  (click here to cancel)",
    "Satellite layer", "Add a Google satellite basemap to help locate your point",
    "Clear marker", "Remove the point marker from the map",
    "Run analysis", "Download NASA POWER data for this point and build the charts",
    # plot toolbars
    "Variable:", "Index:", "Mean monthly precipitation and temperature",
    "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.",
    "Save daily data", "Export the full daily NASA POWER series as CSV",
    "Open in browser", "Open this chart full-screen in your web browser",
    "Save chart data", "Export the plotted annual series as CSV",
    "Export the monthly climate normals as CSV", "Export the selected index series as CSV",
    "Choose the climate variable to plot", "Choose the ETCCDI climate index to plot",
    "Back", "Go to the previous page", "Next", "Go to the next page",
    # dialogs / messages
    "Fetching climate data...", "Missing coordinates",
    "Click a point on the map (or enter Longitude/Latitude) first.",
    "Failed to fetch or process climate data.\nSee the QGIS log for details.",
    "Data not available", "Proxy Settings",
    "Enter proxy (e.g. http://[username]:[password]@host:port):",
]

TRANSLATIONS = {
    "pt": {
        "Intro": "Início", "Coordinates": "Coordenadas", "Trends": "Tendências",
        "Thermo-pluviometric": "Termopluviométrico", "Indices": "Índices",
        "Welcome": "Bem-vindo", "Select coordinates": "Selecione as coordenadas",
        "Annual trends": "Tendências anuais",
        "Thermo-pluviometric diagram": "Diagrama termopluviométrico",
        "Climate indices": "Índices climáticos",
        "Proxy settings": "Configurações de proxy",
        "Proxy setting (only if required by your network provider)": "Configuração de proxy (apenas se exigido pela sua rede)",
        "Learn more about this plugin": "Saiba mais sobre este complemento",
        "Get Started": "Começar",
        "This is a free and open project, supported by ": "Este é um projeto livre e aberto, apoiado pela ",
        "Get in touch for exclusive and personalized commercial solutions.": "Entre em contato para soluções comerciais exclusivas e personalizadas.",
        "Location": "Localização", "Longitude": "Longitude", "Latitude": "Latitude",
        "Years": "Anos", "to": "a",
        "Longitude in decimal degrees (WGS84)": "Longitude em graus decimais (WGS84)",
        "Latitude in decimal degrees (WGS84)": "Latitude em graus decimais (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "Capture uma coordenada clicando no mapa",
        "First year to download": "Primeiro ano a baixar",
        "Last year to download": "Último ano a baixar",
        "📍  Pick a point on the map": "📍  Escolha um ponto no mapa",
        "📍  Click the map…  (click here to cancel)": "📍  Clique no mapa…  (clique aqui para cancelar)",
        "Satellite layer": "Camada de satélite",
        "Add a Google satellite basemap to help locate your point": "Adiciona um mapa base de satélite do Google para ajudar a localizar o ponto",
        "Clear marker": "Remover marcador",
        "Remove the point marker from the map": "Remove o marcador do ponto do mapa",
        "Run analysis": "Executar análise",
        "Download NASA POWER data for this point and build the charts": "Baixa os dados do NASA POWER para este ponto e gera os gráficos",
        "Variable:": "Variável:", "Index:": "Índice:",
        "Mean monthly precipitation and temperature": "Precipitação e temperatura médias mensais",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "Precipitação média mensal (barras) e temperaturas médias (linhas) ao longo do ano.",
        "Save daily data": "Salvar dados diários",
        "Export the full daily NASA POWER series as CSV": "Exporta a série diária completa do NASA POWER em CSV",
        "Open in browser": "Abrir no navegador",
        "Open this chart full-screen in your web browser": "Abre este gráfico em tela cheia no navegador",
        "Save chart data": "Salvar dados do gráfico",
        "Export the plotted annual series as CSV": "Exporta a série anual plotada em CSV",
        "Export the monthly climate normals as CSV": "Exporta as normais climáticas mensais em CSV",
        "Export the selected index series as CSV": "Exporta a série do índice selecionado em CSV",
        "Choose the climate variable to plot": "Escolha a variável climática a plotar",
        "Choose the ETCCDI climate index to plot": "Escolha o índice climático ETCCDI a plotar",
        "Back": "Voltar", "Go to the previous page": "Ir para a página anterior",
        "Next": "Avançar", "Go to the next page": "Ir para a próxima página",
        "Fetching climate data...": "Baixando dados climáticos...",
        "Missing coordinates": "Coordenadas ausentes",
        "Click a point on the map (or enter Longitude/Latitude) first.": "Clique em um ponto no mapa (ou digite Longitude/Latitude) primeiro.",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "Falha ao baixar ou processar os dados climáticos.\nVeja o log do QGIS para detalhes.",
        "Data not available": "Dados não disponíveis",
        "Proxy Settings": "Configurações de Proxy",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "Digite o proxy (ex.: http://[usuario]:[senha]@host:porta):",
    },
    "es": {
        "Intro": "Inicio", "Coordinates": "Coordenadas", "Trends": "Tendencias",
        "Thermo-pluviometric": "Termopluviométrico", "Indices": "Índices",
        "Welcome": "Bienvenido", "Select coordinates": "Seleccione las coordenadas",
        "Annual trends": "Tendencias anuales",
        "Thermo-pluviometric diagram": "Diagrama termopluviométrico",
        "Climate indices": "Índices climáticos",
        "Proxy settings": "Configuración de proxy",
        "Proxy setting (only if required by your network provider)": "Configuración de proxy (solo si lo exige su red)",
        "Learn more about this plugin": "Más información sobre este complemento",
        "Get Started": "Comenzar",
        "This is a free and open project, supported by ": "Este es un proyecto libre y abierto, apoyado por ",
        "Get in touch for exclusive and personalized commercial solutions.": "Contáctenos para soluciones comerciales exclusivas y personalizadas.",
        "Location": "Ubicación", "Longitude": "Longitud", "Latitude": "Latitud",
        "Years": "Años", "to": "a",
        "Longitude in decimal degrees (WGS84)": "Longitud en grados decimales (WGS84)",
        "Latitude in decimal degrees (WGS84)": "Latitud en grados decimales (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "Capture una coordenada haciendo clic en el mapa",
        "First year to download": "Primer año a descargar",
        "Last year to download": "Último año a descargar",
        "📍  Pick a point on the map": "📍  Elija un punto en el mapa",
        "📍  Click the map…  (click here to cancel)": "📍  Haga clic en el mapa…  (haga clic aquí para cancelar)",
        "Satellite layer": "Capa de satélite",
        "Add a Google satellite basemap to help locate your point": "Agrega un mapa base de satélite de Google para ayudar a ubicar el punto",
        "Clear marker": "Quitar marcador",
        "Remove the point marker from the map": "Quita el marcador del punto del mapa",
        "Run analysis": "Ejecutar análisis",
        "Download NASA POWER data for this point and build the charts": "Descarga los datos de NASA POWER para este punto y crea los gráficos",
        "Variable:": "Variable:", "Index:": "Índice:",
        "Mean monthly precipitation and temperature": "Precipitación y temperatura medias mensuales",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "Precipitación media mensual (barras) y temperaturas medias (líneas) a lo largo del año.",
        "Save daily data": "Guardar datos diarios",
        "Export the full daily NASA POWER series as CSV": "Exporta la serie diaria completa de NASA POWER en CSV",
        "Open in browser": "Abrir en el navegador",
        "Open this chart full-screen in your web browser": "Abre este gráfico a pantalla completa en el navegador",
        "Save chart data": "Guardar datos del gráfico",
        "Export the plotted annual series as CSV": "Exporta la serie anual graficada en CSV",
        "Export the monthly climate normals as CSV": "Exporta las normales climáticas mensuales en CSV",
        "Export the selected index series as CSV": "Exporta la serie del índice seleccionado en CSV",
        "Choose the climate variable to plot": "Elija la variable climática a graficar",
        "Choose the ETCCDI climate index to plot": "Elija el índice climático ETCCDI a graficar",
        "Back": "Atrás", "Go to the previous page": "Ir a la página anterior",
        "Next": "Siguiente", "Go to the next page": "Ir a la página siguiente",
        "Fetching climate data...": "Descargando datos climáticos...",
        "Missing coordinates": "Faltan coordenadas",
        "Click a point on the map (or enter Longitude/Latitude) first.": "Primero haga clic en un punto del mapa (o ingrese Longitud/Latitud).",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "Error al descargar o procesar los datos climáticos.\nConsulte el registro de QGIS para más detalles.",
        "Data not available": "Datos no disponibles",
        "Proxy Settings": "Configuración de Proxy",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "Ingrese el proxy (ej.: http://[usuario]:[clave]@host:puerto):",
    },
    "fr": {
        "Intro": "Accueil", "Coordinates": "Coordonnées", "Trends": "Tendances",
        "Thermo-pluviometric": "Thermo-pluviométrique", "Indices": "Indices",
        "Welcome": "Bienvenue", "Select coordinates": "Sélectionnez les coordonnées",
        "Annual trends": "Tendances annuelles",
        "Thermo-pluviometric diagram": "Diagramme thermo-pluviométrique",
        "Climate indices": "Indices climatiques",
        "Proxy settings": "Paramètres du proxy",
        "Proxy setting (only if required by your network provider)": "Paramètre de proxy (uniquement si requis par votre réseau)",
        "Learn more about this plugin": "En savoir plus sur ce module",
        "Get Started": "Commencer",
        "This is a free and open project, supported by ": "Ceci est un projet libre et ouvert, soutenu par ",
        "Get in touch for exclusive and personalized commercial solutions.": "Contactez-nous pour des solutions commerciales exclusives et personnalisées.",
        "Location": "Localisation", "Longitude": "Longitude", "Latitude": "Latitude",
        "Years": "Années", "to": "à",
        "Longitude in decimal degrees (WGS84)": "Longitude en degrés décimaux (WGS84)",
        "Latitude in decimal degrees (WGS84)": "Latitude en degrés décimaux (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "Capturez une coordonnée en cliquant sur la carte",
        "First year to download": "Première année à télécharger",
        "Last year to download": "Dernière année à télécharger",
        "📍  Pick a point on the map": "📍  Choisissez un point sur la carte",
        "📍  Click the map…  (click here to cancel)": "📍  Cliquez sur la carte…  (cliquez ici pour annuler)",
        "Satellite layer": "Couche satellite",
        "Add a Google satellite basemap to help locate your point": "Ajoute un fond de carte satellite Google pour localiser le point",
        "Clear marker": "Effacer le repère",
        "Remove the point marker from the map": "Supprime le repère du point sur la carte",
        "Run analysis": "Lancer l'analyse",
        "Download NASA POWER data for this point and build the charts": "Télécharge les données NASA POWER pour ce point et crée les graphiques",
        "Variable:": "Variable :", "Index:": "Indice :",
        "Mean monthly precipitation and temperature": "Précipitations et températures moyennes mensuelles",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "Précipitations mensuelles moyennes (barres) et températures moyennes (lignes) sur l'année.",
        "Save daily data": "Enregistrer les données quotidiennes",
        "Export the full daily NASA POWER series as CSV": "Exporte la série quotidienne complète NASA POWER en CSV",
        "Open in browser": "Ouvrir dans le navigateur",
        "Open this chart full-screen in your web browser": "Ouvre ce graphique en plein écran dans le navigateur",
        "Save chart data": "Enregistrer les données du graphique",
        "Export the plotted annual series as CSV": "Exporte la série annuelle tracée en CSV",
        "Export the monthly climate normals as CSV": "Exporte les normales climatiques mensuelles en CSV",
        "Export the selected index series as CSV": "Exporte la série de l'indice sélectionné en CSV",
        "Choose the climate variable to plot": "Choisissez la variable climatique à tracer",
        "Choose the ETCCDI climate index to plot": "Choisissez l'indice climatique ETCCDI à tracer",
        "Back": "Retour", "Go to the previous page": "Aller à la page précédente",
        "Next": "Suivant", "Go to the next page": "Aller à la page suivante",
        "Fetching climate data...": "Téléchargement des données climatiques...",
        "Missing coordinates": "Coordonnées manquantes",
        "Click a point on the map (or enter Longitude/Latitude) first.": "Cliquez d'abord sur un point de la carte (ou saisissez Longitude/Latitude).",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "Échec du téléchargement ou du traitement des données climatiques.\nConsultez le journal QGIS pour plus de détails.",
        "Data not available": "Données non disponibles",
        "Proxy Settings": "Paramètres du proxy",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "Saisissez le proxy (ex. : http://[utilisateur]:[motdepasse]@hôte:port) :",
    },
    "it": {
        "Intro": "Introduzione", "Coordinates": "Coordinate", "Trends": "Tendenze",
        "Thermo-pluviometric": "Termopluviometrico", "Indices": "Indici",
        "Welcome": "Benvenuto", "Select coordinates": "Seleziona le coordinate",
        "Annual trends": "Tendenze annuali",
        "Thermo-pluviometric diagram": "Diagramma termopluviometrico",
        "Climate indices": "Indici climatici",
        "Proxy settings": "Impostazioni proxy",
        "Proxy setting (only if required by your network provider)": "Impostazione proxy (solo se richiesto dalla tua rete)",
        "Learn more about this plugin": "Scopri di più su questo plugin",
        "Get Started": "Inizia",
        "This is a free and open project, supported by ": "Questo è un progetto libero e aperto, supportato da ",
        "Get in touch for exclusive and personalized commercial solutions.": "Contattaci per soluzioni commerciali esclusive e personalizzate.",
        "Location": "Posizione", "Longitude": "Longitudine", "Latitude": "Latitudine",
        "Years": "Anni", "to": "a",
        "Longitude in decimal degrees (WGS84)": "Longitudine in gradi decimali (WGS84)",
        "Latitude in decimal degrees (WGS84)": "Latitudine in gradi decimali (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "Cattura una coordinata cliccando sulla mappa",
        "First year to download": "Primo anno da scaricare",
        "Last year to download": "Ultimo anno da scaricare",
        "📍  Pick a point on the map": "📍  Scegli un punto sulla mappa",
        "📍  Click the map…  (click here to cancel)": "📍  Clicca sulla mappa…  (clicca qui per annullare)",
        "Satellite layer": "Livello satellitare",
        "Add a Google satellite basemap to help locate your point": "Aggiunge una mappa base satellitare di Google per localizzare il punto",
        "Clear marker": "Rimuovi marcatore",
        "Remove the point marker from the map": "Rimuove il marcatore del punto dalla mappa",
        "Run analysis": "Esegui analisi",
        "Download NASA POWER data for this point and build the charts": "Scarica i dati NASA POWER per questo punto e crea i grafici",
        "Variable:": "Variabile:", "Index:": "Indice:",
        "Mean monthly precipitation and temperature": "Precipitazioni e temperature medie mensili",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "Precipitazioni medie mensili (barre) e temperature medie (linee) durante l'anno.",
        "Save daily data": "Salva dati giornalieri",
        "Export the full daily NASA POWER series as CSV": "Esporta la serie giornaliera completa NASA POWER in CSV",
        "Open in browser": "Apri nel browser",
        "Open this chart full-screen in your web browser": "Apre questo grafico a schermo intero nel browser",
        "Save chart data": "Salva dati del grafico",
        "Export the plotted annual series as CSV": "Esporta la serie annuale tracciata in CSV",
        "Export the monthly climate normals as CSV": "Esporta le normali climatiche mensili in CSV",
        "Export the selected index series as CSV": "Esporta la serie dell'indice selezionato in CSV",
        "Choose the climate variable to plot": "Scegli la variabile climatica da tracciare",
        "Choose the ETCCDI climate index to plot": "Scegli l'indice climatico ETCCDI da tracciare",
        "Back": "Indietro", "Go to the previous page": "Vai alla pagina precedente",
        "Next": "Avanti", "Go to the next page": "Vai alla pagina successiva",
        "Fetching climate data...": "Download dei dati climatici...",
        "Missing coordinates": "Coordinate mancanti",
        "Click a point on the map (or enter Longitude/Latitude) first.": "Clicca prima un punto sulla mappa (o inserisci Longitudine/Latitudine).",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "Impossibile scaricare o elaborare i dati climatici.\nConsulta il log di QGIS per i dettagli.",
        "Data not available": "Dati non disponibili",
        "Proxy Settings": "Impostazioni Proxy",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "Inserisci il proxy (es.: http://[utente]:[password]@host:porta):",
    },
    "hi": {
        "Intro": "परिचय", "Coordinates": "निर्देशांक", "Trends": "रुझान",
        "Thermo-pluviometric": "ताप-वर्षामापी", "Indices": "सूचकांक",
        "Welcome": "स्वागत है", "Select coordinates": "निर्देशांक चुनें",
        "Annual trends": "वार्षिक रुझान",
        "Thermo-pluviometric diagram": "ताप-वर्षामापी आरेख",
        "Climate indices": "जलवायु सूचकांक",
        "Proxy settings": "प्रॉक्सी सेटिंग्स",
        "Proxy setting (only if required by your network provider)": "प्रॉक्सी सेटिंग (केवल यदि आपके नेटवर्क के लिए आवश्यक हो)",
        "Learn more about this plugin": "इस प्लगइन के बारे में और जानें",
        "Get Started": "शुरू करें",
        "This is a free and open project, supported by ": "यह एक मुफ़्त और खुला प्रोजेक्ट है, समर्थित ",
        "Get in touch for exclusive and personalized commercial solutions.": "विशेष और व्यक्तिगत व्यावसायिक समाधानों के लिए संपर्क करें।",
        "Location": "स्थान", "Longitude": "देशांतर", "Latitude": "अक्षांश",
        "Years": "वर्ष", "to": "से",
        "Longitude in decimal degrees (WGS84)": "दशमलव डिग्री में देशांतर (WGS84)",
        "Latitude in decimal degrees (WGS84)": "दशमलव डिग्री में अक्षांश (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "मानचित्र पर क्लिक करके निर्देशांक चुनें",
        "First year to download": "डाउनलोड करने का पहला वर्ष",
        "Last year to download": "डाउनलोड करने का अंतिम वर्ष",
        "📍  Pick a point on the map": "📍  मानचित्र पर एक बिंदु चुनें",
        "📍  Click the map…  (click here to cancel)": "📍  मानचित्र पर क्लिक करें…  (रद्द करने के लिए यहाँ क्लिक करें)",
        "Satellite layer": "उपग्रह परत",
        "Add a Google satellite basemap to help locate your point": "बिंदु खोजने में मदद के लिए Google उपग्रह आधार मानचित्र जोड़ें",
        "Clear marker": "मार्कर हटाएँ",
        "Remove the point marker from the map": "मानचित्र से बिंदु मार्कर हटाएँ",
        "Run analysis": "विश्लेषण चलाएँ",
        "Download NASA POWER data for this point and build the charts": "इस बिंदु के लिए NASA POWER डेटा डाउनलोड करें और चार्ट बनाएँ",
        "Variable:": "चर:", "Index:": "सूचकांक:",
        "Mean monthly precipitation and temperature": "मासिक औसत वर्षा और तापमान",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "वर्ष भर मासिक औसत वर्षा (बार) और औसत तापमान (रेखाएँ)।",
        "Save daily data": "दैनिक डेटा सहेजें",
        "Export the full daily NASA POWER series as CSV": "पूर्ण दैनिक NASA POWER श्रृंखला को CSV में निर्यात करें",
        "Open in browser": "ब्राउज़र में खोलें",
        "Open this chart full-screen in your web browser": "इस चार्ट को ब्राउज़र में पूर्ण-स्क्रीन खोलें",
        "Save chart data": "चार्ट डेटा सहेजें",
        "Export the plotted annual series as CSV": "प्लॉट की गई वार्षिक श्रृंखला को CSV में निर्यात करें",
        "Export the monthly climate normals as CSV": "मासिक जलवायु सामान्य को CSV में निर्यात करें",
        "Export the selected index series as CSV": "चयनित सूचकांक श्रृंखला को CSV में निर्यात करें",
        "Choose the climate variable to plot": "प्लॉट करने के लिए जलवायु चर चुनें",
        "Choose the ETCCDI climate index to plot": "प्लॉट करने के लिए ETCCDI जलवायु सूचकांक चुनें",
        "Back": "पीछे", "Go to the previous page": "पिछले पृष्ठ पर जाएँ",
        "Next": "आगे", "Go to the next page": "अगले पृष्ठ पर जाएँ",
        "Fetching climate data...": "जलवायु डेटा प्राप्त किया जा रहा है...",
        "Missing coordinates": "निर्देशांक अनुपस्थित",
        "Click a point on the map (or enter Longitude/Latitude) first.": "पहले मानचित्र पर एक बिंदु क्लिक करें (या देशांतर/अक्षांश दर्ज करें)।",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "जलवायु डेटा प्राप्त या संसाधित करने में विफल।\nविवरण के लिए QGIS लॉग देखें।",
        "Data not available": "डेटा उपलब्ध नहीं",
        "Proxy Settings": "प्रॉक्सी सेटिंग्स",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "प्रॉक्सी दर्ज करें (उदा.: http://[username]:[password]@host:port):",
    },
    "zh": {
        "Intro": "简介", "Coordinates": "坐标", "Trends": "趋势",
        "Thermo-pluviometric": "温雨图", "Indices": "指数",
        "Welcome": "欢迎", "Select coordinates": "选择坐标",
        "Annual trends": "年度趋势",
        "Thermo-pluviometric diagram": "温雨图",
        "Climate indices": "气候指数",
        "Proxy settings": "代理设置",
        "Proxy setting (only if required by your network provider)": "代理设置（仅在您的网络需要时）",
        "Learn more about this plugin": "了解有关此插件的更多信息",
        "Get Started": "开始使用",
        "This is a free and open project, supported by ": "这是一个免费开放的项目，由以下机构支持：",
        "Get in touch for exclusive and personalized commercial solutions.": "联系我们获取专属定制的商业解决方案。",
        "Location": "位置", "Longitude": "经度", "Latitude": "纬度",
        "Years": "年份", "to": "至",
        "Longitude in decimal degrees (WGS84)": "十进制度的经度 (WGS84)",
        "Latitude in decimal degrees (WGS84)": "十进制度的纬度 (WGS84)",
        "Capture a coordinate by clicking on the map canvas": "在地图上点击以获取坐标",
        "First year to download": "下载的起始年份",
        "Last year to download": "下载的结束年份",
        "📍  Pick a point on the map": "📍  在地图上选择一个点",
        "📍  Click the map…  (click here to cancel)": "📍  点击地图…（点击此处取消）",
        "Satellite layer": "卫星图层",
        "Add a Google satellite basemap to help locate your point": "添加 Google 卫星底图以帮助定位您的点",
        "Clear marker": "清除标记",
        "Remove the point marker from the map": "从地图上移除点标记",
        "Run analysis": "运行分析",
        "Download NASA POWER data for this point and build the charts": "下载该点的 NASA POWER 数据并生成图表",
        "Variable:": "变量：", "Index:": "指数：",
        "Mean monthly precipitation and temperature": "月平均降水量和温度",
        "Mean monthly precipitation (bars) and mean temperatures (lines) across the year.": "全年月平均降水量（柱状）和平均温度（折线）。",
        "Save daily data": "保存每日数据",
        "Export the full daily NASA POWER series as CSV": "将完整的每日 NASA POWER 序列导出为 CSV",
        "Open in browser": "在浏览器中打开",
        "Open this chart full-screen in your web browser": "在浏览器中全屏打开此图表",
        "Save chart data": "保存图表数据",
        "Export the plotted annual series as CSV": "将绘制的年度序列导出为 CSV",
        "Export the monthly climate normals as CSV": "将月度气候平均值导出为 CSV",
        "Export the selected index series as CSV": "将所选指数序列导出为 CSV",
        "Choose the climate variable to plot": "选择要绘制的气候变量",
        "Choose the ETCCDI climate index to plot": "选择要绘制的 ETCCDI 气候指数",
        "Back": "上一步", "Go to the previous page": "转到上一页",
        "Next": "下一步", "Go to the next page": "转到下一页",
        "Fetching climate data...": "正在获取气候数据...",
        "Missing coordinates": "缺少坐标",
        "Click a point on the map (or enter Longitude/Latitude) first.": "请先在地图上点击一个点（或输入经度/纬度）。",
        "Failed to fetch or process climate data.\nSee the QGIS log for details.": "获取或处理气候数据失败。\n详情请查看 QGIS 日志。",
        "Data not available": "数据不可用",
        "Proxy Settings": "代理设置",
        "Enter proxy (e.g. http://[username]:[password]@host:port):": "输入代理（例如：http://[username]:[password]@host:port）：",
    },
}


# --- Appended: export / image strings (feature batch 2) ----------------------
SOURCES += [
    "Image", "Save the chart as a PNG image", "Save image",
    "Export all", "Export every table to one Excel file",
    "Run an analysis first.", "Saved:", "Export failed.",
]

_EXTRA = {
    "pt": {
        "Image": "Imagem", "Save the chart as a PNG image": "Salvar o gráfico como imagem PNG",
        "Save image": "Salvar imagem", "Export all": "Exportar tudo",
        "Export every table to one Excel file": "Exporta todas as tabelas em um arquivo Excel",
        "Run an analysis first.": "Execute uma análise primeiro.",
        "Saved:": "Salvo:", "Export failed.": "Falha na exportação.",
    },
    "es": {
        "Image": "Imagen", "Save the chart as a PNG image": "Guardar el gráfico como imagen PNG",
        "Save image": "Guardar imagen", "Export all": "Exportar todo",
        "Export every table to one Excel file": "Exporta todas las tablas en un archivo Excel",
        "Run an analysis first.": "Ejecute un análisis primero.",
        "Saved:": "Guardado:", "Export failed.": "Error en la exportación.",
    },
    "fr": {
        "Image": "Image", "Save the chart as a PNG image": "Enregistrer le graphique en image PNG",
        "Save image": "Enregistrer l'image", "Export all": "Tout exporter",
        "Export every table to one Excel file": "Exporte toutes les tables dans un fichier Excel",
        "Run an analysis first.": "Lancez d'abord une analyse.",
        "Saved:": "Enregistré :", "Export failed.": "Échec de l'export.",
    },
    "it": {
        "Image": "Immagine", "Save the chart as a PNG image": "Salva il grafico come immagine PNG",
        "Save image": "Salva immagine", "Export all": "Esporta tutto",
        "Export every table to one Excel file": "Esporta tutte le tabelle in un file Excel",
        "Run an analysis first.": "Esegui prima un'analisi.",
        "Saved:": "Salvato:", "Export failed.": "Esportazione non riuscita.",
    },
    "hi": {
        "Image": "छवि", "Save the chart as a PNG image": "चार्ट को PNG छवि के रूप में सहेजें",
        "Save image": "छवि सहेजें", "Export all": "सब निर्यात करें",
        "Export every table to one Excel file": "सभी तालिकाओं को एक Excel फ़ाइल में निर्यात करें",
        "Run an analysis first.": "पहले एक विश्लेषण चलाएँ।",
        "Saved:": "सहेजा गया:", "Export failed.": "निर्यात विफल।",
    },
    "zh": {
        "Image": "图像", "Save the chart as a PNG image": "将图表保存为 PNG 图像",
        "Save image": "保存图像", "Export all": "全部导出",
        "Export every table to one Excel file": "将所有表格导出到一个 Excel 文件",
        "Run an analysis first.": "请先运行分析。",
        "Saved:": "已保存：", "Export failed.": "导出失败。",
    },
}
for _l, _d in _EXTRA.items():
    TRANSLATIONS[_l].update(_d)


# --- Appended: comparison-point strings (feature batch 3) --------------------
SOURCES += [
    "Comparison point B (optional)", "Leave empty for a single-point analysis",
    "📍  Pick comparison point B", "📍  Click the map for B…  (click here to cancel)",
]

_EXTRA_B = {
    "pt": {
        "Comparison point B (optional)": "Ponto de comparação B (opcional)",
        "Leave empty for a single-point analysis": "Deixe vazio para análise de um único ponto",
        "📍  Pick comparison point B": "📍  Escolher ponto de comparação B",
        "📍  Click the map for B…  (click here to cancel)": "📍  Clique no mapa para B…  (clique aqui para cancelar)",
    },
    "es": {
        "Comparison point B (optional)": "Punto de comparación B (opcional)",
        "Leave empty for a single-point analysis": "Déjelo vacío para un análisis de un solo punto",
        "📍  Pick comparison point B": "📍  Elegir punto de comparación B",
        "📍  Click the map for B…  (click here to cancel)": "📍  Haga clic en el mapa para B…  (haga clic aquí para cancelar)",
    },
    "fr": {
        "Comparison point B (optional)": "Point de comparaison B (facultatif)",
        "Leave empty for a single-point analysis": "Laissez vide pour une analyse à point unique",
        "📍  Pick comparison point B": "📍  Choisir le point de comparaison B",
        "📍  Click the map for B…  (click here to cancel)": "📍  Cliquez sur la carte pour B…  (cliquez ici pour annuler)",
    },
    "it": {
        "Comparison point B (optional)": "Punto di confronto B (opzionale)",
        "Leave empty for a single-point analysis": "Lascia vuoto per un'analisi a punto singolo",
        "📍  Pick comparison point B": "📍  Scegli il punto di confronto B",
        "📍  Click the map for B…  (click here to cancel)": "📍  Clicca sulla mappa per B…  (clicca qui per annullare)",
    },
    "hi": {
        "Comparison point B (optional)": "तुलना बिंदु B (वैकल्पिक)",
        "Leave empty for a single-point analysis": "एकल-बिंदु विश्लेषण के लिए खाली छोड़ें",
        "📍  Pick comparison point B": "📍  तुलना बिंदु B चुनें",
        "📍  Click the map for B…  (click here to cancel)": "📍  B के लिए मानचित्र पर क्लिक करें…  (रद्द करने के लिए यहाँ क्लिक करें)",
    },
    "zh": {
        "Comparison point B (optional)": "对比点 B（可选）",
        "Leave empty for a single-point analysis": "留空则进行单点分析",
        "📍  Pick comparison point B": "📍  选择对比点 B",
        "📍  Click the map for B…  (click here to cancel)": "📍  点击地图选择 B…（点击此处取消）",
    },
}
for _l, _d in _EXTRA_B.items():
    TRANSLATIONS[_l].update(_d)


# --- Appended: data-source strings (Open-Meteo) ------------------------------
SOURCES += ["Data source", "Climate data provider"]
for _l, _v in {
    "pt": ("Fonte de dados", "Provedor de dados climáticos"),
    "es": ("Fuente de datos", "Proveedor de datos climáticos"),
    "fr": ("Source de données", "Fournisseur de données climatiques"),
    "it": ("Fonte dati", "Fornitore di dati climatici"),
    "hi": ("डेटा स्रोत", "जलवायु डेटा प्रदाता"),
    "zh": ("数据源", "气候数据提供方"),
}.items():
    TRANSLATIONS[_l].update({"Data source": _v[0], "Climate data provider": _v[1]})


# --- Appended: per-B source strings ------------------------------------------
SOURCES += ["(same source as A)", "Data source for the comparison point", "Source"]
for _l, _v in {
    "pt": ("(mesma fonte de A)", "Fonte de dados do ponto de comparação", "Fonte"),
    "es": ("(misma fuente que A)", "Fuente de datos del punto de comparación", "Fuente"),
    "fr": ("(même source que A)", "Source de données du point de comparaison", "Source"),
    "it": ("(stessa fonte di A)", "Fonte dati del punto di confronto", "Fonte"),
    "hi": ("(A के समान स्रोत)", "तुलना बिंदु के लिए डेटा स्रोत", "स्रोत"),
    "zh": ("（与 A 相同来源）", "对比点的数据源", "来源"),
}.items():
    TRANSLATIONS[_l].update({"(same source as A)": _v[0],
                             "Data source for the comparison point": _v[1], "Source": _v[2]})


# --- Appended: loading-placeholder coordinate labels --------------------------
SOURCES += ["Point A", "Point B"]
for _l, _v in {
    "pt": ("Ponto A", "Ponto B"),
    "es": ("Punto A", "Punto B"),
    "fr": ("Point A", "Point B"),
    "it": ("Punto A", "Punto B"),
    "hi": ("बिंदु A", "बिंदु B"),
    "zh": ("点 A", "点 B"),
}.items():
    TRANSLATIONS[_l].update({"Point A": _v[0], "Point B": _v[1]})


# --- Intro page HTML body (per language) -------------------------------------
# Used by view/pages.py to build the intro webview content dynamically so that
# the intro page respects the user's QGIS locale, not just the widget strings.
INTRO_BODY = {
    "en": """
  <h1>ClimaPlots</h1>
  <p class="sub">Climate analysis from NASA POWER and Open-Meteo (ERA5), inside QGIS.</p>
  <p>ClimaPlots fetches decades of daily climate data for any point on the map
     and turns it into interactive charts &mdash; no coding required. Choose
     between two data sources: <b>NASA POWER</b> (from 1981) and
     <b>Open-Meteo (ERA5)</b> (from 1940).</p>
  <h2>What it produces</h2>
  <p><b>Annual trends</b> for temperature, precipitation, relative humidity,
     irradiation, wind speed, reference ET&#8320; and growing degree days, each
     annotated with <b>Mann&ndash;Kendall</b> trend and <b>Pettitt</b>
     homogeneity tests.</p>
  <p><b>Thermo-pluviometric diagram</b> &mdash; the mean monthly precipitation
     and temperature regime of the location.</p>
  <p><b>Climate indices</b> &mdash; ETCCDI temperature and precipitation indices
     plus the Standardized Precipitation Index (SPI).</p>
  <h2>Compare two locations or two sources</h2>
  <p>Add an optional <b>comparison point B</b> to overlay a second series on the
     Trends chart, with trend statistics reported for both points. B can use its
     own data source, so the <i>same</i> location can be compared across NASA
     POWER and Open-Meteo &mdash; use <b>Same location as A</b> to copy point A's
     coordinates without re-clicking the map.</p>
  <h2>Quick start</h2>
  <ol>
    <li>Open the <b>Coordinates</b> page and pick a <b>data source</b>.</li>
    <li>Click <b>Pick point on map</b> and click a location on the canvas
        (or type the longitude/latitude manually).</li>
    <li>Optionally set a <b>comparison point B</b> &mdash; pick it on the map,
        or press <b>Same location as A</b>.</li>
    <li>Press <b>Run Analysis</b> and wait while the data is downloaded.</li>
    <li>Browse the <b>Trends</b>, <b>Thermo-pluviometric</b> and
        <b>Indices</b> pages. Use <b>Open in the browser</b> for a full-screen
        chart, or <b>Save data</b> to export a CSV.</li>
  </ol>
  <p>Behind a corporate network? Set a proxy via <b>Proxy settings</b> in the
     top-right corner.</p>
  <div class="cite">
    <b>Citation</b> &mdash; publications that use this plugin must cite:<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "pt": """
  <h1>ClimaPlots</h1>
  <p class="sub">Análise climática com NASA POWER e Open-Meteo (ERA5), dentro do QGIS.</p>
  <p>O ClimaPlots baixa décadas de dados climáticos diários para qualquer ponto do
     mapa e os transforma em gráficos interativos &mdash; sem necessidade de
     programação. Escolha entre duas fontes de dados: <b>NASA POWER</b> (a partir
     de 1981) e <b>Open-Meteo (ERA5)</b> (a partir de 1940).</p>
  <h2>O que ele produz</h2>
  <p><b>Tendências anuais</b> de temperatura, precipitação, umidade relativa,
     irradiação, velocidade do vento, ET&#8320; de referência e graus-dia de
     crescimento, cada uma anotada com o teste de tendência <b>Mann&ndash;Kendall</b>
     e o teste de homogeneidade <b>Pettitt</b>.</p>
  <p><b>Diagrama termopluviométrico</b> &mdash; o regime mensal médio de precipitação
     e temperatura do local.</p>
  <p><b>Índices climáticos</b> &mdash; índices de temperatura e precipitação ETCCDI
     mais o Índice de Precipitação Padronizado (SPI).</p>
  <h2>Comparar dois locais ou duas fontes</h2>
  <p>Adicione um <b>ponto de comparação B</b> opcional para sobrepor uma segunda
     série no gráfico de Tendências, com estatísticas de tendência reportadas para
     ambos os pontos. B pode usar sua própria fonte de dados, portanto o <i>mesmo</i>
     local pode ser comparado entre NASA POWER e Open-Meteo &mdash; use
     <b>Mesma localização de A</b> para copiar as coordenadas do ponto A sem precisar
     clicar novamente no mapa.</p>
  <h2>Início rápido</h2>
  <ol>
    <li>Abra a página <b>Coordenadas</b> e escolha uma <b>fonte de dados</b>.</li>
    <li>Clique em <b>Escolha um ponto no mapa</b> e clique em um local no mapa
        (ou digite longitude/latitude manualmente).</li>
    <li>Opcionalmente, defina um <b>ponto de comparação B</b> &mdash; escolha-o
        no mapa ou pressione <b>Mesma localização de A</b>.</li>
    <li>Pressione <b>Executar análise</b> e aguarde enquanto os dados são baixados.</li>
    <li>Navegue pelas páginas <b>Tendências</b>, <b>Termopluviométrico</b> e
        <b>Índices</b>. Use <b>Abrir no navegador</b> para um gráfico em tela cheia,
        ou <b>Salvar dados</b> para exportar um CSV.</li>
  </ol>
  <p>Atrás de um proxy corporativo? Configure-o via <b>Configurações de proxy</b>
     no canto superior direito.</p>
  <div class="cite">
    <b>Citação</b> &mdash; publicações que utilizam este complemento devem citar:<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "es": """
  <h1>ClimaPlots</h1>
  <p class="sub">Análisis climático con NASA POWER y Open-Meteo (ERA5), dentro de QGIS.</p>
  <p>ClimaPlots descarga décadas de datos climáticos diarios para cualquier punto del
     mapa y los convierte en gráficos interactivos &mdash; sin necesidad de programación.
     Elija entre dos fuentes de datos: <b>NASA POWER</b> (desde 1981) y
     <b>Open-Meteo (ERA5)</b> (desde 1940).</p>
  <h2>Qué produce</h2>
  <p><b>Tendencias anuales</b> de temperatura, precipitación, humedad relativa,
     irradiación, velocidad del viento, ET&#8320; de referencia y grados-día de
     crecimiento, cada una anotada con el test de tendencia <b>Mann&ndash;Kendall</b>
     y el test de homogeneidad <b>Pettitt</b>.</p>
  <p><b>Diagrama termopluviométrico</b> &mdash; el régimen mensual medio de
     precipitación y temperatura del lugar.</p>
  <p><b>Índices climáticos</b> &mdash; índices de temperatura y precipitación ETCCDI
     más el Índice de Precipitación Estandarizado (SPI).</p>
  <h2>Comparar dos lugares o dos fuentes</h2>
  <p>Agregue un <b>punto de comparación B</b> opcional para superponer una segunda
     serie en el gráfico de Tendencias, con estadísticas de tendencia reportadas para
     ambos puntos. B puede usar su propia fuente de datos, por lo que la <i>misma</i>
     ubicación puede compararse entre NASA POWER y Open-Meteo &mdash; use
     <b>Misma ubicación que A</b> para copiar las coordenadas del punto A sin hacer
     clic de nuevo en el mapa.</p>
  <h2>Inicio rápido</h2>
  <ol>
    <li>Abra la página <b>Coordenadas</b> y seleccione una <b>fuente de datos</b>.</li>
    <li>Haga clic en <b>Elegir un punto en el mapa</b> y haga clic en un lugar
        (o escriba la longitud/latitud manualmente).</li>
    <li>Opcionalmente, defina un <b>punto de comparación B</b> &mdash; elíjalo en
        el mapa o presione <b>Misma ubicación que A</b>.</li>
    <li>Presione <b>Ejecutar análisis</b> y espere mientras se descargan los datos.</li>
    <li>Navegue por las páginas <b>Tendencias</b>, <b>Termopluviométrico</b> e
        <b>Índices</b>. Use <b>Abrir en el navegador</b> para un gráfico a pantalla
        completa, o <b>Guardar datos</b> para exportar un CSV.</li>
  </ol>
  <p>¿Detrás de una red corporativa? Configure un proxy en
     <b>Configuración de proxy</b> en la esquina superior derecha.</p>
  <div class="cite">
    <b>Cita</b> &mdash; las publicaciones que utilicen este complemento deben citar:<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "fr": """
  <h1>ClimaPlots</h1>
  <p class="sub">Analyse climatique avec NASA POWER et Open-Meteo (ERA5), dans QGIS.</p>
  <p>ClimaPlots télécharge des décennies de données climatiques quotidiennes pour
     n'importe quel point de la carte et les transforme en graphiques interactifs
     &mdash; sans programmation. Choisissez entre deux sources de données :
     <b>NASA POWER</b> (depuis 1981) et <b>Open-Meteo (ERA5)</b> (depuis 1940).</p>
  <h2>Ce qu'il produit</h2>
  <p><b>Tendances annuelles</b> de température, précipitations, humidité relative,
     irradiation, vitesse du vent, ET&#8320; de référence et degrés-jours de
     croissance, chacune annotée avec le test de tendance <b>Mann&ndash;Kendall</b>
     et le test d'homogénéité <b>Pettitt</b>.</p>
  <p><b>Diagramme thermo-pluviométrique</b> &mdash; le régime mensuel moyen de
     précipitations et de température du lieu.</p>
  <p><b>Indices climatiques</b> &mdash; indices de température et de précipitations
     ETCCDI plus l'Indice de Précipitations Standardisé (SPI).</p>
  <h2>Comparer deux lieux ou deux sources</h2>
  <p>Ajoutez un <b>point de comparaison B</b> optionnel pour superposer une deuxième
     série sur le graphique des Tendances, avec des statistiques de tendance rapportées
     pour les deux points. B peut utiliser sa propre source de données, de sorte que
     le <i>même</i> lieu peut être comparé entre NASA POWER et Open-Meteo &mdash;
     utilisez <b>Même emplacement que A</b> pour copier les coordonnées du point A
     sans recliquer sur la carte.</p>
  <h2>Démarrage rapide</h2>
  <ol>
    <li>Ouvrez la page <b>Coordonnées</b> et choisissez une <b>source de données</b>.</li>
    <li>Cliquez sur <b>Choisissez un point sur la carte</b> et cliquez sur un lieu
        (ou saisissez la longitude/latitude manuellement).</li>
    <li>Définissez optionnellement un <b>point de comparaison B</b> &mdash;
        choisissez-le sur la carte ou appuyez sur <b>Même emplacement que A</b>.</li>
    <li>Appuyez sur <b>Lancer l'analyse</b> et attendez le téléchargement des données.</li>
    <li>Parcourez les pages <b>Tendances</b>, <b>Thermo-pluviométrique</b> et
        <b>Indices</b>. Utilisez <b>Ouvrir dans le navigateur</b> pour un graphique
        plein écran, ou <b>Enregistrer les données</b> pour exporter un CSV.</li>
  </ol>
  <p>Derrière un réseau d'entreprise ? Configurez un proxy via
     <b>Paramètres du proxy</b> dans le coin supérieur droit.</p>
  <div class="cite">
    <b>Citation</b> &mdash; les publications utilisant ce module doivent citer :<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "it": """
  <h1>ClimaPlots</h1>
  <p class="sub">Analisi climatica con NASA POWER e Open-Meteo (ERA5), dentro QGIS.</p>
  <p>ClimaPlots scarica decenni di dati climatici giornalieri per qualsiasi punto della
     mappa e li trasforma in grafici interattivi &mdash; senza necessità di
     programmazione. Scegli tra due fonti di dati: <b>NASA POWER</b> (dal 1981) e
     <b>Open-Meteo (ERA5)</b> (dal 1940).</p>
  <h2>Cosa produce</h2>
  <p><b>Tendenze annuali</b> di temperatura, precipitazioni, umidità relativa,
     irradiazione, velocità del vento, ET&#8320; di riferimento e gradi-giorno di
     crescita, ciascuna annotata con il test di tendenza <b>Mann&ndash;Kendall</b>
     e il test di omogeneità <b>Pettitt</b>.</p>
  <p><b>Diagramma termopluviometrico</b> &mdash; il regime mensile medio di
     precipitazioni e temperatura del luogo.</p>
  <p><b>Indici climatici</b> &mdash; indici di temperatura e precipitazioni ETCCDI
     più l'Indice di Precipitazione Standardizzato (SPI).</p>
  <h2>Confrontare due luoghi o due fonti</h2>
  <p>Aggiungi un <b>punto di confronto B</b> opzionale per sovrapporre una seconda
     serie al grafico delle Tendenze, con statistiche di tendenza riportate per
     entrambi i punti. B può usare la propria fonte di dati, quindi lo <i>stesso</i>
     luogo può essere confrontato tra NASA POWER e Open-Meteo &mdash; usa
     <b>Stessa posizione di A</b> per copiare le coordinate del punto A senza
     riscattare la mappa.</p>
  <h2>Avvio rapido</h2>
  <ol>
    <li>Apri la pagina <b>Coordinate</b> e scegli una <b>fonte dati</b>.</li>
    <li>Clicca su <b>Scegli un punto sulla mappa</b> e clicca su un luogo
        (o digita manualmente la longitudine/latitudine).</li>
    <li>Facoltativamente, imposta un <b>punto di confronto B</b> &mdash; sceglilo
        sulla mappa o premi <b>Stessa posizione di A</b>.</li>
    <li>Premi <b>Esegui analisi</b> e attendi il download dei dati.</li>
    <li>Sfoglia le pagine <b>Tendenze</b>, <b>Termopluviometrico</b> e <b>Indici</b>.
        Usa <b>Apri nel browser</b> per un grafico a schermo intero, o
        <b>Salva dati</b> per esportare un CSV.</li>
  </ol>
  <p>Dietro una rete aziendale? Imposta un proxy tramite <b>Impostazioni proxy</b>
     nell'angolo in alto a destra.</p>
  <div class="cite">
    <b>Citazione</b> &mdash; le pubblicazioni che utilizzano questo plugin devono citare:<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "hi": """
  <h1>ClimaPlots</h1>
  <p class="sub">NASA POWER और Open-Meteo (ERA5) से जलवायु विश्लेषण, QGIS के अंदर।</p>
  <p>ClimaPlots मानचित्र पर किसी भी बिंदु के लिए दशकों के दैनिक जलवायु डेटा को
     डाउनलोड करता है और उन्हें इंटरेक्टिव चार्ट में बदलता है &mdash; कोई कोडिंग
     आवश्यक नहीं। दो डेटा स्रोतों में से चुनें: <b>NASA POWER</b> (1981 से) और
     <b>Open-Meteo (ERA5)</b> (1940 से)।</p>
  <h2>यह क्या उत्पन्न करता है</h2>
  <p>तापमान, वर्षा, सापेक्ष आर्द्रता, विकिरण, पवन गति, संदर्भ ET&#8320; और बढ़ने
     के डिग्री-दिनों की <b>वार्षिक प्रवृत्तियाँ</b>, प्रत्येक
     <b>Mann&ndash;Kendall</b> प्रवृत्ति और <b>Pettitt</b> समरूपता परीक्षणों के साथ।</p>
  <p><b>ताप-वर्षामापी आरेख</b> &mdash; स्थान का औसत मासिक वर्षा और तापमान व्यवस्था।</p>
  <p><b>जलवायु सूचकांक</b> &mdash; ETCCDI तापमान और वर्षा सूचकांक तथा
     मानकीकृत वर्षा सूचकांक (SPI)।</p>
  <h2>दो स्थानों या दो स्रोतों की तुलना</h2>
  <p>Trends चार्ट पर दूसरी श्रृंखला ओवरले करने के लिए एक वैकल्पिक
     <b>तुलना बिंदु B</b> जोड़ें, दोनों बिंदुओं के लिए प्रवृत्ति आँकड़े रिपोर्ट
     किए जाते हैं। B अपना डेटा स्रोत उपयोग कर सकता है, इसलिए <i>समान</i> स्थान की
     NASA POWER और Open-Meteo में तुलना की जा सकती है &mdash; मानचित्र पर पुनः क्लिक
     किए बिना बिंदु A के निर्देशांक कॉपी करने के लिए <b>A के समान स्थान</b> का
     उपयोग करें।</p>
  <h2>त्वरित प्रारंभ</h2>
  <ol>
    <li><b>निर्देशांक</b> पृष्ठ खोलें और एक <b>डेटा स्रोत</b> चुनें।</li>
    <li><b>मानचित्र पर एक बिंदु चुनें</b> पर क्लिक करें और मानचित्र पर एक स्थान
        क्लिक करें (या देशांतर/अक्षांश मैन्युअल रूप से टाइप करें)।</li>
    <li>वैकल्पिक रूप से एक <b>तुलना बिंदु B</b> सेट करें &mdash; मानचित्र पर
        चुनें, या <b>A के समान स्थान</b> दबाएं।</li>
    <li><b>विश्लेषण चलाएँ</b> दबाएं और डेटा डाउनलोड होने की प्रतीक्षा करें।</li>
    <li><b>रुझान</b>, <b>ताप-वर्षामापी</b> और <b>सूचकांक</b> पृष्ठ देखें। पूर्ण-स्क्रीन
        चार्ट के लिए <b>ब्राउज़र में खोलें</b>, या CSV निर्यात के लिए
        <b>डेटा सहेजें</b> का उपयोग करें।</li>
  </ol>
  <p>कॉर्पोरेट नेटवर्क के पीछे? ऊपरी-दाएं कोने में <b>प्रॉक्सी सेटिंग्स</b> के
     माध्यम से प्रॉक्सी सेट करें।</p>
  <div class="cite">
    <b>उद्धरण</b> &mdash; इस प्लगइन का उपयोग करने वाले प्रकाशनों को उद्धृत करना होगा:<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
    "zh": """
  <h1>ClimaPlots</h1>
  <p class="sub">基于 NASA POWER 和 Open-Meteo (ERA5) 的气候分析，集成于 QGIS。</p>
  <p>ClimaPlots 可为地图上任意一点下载数十年的每日气候数据，并将其转化为交互式图表
     &mdash; 无需编程。可在两种数据源之间选择：<b>NASA POWER</b>（自 1981 年起）和
     <b>Open-Meteo (ERA5)</b>（自 1940 年起）。</p>
  <h2>功能概览</h2>
  <p>气温、降水量、相对湿度、辐射、风速、参考 ET&#8320; 和生长积温的<b>年度趋势</b>，
     每项均标注 <b>Mann&ndash;Kendall</b> 趋势检验和 <b>Pettitt</b> 均一性检验结果。</p>
  <p><b>温雨图</b> &mdash; 该地点的月平均降水量和温度变化规律。</p>
  <p><b>气候指数</b> &mdash; ETCCDI 温度和降水指数，以及标准化降水指数 (SPI)。</p>
  <h2>对比两个地点或两个数据源</h2>
  <p>添加可选的<b>对比点 B</b>，在趋势图中叠加第二条数据系列，并同时报告两点的趋势
     统计。B 可使用独立的数据源，因此<i>同一</i>地点可在 NASA POWER 和 Open-Meteo
     之间进行对比 &mdash; 使用<b>与 A 相同的位置</b>可直接复制点 A 的坐标，无需重新
     点击地图。</p>
  <h2>快速入门</h2>
  <ol>
    <li>打开<b>坐标</b>页面，选择<b>数据源</b>。</li>
    <li>点击<b>在地图上选择一个点</b>，然后在地图上点击某个位置（或手动输入经度/纬度）。</li>
    <li>可选：设置<b>对比点 B</b> &mdash; 在地图上选取，或按<b>与 A 相同的位置</b>。</li>
    <li>点击<b>运行分析</b>，等待数据下载完成。</li>
    <li>浏览<b>趋势</b>、<b>温雨图</b>和<b>指数</b>页面。使用<b>在浏览器中打开</b>
        查看全屏图表，或使用<b>保存数据</b>导出 CSV。</li>
  </ol>
  <p>位于企业网络内？通过右上角的<b>代理设置</b>配置代理。</p>
  <div class="cite">
    <b>引用</b> &mdash; 使用本插件的出版物必须引用：<br>
    <a href="https://doi.org/10.1590/1678-4499.20250223">
      https://doi.org/10.1590/1678-4499.20250223</a>
  </div>
""",
}
