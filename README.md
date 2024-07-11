Exekutatu behar den fitxeroa: 06-Multiple.py

Technical problems
1) Streamlit-i esan egin behar zaio ze modulo instalatu. Hortarako, Requirements.txt fitxero
   sortu behar da.
   Sortzeko. Fitxeroa dagoen direktorioan, exekutatu: pipreqs.
2) Yfinance-ek errorea ematen zuen. Konpontzeko, import yfinance aurretik bi lerro gehitu ditut.

-Fitxero nagusia: 06-Multiple.py

Bertan Streamlit-en Multipage dago. Beraz, barruan, beste python fitxero batzuk irakurtzen ditu. 
Fitxero hauek pages karpetaren barruan daude.

Momentuz, datuak azkeneko denbora eremu batean irakurtzen ditu.

Egin daitezkeen aldaketak:
1) Hasiera eta bukaera datak nik jarri (Linux-en ordenagailuan badaukat bertsio bat: 
     Stock_Python_Ubuntu_June24/pages/Besteak_pages/08-s_and_p_mp.py
2) Taula batean (st.table), balio konkretu bat jarri
3) Pyplot edo Matplotlib-subplot erabiliz, grafika interktiboak egin daitezke, 
 baina aukera guztiek ez dute ondo funtionatzen. Ikusi:
    Stock_Python_Ubuntu_June24/pages/Besteak_pages/
